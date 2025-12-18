# std lib
import datetime
import logging
import string

import openai
# libs
import requests
# local
from contact.models import QAndA
from openai import OpenAI


class ContactExceptionError():
    pass


LLM_DICT = {
    'chatgpt4': 'GPT-4o',
    'chatgpt4.1': 'GPT-4.1',
    'uccix_instruct': 'UCCIX-Instruct',
    'uccix_instruct_70b': 'UCCIX-v2-Llama3.1-70B-Instruct',
    'UCCIX-Mistral-24B': 'UCCIX-Mistral-24B',
    'deepseek': 'deepseek-ai/DeepSeek-R1-Distill-Llama-70B',
}


def llm_summary(chatbot, messages):
    logger = logging.getLogger('contact.llm.llm_summary')
    logger.info('LLM Summary Process Start')
    try:
        client = OpenAI(
            api_key=chatbot.api_key,
            base_url='https://ml-openai.cloudcix.com',
        )

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=LLM_DICT['uccix_instruct_70b'],
            stream=True,
            timeout=600,
            max_tokens=100,
            temperature=0.1,
            seed=42,
        )
    except (
        openai.InternalServerError,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
    ) as e:  # pragma: no cover
        logger.error(f'A non 200 response has occurred with the LLM Summary service.\nException: {e}')
        raise ContactExceptionError()
    logger.info('LLM Summary Process End')

    for chunk in chat_completion:
        if not chunk.choices or chunk.choices[0].delta is None:
            continue
        yield chunk.choices[0].delta.content


def llm(chatbot, messages):
    logger = logging.getLogger('contact.llm.llm')
    logger.info('LLM Process Start')
    try:
        client = OpenAI(
            api_key=chatbot.api_key,
            base_url='https://ml-openai.cloudcix.com',
        )

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=LLM_DICT[chatbot.nn_llm],
            stream=True,
            timeout=600,
            max_tokens=chatbot.max_tokens,
            temperature=float(chatbot.temperature),
        )
    except (
        openai.InternalServerError,
        requests.exceptions.ConnectionError,
        requests.exceptions.HTTPError,
        requests.exceptions.Timeout,
        requests.exceptions.RequestException,
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

    if chatbot.nn_llm in ['chatgpt4', 'uccix_instruct']:
        for chunk in chat_completion:
            if not chunk.choices or chunk.choices[0].delta is None:
                continue
            yield chunk.choices[0].delta.content
    else:
        for chunk in chat_completion:
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
