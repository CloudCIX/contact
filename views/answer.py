"""
Management for Answer
"""
import logging
# stdlib
import sys
from copy import deepcopy

# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from contact.intent import Intent, classify_intent
# local
from contact.llm import ContactExceptionError, create_prompt, echo, llm
from contact.models import Chatbot, Conversation, QAndA
from contact.permissions.answer import Permissions
from contact.smalltalk import smalltalk
from contact.utils import CustomStreamingHttpResponse
from contact.vector import best_match_25, rerank, vector_similarity
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.request import Request
from rest_framework.response import Response

__all__ = [
    'AnswerCollection',
]


class AnswerCollection(APIView):
    """
    Request to Answer a Question in a Conversation.
    """

    @staticmethod
    def streaming_answer(response, conversation, users_question, users_images=[]):
        logger = logging.getLogger('contact.views.answer.streaming_answer')
        logger.info('Streaming Answer Process Start')
        answer_content = ''
        try:
            for ans in response:
                answer_content += str(ans)
                yield ans
                sys.stdout.flush()
        except ContactExceptionError:
            logger = logging.getLogger('contact.views.answer.streaming_answer')
            logger.error('LLM Error occurred while getting answer from chatbot LLM.')
            yield 'An unknown error has occurred, please try again later.'
            sys.stdout.flush()
            return
        except Exception as e:  # pragma: no cover
            logger = logging.getLogger('contact.views.answer.streaming_answer')
            logger.error(f'An unknown error has occurred while streaming the answer. Exception: {e}')
            yield 'An unknown error has occurred, please try again later.'
            sys.stdout.flush()
            return

        QAndA.objects.create(
            answer=answer_content,
            conversation=conversation,
            question=users_question,
            question_images=users_images,
        )
        logger.info('Streaming Answer Process End')

    @staticmethod
    def streaming_error_response():
        response = ['An', 'unknown', 'error', 'has', 'occurred,', 'please', 'try', 'again', 'later.']
        for ans in response:
            yield ans
            sys.stdout.flush()

    def post(self, request: Request, chatbot_name: str) -> Response:
        """
        summary: Answer sent Question

        description: |
            This service will answer the sent question, create a new q_and_a in Conversation and return the
            Q and A details

            Parameters required to be sent in data are:
            1. question: String to be answered
            2. conversation_id: The ID of the Conversation which must be in the Chatbot

        path_params:
            chatbot_name:
                description: The name of the Chatbot to Answer question.
                type: string

        responses:
            200:
                description: Question answered successfully, Q and A record created and returned.
                content:
                    text/plain; charset=utf-8:
                        schema:
                            type: string
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER
        data = request.data

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                chatbot = Chatbot.objects.get(name=chatbot_name)
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_answer_create_001')

        with tracer.start_span('checking_for_required_fields', child_of=request.span):
            if 'question' not in data or 'conversation_id' not in data:
                return Http400(error_code='contact_answer_create_002')

            users_question = data['question']
            users_images = data.get('images', [])

        with tracer.start_span('validate_conversation_id', child_of=request.span):
            try:
                conversation = Conversation.objects.get(pk=data['conversation_id'], chatbot=chatbot)
            except Conversation.DoesNotExist:
                return Http404(error_code='contact_answer_create_003')

        with tracer.start_span('smalltalk_attempting_to_answer', child_of=request.span):
            users_question = data['question']
            smalltalk_question, smalltalk_answer = smalltalk(users_question)

            if smalltalk_answer is not None:
                def streaming_small_talk_answer():
                    for ans in smalltalk_answer.split():
                        yield ans + ' '

                return StreamingHttpResponse(
                    streaming_small_talk_answer(),
                    content_type='application/json; charset=utf-8',
                )

        if chatbot.apply_intent_classification:
            with tracer.start_span('classify_intent', child_of=request.span):
                try:
                    intent = classify_intent(chatbot, conversation, users_question)
                except ContactExceptionError:  # pragma: no cover
                    return CustomStreamingHttpResponse(
                        self.streaming_error_response(),
                        content_type='text/event-stream; charset=utf-8',
                    )
            if intent == Intent.SMALLTALK:
                with tracer.start_span('get_smalltalk_answer_from_chatbot_llm', child_of=request.span):
                    try:
                        # NOTE: deepcopy chatbot to override fields used in llm.py:
                        # Is this the best practice?
                        smalltalk_chatbot = deepcopy(chatbot)
                        smalltalk_chatbot.system_prompt = smalltalk_chatbot.smalltalk_prompt
                        smalltalk_chatbot.user_prompt = None
                        prompt = create_prompt(conversation, chatbot, [], users_question, users_images)
                        if smalltalk_chatbot.echo:
                            answer = echo(prompt)
                            return CustomStreamingHttpResponse(
                                self.streaming_answer(
                                    [(item + ' ').encode('utf-8') for item in answer.split()],
                                    conversation,
                                    users_question,
                                    users_images,
                                ),
                                content_type='text/event-stream; charset=utf-8',
                            )
                        else:
                            answer = llm(smalltalk_chatbot, prompt)
                            return CustomStreamingHttpResponse(
                                self.streaming_answer(answer, conversation, users_question, users_images),
                                content_type='text/event-stream; charset=utf-8',
                            )
                    except ContactExceptionError:  # pragma: no cover
                        return CustomStreamingHttpResponse(
                            self.streaming_error_response(),
                            content_type='text/event-stream; charset=utf-8',
                        )

        # testing the vector similarity function in vector.py file related to answer service
        with tracer.start_span('getting_similiar_chunks', child_of=request.span):
            similar_chunks = vector_similarity(
                chatbot.api_key,
                chatbot.corpus_names,
                chatbot.encoder,
                users_question,
                chatbot.similarity,
                chatbot.reference_limit,
                float(chatbot.threshold),
            )
            chunks = []
            for item in similar_chunks:
                hyperlink, chunk, distance = item
                chunks.append([hyperlink, chunk])

            if chatbot.apply_reranking:
                bm25_chunks = best_match_25(
                    chatbot.api_key,
                    chatbot.corpus_names,
                    None,
                    chatbot.bm25_limit,
                    users_question,
                )
                for item in bm25_chunks:
                    chunks.append([item[0], item[1]])
                chunk_set = list(set([tuple(item) for item in chunks]))
                chunks = [list(item) for item in chunk_set]
                top_chunks = rerank(chatbot, chunks, users_question)
            elif chatbot.bm25_limit > 0:
                top_chunks = best_match_25(chatbot.api_key, None, chunks, chatbot.bm25_limit, users_question)
            else:
                top_chunks = chunks

        with tracer.start_span('getting_answer_from_chatbot_llm', child_of=request.span):
            prompt = create_prompt(conversation, chatbot, top_chunks, users_question, users_images)
            # Fallback: if there are no similar/reference chunks and chatbot.no_reference_answer is set
            if len(top_chunks) == 0 and bool(getattr(chatbot, 'no_reference_answer', '')):
                fallback_text = chatbot.no_reference_answer
                answer_iterable = [(item + ' ').encode('utf-8') for item in fallback_text.split()]
                return CustomStreamingHttpResponse(
                    self.streaming_answer(answer_iterable, conversation, users_question, users_images),
                    content_type='text/event-stream; charset=utf-8',
                )
            if chatbot.echo is False:
                try:
                    answer = llm(chatbot, prompt)
                    return CustomStreamingHttpResponse(
                        self.streaming_answer(answer, conversation, users_question, users_images),
                        content_type='text/event-stream; charset=utf-8',
                    )
                except ContactExceptionError:  # pragma: no cover
                    logger = logging.getLogger('contact.views.answer.streaming_error')
                    logger.error('LLM Error occurred while getting answer from chatbot LLM.')
                    return CustomStreamingHttpResponse(
                        self.streaming_error_response(),
                        content_type='text/event-stream; charset=utf-8',
                    )
            else:
                answer = echo(prompt)
                return CustomStreamingHttpResponse(
                    self.streaming_answer(
                        [(item + ' ').encode('utf-8') for item in answer.split()],
                        conversation,
                        users_question,
                        users_images,
                    ),
                    content_type='text/event-stream; charset=utf-8',
                )
