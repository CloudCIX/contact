"""
Management for Opportunity Contact
"""
# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import OpportunityContactCreateController, OpportunityContactDeleteController
from contact.models import Opportunity, OpportunityContact

__all__ = [
    'OpportunityContactCollection',
]


class OpportunityContactCollection(APIView):
    """
    Handles methods regarding Opportunity Contact records
    """
    def post(self, request: Request, opportunity_id: int) -> Response:
        """
        summary: Create a new Opportunity Contact record

        description: |
            Create a new Opportunity Contact record in the requesting User's Member, using the data
            supplied by the User.

        path_params:
            opportunity_id:
                description: The id of the Opportunity record
                type: integer

        responses:
            201:
                description: Opportunity Contact record was created successfully
                content: none
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
                return Http404(error_code='contact_opportunity_contact_create_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = OpportunityContactCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        contacts: Optional[QuerySet] = controller.cleaned_data.pop('contacts', None)

        with tracer.start_span('saving_opportunity_contact_object', child_of=request.span):
            if contacts is not None and contacts.count() > 0:
                OpportunityContact.objects.bulk_create(
                    (
                        OpportunityContact(
                            contact=contact,
                            opportunity=opportunity_obj,
                        )
                        for contact in contacts.iterator()
                    ),
                    ignore_conflicts=True,
                )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, opportunity_id: int):
        """
        summary: Delete a specified Opportunity Contact record

        description: |
            Attempt to delete an Opportunity Contact record in the requesting User's Member by the
            given 'opportunity_id', returning a 404 if it does not exist

        path_params:
            opportunity_id:
                description: The id of the Opportunity record associated with Opportunity contact record to delete
                type: integer

        responses:
            204:
                description: Opportunity Contact record was deleted successfully
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
                return Http404(error_code='contact_opportunity_contact_delete_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = OpportunityContactDeleteController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        contacts: Optional[QuerySet] = controller.cleaned_data.pop('contacts', None)

        with tracer.start_span('deleting_object', child_of=request.span):
            if contacts is not None and contacts.count() > 0:
                OpportunityContact.objects.filter(
                    contact__in=contacts,
                    opportunity=opportunity_obj,
                ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
