"""
Management for Corpus
"""
# stdlib
# libs
from cloudcix_rest.exceptions import Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import (
    CorpusListController,
)
from contact.models import Chatbot, Corpus
from contact.serializers import CorpusSerializer

__all__ = [
    'CorpusCollection',
]


class CorpusCollection(APIView):
    """
    Handles methods regarding Corpus records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request, chatbot_id: int) -> Response:
        """
        summary: Retrieve a list of Corpus records

        description: |
            Retrieve a list of the Corpus records for the requested Chatbot.

        path_params:
            chatbot_id:
                description: The id of the Chatbot record the Corpus is associated with.
                type: integer

        responses:
            200:
                description: A list of the Corpus records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        try:
            chatbot = Chatbot.objects.get(id=chatbot_id, member_id=request.user.member['id'])
        except Chatbot.DoesNotExist:
            return Http404(error_code='contact_corpus_list_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CorpusListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span):
            objs = Corpus.objects.filter(
                chatbot=chatbot,
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                controller.cleaned_data['order'],
            )

        with tracer.start_span('generating_metadata', child_of=request.span):
            limit = controller.cleaned_data['limit']
            order = controller.cleaned_data['order']
            page = controller.cleaned_data['page']
            total_records = objs.count()
            warnings = controller.warnings
            metadata = {
                'limit': limit,
                'order': order,
                'page': page,
                'total_records': total_records,
                'warnings': warnings,
            }
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = CorpusSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})
