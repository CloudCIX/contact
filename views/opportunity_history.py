"""
Management for Opportunity History
"""
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
# local
from contact.controllers import OpportunityHistoryListController, OpportunityHistoryCreateController
from contact.models import Opportunity, OpportunityHistory
from contact.notification import OpportunityHistoryNotification
from contact.serializers import OpportunityHistorySerializer

__all__ = [
    'OpportunityHistoryCollection',
]


class OpportunityHistoryCollection(APIView):
    """
    Handles methods regarding Contact records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request, opportunity_id: int) -> Response:
        """
        summary: Retrieve a list of Opportunity History records

        description: |
            Retrieve a list of the Opportunity History records for the requesting User's Member.

        path_params:
            opportunity_id:
                description: The id of the Opportunity record
                type: integer

        responses:
            200:
                description: A list of the Opportunity History records, filtered and ordered by the User
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_opportunity_object', child_of=request.span):
            try:
                opportunity_obj = Opportunity.objects.get(
                    id=opportunity_id,
                    member_id=request.user.member['id'],
                )
            except Opportunity.DoesNotExist:
                return Http404(error_code='contact_opportunity_history_list_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = OpportunityHistoryListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            objs = OpportunityHistory.objects.filter(
                opportunity=opportunity_obj,
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
            data = OpportunityHistorySerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request, opportunity_id: int) -> Response:
        """
        summary: Create a new Opportunity History record

        description: |
            Create a new Opportunity History record in the requesting User's Member, using the data
            supplied by the User.

        path_params:
            opportunity_id:
                description: The id of the Opportunity record
                type: integer

        responses:
            201:
                description: Opportunity History record was created successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_opportunity_object', child_of=request.span):
            try:
                opportunity_obj = Opportunity.objects.get(
                    id=opportunity_id,
                    member_id=request.user.member['id'],
                )
            except Opportunity.DoesNotExist:
                return Http404(error_code='contact_opportunity_history_create_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = OpportunityHistoryCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.opportunity = opportunity_obj
            controller.instance.user_id = request.user.id
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = OpportunityHistorySerializer(instance=controller.instance).data

        with tracer.start_span('sending_notification', child_of=request.span):
            if controller.instance.history_type == OpportunityHistory.EMAIL:
                # Opportunity History Send Email
                OpportunityHistoryNotification().send(user=request.user, opportunity_history=data)

        return Response({'content': data}, status=status.HTTP_201_CREATED)
