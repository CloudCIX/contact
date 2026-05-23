# std lib
import datetime
import json
import logging
import string

import openai
# libs
import httpx
# local
from django.conf import settings
from contact.models import QAndA
from openai import AsyncOpenAI
from pydantic import BaseModel


class ContactExceptionError(Exception):
    pass


LLM_DICT = {
    'UCCIX-Mistral-24B': 'UCCIX-Mistral-24B',
    'Mistral-Large-3': 'Mistral-Large-3',
}


class TitleResponse(BaseModel):
    title: str


class PromptRewriteResponse(BaseModel):
    rewritten_question: str


PROMPT_REWRITER_USER = """## CHATBOT CONTEXT
{chatbot_context}

---

## CHAT HISTORY
{chat_history}

---

## CURRENT USER QUESTION
{query}

---

## YOUR TASK
Rewrite the question above following the rules.
If no rewrite is needed, return it exactly as-is.

Rewritten Question:"""


def create_prompt_rewrite_messages(
    chat_history,
    users_question,
    chatbot_system_prompt='',
    chatbot_context_prompt='',
    rewrite_prompt_system='',
):
    """
    Build rewrite messages for the LLM rewriter.

    Args:
        chat_history: String of previous conversation exchanges (empty string if no prior messages)
        users_question: The current user question to rewrite
        chatbot_system_prompt: System instructions configured by the user (empty string if not set)
        chatbot_context_prompt: Knowledge base context prompt configured by the user (empty string if not set)
        rewrite_prompt_system: The prompt to instruct the rewriter LLM

    Returns:
        List of message dicts with 'role' and 'content' keys, ready to send to the LLM
    """
    # Combine the chatbot's system prompt and knowledge base context prompt
    # to provide domain awareness to the rewriter
    chatbot_context = ''
    if chatbot_system_prompt:
        chatbot_context += f'{chatbot_system_prompt}\n'
    if chatbot_context_prompt:
        chatbot_context += f'{chatbot_context_prompt}'

    user_prompt = PROMPT_REWRITER_USER.format(
        chatbot_context=chatbot_context.strip() or '(This chatbot has no system prompt or domain context configured)',
        chat_history=chat_history or '(No previous messages in this conversation)',
        query=users_question,
    )

    return [
        {'role': 'system', 'content': rewrite_prompt_system},
        {'role': 'user', 'content': user_prompt},
    ]


async def llm_summary(chatbot, messages):
    logger = logging.getLogger('contact.llm.llm_summary')
    logger.info('LLM Summary Process Start')
    try:
        client = AsyncOpenAI(
            api_key=chatbot.api_key,
            base_url=settings.CLOUDCIX_LLM_URL,
        )

        chat_completion = await client.chat.completions.parse(
            messages=messages,
            model=LLM_DICT[chatbot.nn_llm],
            timeout=600,
            max_tokens=200,
            temperature=0.15,
            seed=42,
            response_format=TitleResponse,
        )
    except (
        openai.APIConnectionError,
        openai.InternalServerError,
        httpx.ConnectError,
        httpx.HTTPStatusError,
        httpx.TimeoutException,
        httpx.RequestError,
    ) as e:  # pragma: no cover
        logger.error(f'A non 200 response has occurred with the LLM Summary service.\nException: {e}')
        raise ContactExceptionError()
    logger.info('LLM Summary Process End')

    result = json.loads(chat_completion.choices[0].message.content)
    return result['title']


async def llm_rewrite_prompt(chatbot, messages, original_question=''):
    logger = logging.getLogger('contact.llm.llm_rewrite_prompt')
    logger.info('LLM Prompt Rewriting Process Start')
    try:
        client = AsyncOpenAI(
            api_key=chatbot.api_key,
            base_url=settings.CLOUDCIX_LLM_URL,
        )

        chat_completion = await client.chat.completions.parse(
            messages=messages,
            model=LLM_DICT[chatbot.nn_llm],
            timeout=600,
            max_tokens=200,
            temperature=0.1,
            seed=42,
            response_format=PromptRewriteResponse,
        )
    except (
        openai.APIConnectionError,
        openai.InternalServerError,
        httpx.ConnectError,
        httpx.HTTPStatusError,
        httpx.TimeoutException,
        httpx.RequestError,
    ) as e:  # pragma: no cover
        logger.error(f'A non 200 response has occurred with the LLM Prompt Rewriting service.\nException: {e}')
        raise ContactExceptionError()
    logger.info('LLM Prompt Rewriting Process End')

    result = json.loads(chat_completion.choices[0].message.content)
    rewritten_question = str(result.get('rewritten_question', '')).strip()
    if len(rewritten_question) == 0:
        rewritten_question = str(original_question).strip()

    logger.info('Original Question: "%s"', original_question)
    logger.info('Rewritten Question: "%s"', rewritten_question)

    return {
        'rewritten_question': rewritten_question,
    }


