"""
Management for Summary
"""
# stdlib
# libs
from cloudcix_rest.exceptions import Http400, Http404, Http503
from cloudcix_rest.views import APIView
# local
from contact.llm import ContactExceptionError, llm_summary
from contact.models import Chatbot, Contact, Conversation
from contact.permissions.summary import Permissions
from contact.serializers import ConversationSerializer
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

__all__ = [
    'SummaryCollection',
]


class SummaryCollection(APIView):
    """
    Request to Summarise a Question.
    """

    serializer_class = ConversationSerializer

    def post(self, request: Request, chatbot_name: str) -> Response:
        """
        summary: Summarise sent Question

        description: |
            This service will summarise the sent question, create a new conversation and return the
            Conversation details

            Parameters required to be sent in data are:
            1. question: String to be summarised
            2. contact_id: The ID of the Contact which must be in the same Member as the Chatbot

        path_params:
            chatbot_name:
                description: The name of the Chatbot to create a Summary heading of a Conversation.
                type: string

        responses:
            201:
                description: Question summarised successfully, Conversation record created and returned.
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
                obj = Chatbot.objects.get(name=chatbot_name)
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_summary_create_001')

        with tracer.start_span('checking_for_required_fields', child_of=request.span):
            contact_id = data.get('contact_id', None)
            cookie = data.get('cookie', None)
            question = data.get('question', None)
            if question is None or (contact_id is None and cookie is None):
                return Http400(error_code='contact_summary_create_002')

        with tracer.start_span('validate_contact_id', child_of=request.span):
            if contact_id is not None:
                try:
                    Contact.objects.get(pk=data['contact_id'], member_id=obj.member_id)
                except Contact.DoesNotExist:
                    return Http404(error_code='contact_summary_create_003')

        with tracer.start_span('summarising_question', child_of=request.span):
            try:
                content = f'Create a title in exactly 3 words for this text: "{question}". '
                content += 'The title should be in plain text only, no quotes, asterisks, or other formatting.'
                prompt = [{
                    'role': 'user',
                    'content': content,
                }]
                summary = llm_summary(obj, prompt)

                if len(summary) > 50:  # pragma: no cover
                    summary = summary[:50]

            except ContactExceptionError:  # pragma: no cover
                return Http503(error_code='contact_summary_create_004')

        with tracer.start_span('creating_conversation', child_of=request.span):
            conversation = Conversation.objects.create(name=summary, chatbot=obj, contact_id=contact_id, cookie=cookie)

        with tracer.start_span('serializing_conversation', child_of=request.span):
            data = ConversationSerializer(instance=conversation).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)
