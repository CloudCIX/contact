"""
Management for Campaign Contact
"""
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import (
    CampaignContactCreateController,
    CampaignContactUpdateController,
    CampaignContactDeleteController,
)
from contact.models import Campaign, CampaignContact


__all__ = [
    'CampaignContactCollection',
]


class CampaignContactCollection(APIView):
    """
    Handle methods regarding CampaignContact records that doesn't require an Id to be specified
    """

    def post(self, request: Request, campaign_id: int) -> Response:
        """
        summary: Create one or more new CampaignContact records

        description: |
            Create new CampaignContact records in the requesting User's Member, using the data supplied by the User.

        path_params:
            campaign_id:
                description: The ID of the Campaign record to create Contacts in
                type: Integer

        responses:
            201:
                description: CampaignContact records were created successfully
                content: none
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_request_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=campaign_id, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_contact_create_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignContactCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('adding_CampaignContact', child_of=request.span):
            contacts = controller.cleaned_data.pop('contacts')
            if contacts is not None and contacts.count() > 0:
                CampaignContact.objects.bulk_create(
                    (
                        CampaignContact(campaign=obj, contact=contact)
                        for contact in contacts.iterator()
                    ), ignore_conflicts=True,
                )

        return Response(status=status.HTTP_201_CREATED)

    def put(self, request: Request, campaign_id: int) -> Response:
        """
        summary: Update the details of a specified CampaignContact record

        description: |
            Attempt to update CampaignContact records by the given `campaign_id`, returning a 404 if the Campaign
            record does not exist.
        path_params:
            campaign_id:
                description: The ID of the Campaign record to update Contacts in
                type: integer
        responses:
            200:
                description: CampaignContact records were updated successfully
                content: none
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_request_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=campaign_id, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_contact_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignContactUpdateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('adding_CampaignContact', child_of=request.span):
            contacts = controller.cleaned_data.pop('contacts')
            responded = controller.cleaned_data.pop('responded', None)
            if responded is not None and contacts is not None and contacts.count() > 0:
                CampaignContact.objects.filter(campaign=obj, contact__in=contacts).update(responded=responded)
        return Response()

    def delete(self, request: Request, campaign_id: int) -> Response:
        """
        summary: Create a new CampaignContact record

        description: |
            Delete a CampaignContact record in the requesting User's Member, using the data supplied by the User.

        path_params:
            campaign_id:
                description: The ID of the Campaign record to delete Contacts in
                type: Integer

        responses:
            204:
                description: CampaignContact record was deleted successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_request_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=campaign_id, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_contact_delete_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignContactDeleteController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('removing_campaign_contacts', child_of=request.span):
            contacts = controller.cleaned_data.pop('contacts')

            CampaignContact.objects.filter(campaign=obj, contact__in=contacts).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