async def llm(chatbot, messages):
    logger = logging.getLogger('contact.llm.llm')
    logger.info('LLM Process Start')
    try:
        client = AsyncOpenAI(
            api_key=chatbot.api_key,
            base_url=settings.CLOUDCIX_LLM_URL,
        )

        chat_completion = await client.chat.completions.create(
            messages=messages,
            model=LLM_DICT[chatbot.nn_llm],
            stream=True,
            timeout=600,
            max_tokens=chatbot.max_tokens,
            temperature=float(chatbot.temperature),
        )
    except (
        openai.APIConnectionError,
        openai.InternalServerError,
        httpx.ConnectError,
        httpx.HTTPStatusError,
        httpx.TimeoutException,
        httpx.RequestError,
    ) as e:  # pragma: no cover
        logger.error(f'A non 200 response has occurred with the LLM service.\nException: {e}')
        raise ContactExceptionError()
    except openai.NotFoundError:
        logger.error(
            f'The requested model {LLM_DICT[chatbot.nn_llm]} was not found in the LLM service for Chatbot '
            f'{chatbot.name}.',
        )
        error_message = (
            'The LLM for this chatbot is deprecated. Please contact support.'
        )
        for chunk in error_message:
            yield chunk
        return

    logger.info('LLM Process End')

    async for chunk in chat_completion:
        if not chunk.choices or chunk.choices[0].delta is None:
            continue
        content = chunk.choices[0].delta.content
        if content == '<think>':
            yield '[THINK]'
        elif content == '</think>':
            yield '[/THINK]'
        else:
            yield content


def echo(question):
    """
    Echo returns the constructed prompt of what would be sent to a LLM for debug purposes.
    """
    return str(question)


def create_prompt(conversation, chatbot, similar_chunks, users_question, users_images):
    logger = logging.getLogger('contact.llm.create_prompt')
    logger.info('Prompt Construction Process Start')
    prompt = []
    # Building prompt for sent question
    if bool(chatbot.system_prompt):
        prompt = [{'role': 'system', 'content': chatbot.system_prompt}]

    conversation_history = QAndA.objects.filter(
        conversation=conversation).order_by('-created')
    # Append previous answers to prompt constructed
    for q_and_a in conversation_history:
        if q_and_a.question_images and len(q_and_a.question_images) > 0:
            prompt += [
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': q_and_a.question},
                    ]
                    + [
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:{image[1]};base64,{image[0]}',
                                # https://platform.openai.com/docs/guides/images-vision?api-mode=chat&format=base64-encoded#analyze-images
                            },
                        }
                        for image in q_and_a.question_images
                    ],
                },
                {'role': 'assistant', 'content': q_and_a.answer},
            ]
        else:
            prompt += [
                {'role': 'user', 'content': q_and_a.question},
                {'role': 'assistant', 'content': q_and_a.answer},
            ]

    if chatbot.nn_llm != 'deepseek':
        content = f"""{users_question}"""
        if bool(chatbot.user_prompt) and len(similar_chunks) > 0:
            content += f"""\n\n{chatbot.user_prompt}"""

        count = 1
        for chunk in similar_chunks:
            content += f"""

{count}. According to [Source {string.ascii_uppercase[count - 1]}]({chunk[0]}):
{chunk[1]}"""

            count += 1
    else:
        content = ''
        if len(similar_chunks) > 0:
            if bool(chatbot.user_prompt):
                content += f"""{chatbot.user_prompt}"""
            content += "\n# The following contents are the search results related to the user's message:"
            count = 1
            for chunk in similar_chunks:
                content += f"""
[webpage {count} begin]
webpage_url: {chunk[0]}
webpage_content: {chunk[1]}
[webpage {count} end]
"""
                count += 1

            content += f"""
In the search results I provide to you, each result is formatted as [webpage X begin]...[webpage X end],
where X represents the numerical index of each article. Please cite the context at the end of the relevant
sentence when appropriate. Use the citation format [citation:X](citation_url) in the corresponding part of your answer.
If a sentence is derived from multiple contexts, list all relevant citation numbers, such as [citation:3](citation_url)
[citation:5](citation_url). Be sure not to cluster all citations at the end; instead, include them in the corresponding
parts of the answer.
When responding, please keep the following points in mind:
- Today is {datetime.date.today()}.
- Not all content in the search results is closely related to the user's question. You need to evaluate and filter the
search results based on the question.
- For listing-type questions (e.g., listing all flight information), try to limit the answer to 10 key points and inform
the user that they can refer to the search sources for complete information. Prioritize providing the most complete and
relevant items in the list. Avoid mentioning content not provided in the search results unless necessary.
- For creative tasks (e.g., writing an essay), ensure that references are cited within the body of the text,
such as [citation:3][citation:5], rather than only at the end of the text. You need to interpret and summarize
the user's requirements, choose an appropriate format, fully utilize the search results, extract key information,
and generate an answer that is insightful, creative, and professional. Extend the length of your response as much as
possible, addressing each point in detail and from multiple perspectives, ensuring the content is rich and thorough.
- If the response is lengthy, structure it well and summarize it in paragraphs. If a point-by-point format is needed,
try to limit it to 5 points and merge related content.
- For objective Q&A, if the answer is very brief, you may add one or two related sentences to enrich the content.
- Choose an appropriate and visually appealing format for your response based on the user's requirements and the
content of the answer, ensuring strong readability.
- Your answer should synthesize information from multiple relevant webpages and avoid repeatedly citing
the same webpage.
- Unless the user requests otherwise, your response should be in the same language as the user's question.

# The user's message is:
{users_question}
"""
        else:
            content += f'{users_question}'
    if users_images and len(users_images) > 0:
        prompt += [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': content},
                ]
                + [
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:{image[1]};base64,{image[0]}',
                        },
                    }
                    for image in users_images
                ],
            },
        ]
    else:
        prompt += [{'role': 'user', 'content': content}]
    logger.info('Prompt Construction Process End')

    return prompt
