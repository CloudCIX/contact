# stdlib
from typing import List
import logging
import requests
# libs
from django.conf import settings
# local


def vector_similarity(api_key, names, encoder, query, order_by, limit, threshold):  # pragma: no cover
    logger = logging.getLogger('contact.vector.vector_similarity')
    if settings.TESTING:
        return []

    logger.info(f'Vector DB Embeddings retrieval Process with Model {encoder} Start')
    embedding_vectors = []
    data = {
        'api_key': api_key,
        'names': names,
        'method': 'vector_search',
        'encoder_name': encoder,
        'query': query,
        'order_by': order_by,
        'threshold': threshold,
        'limit': limit,
    }
    try:
        response = requests.post(
            url=settings.EMBEDDING_DB_URL,
            json=data,
            timeout=600,
        )
    except Exception as e:  # pragma: no cover
        logger.error(f'A non 200 response has occurred with the Embedding DB API service: {e}.')
        return []

    if response.status_code == 200:
        embedding_vectors.extend(response.json()['content'])

    logger.info(f'Vector DB Embeddings retrieval Process with Model {encoder} End')

    return embedding_vectors


def best_match_25(api_key, names, chunks, limit, query):  # pragma: no cover
    if settings.TESTING:
        return []

    logger = logging.getLogger('contact.vector.best_match_25')
    top_chunks = []
    try:
        data = {
            'api_key': api_key,
            'method': 'keyword_search',
            'names': names,
            'chunks': chunks,
            'limit': limit,
            'query': query,
        }
        response = requests.post(
            url=settings.EMBEDDING_DB_URL,
            json=data,
            timeout=600,
        )
    except Exception as e:
        logger.error(f'A non 200 response has occurred with the Embedding DB API service: {e}.')
        return top_chunks

    if response.status_code == 200:
        top_chunks = response.json()['content']

    logger.info('Key word search End')

    return top_chunks


def rerank(chatbot, chunks: List, users_question: str):
    logger = logging.getLogger('contact.vector.rerank')
    logger.info('Rerank Process Start')
    reranked_chunks = []
    try:
        data = {
            'api_key': chatbot.api_key,
            'method': 'rerank',
            'reranker': chatbot.reranker,
            'reranking_limit': chatbot.reranking_limit,
            'query': users_question,
            'chunks': chunks,
        }
        response = requests.post(
            url=settings.EMBEDDING_DB_URL,
            json=data,
            timeout=600,
        )
    except Exception as e:
        logger.error(f'A non 200 response has occurred with the Embedding DB API service: {e}.')
        return reranked_chunks

    if response.status_code == 200:
        reranked_chunks = response.json()['content']

    logger.info('Rerank Process End')

    return reranked_chunks
