"""
Management for Emveddings
"""
# stdlib
# libs
from cloudcix_rest.exceptions import Http404, Http400
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.models import Chatbot
from contact.vector import vector_similarity, best_match_25

__all__ = [
    'EmbeddingsResource',
]


class EmbeddingsResource(APIView):
    """
    Handles methods regarding Embedding records that do require an id to be specified, i.e. read
    """
    def get(self, request: Request, chatbot_name: str, pk: int) -> Response:  # pragma: no cover
        """
        summary: Read the top Chunks from embeddings for a specific query

        description: |
            Attempt to read top Chunks returned from embeddings of a specified chatbot_name, chatbot_id
            for a specific query and limit

        path_params:
            chatbot_name:
                description: The name of the Chatbot
                type: string
            pk:
                description: The id of the chatbot
                type: integer

        responses:
            200:
                description: |
                    Top chunks and their urls based on euclidean distance and limit from embeddings for specific query
                    asked and specified chatbot were read successfully
                content:
                    application/json:
                        schema:
                            type: object
            400: {}
            404: {}
        """
        tracer = settings.TRACER
        data = request.GET

        with tracer.start_span('retrieving_chatbot_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(name=chatbot_name, id=pk, member_id=request.user.member['id'])
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_embeddings_read_001')

        if 'query' not in data:
            return Http400(error_code='contact_embeddings_read_002')

        query = data['query']
        limit = data.get('limit', None)
        bm25_limit = data.get('bm25_limit', None)

        with tracer.start_span('get_chunks', child_of=request.span):
            if bm25_limit or limit:
                if bm25_limit is None:
                    chunks = vector_similarity(
                        obj.api_key,
                        obj.corpus_names,
                        obj.encoder,
                        query,
                        obj.similarity,
                        limit,
                        float(obj.threshold),
                    )
                elif limit is None:
                    chunks = best_match_25(obj.api_key, obj.corpus_names, None, bm25_limit, query)
                else:
                    base_chunks = vector_similarity(
                        obj.api_key,
                        obj.corpus_names,
                        obj.encoder,
                        query,
                        obj.similarity,
                        limit,
                        float(obj.threshold),
                    )
                    chunks = []
                    for item in base_chunks:
                        hyperlink, chunk, distance = item
                        chunks.append([hyperlink, chunk])
                    chunks = best_match_25(obj.api_key, None, chunks, bm25_limit, query)
            else:
                return Response({'content': []})
        return Response({'content': chunks})
