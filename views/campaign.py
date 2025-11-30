"""
Management for Campaign
"""
# stdlib
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import (
    CampaignCreateController,
    CampaignListController,
    CampaignUpdateController,
)
from contact.models import Campaign
from contact.permissions.campaign import Permissions
from contact.serializers import CampaignSerializer


__all__ = [
    'CampaignCollection',
    'CampaignResource',
]


class CampaignCollection(APIView):
    """
    Handles methods regarding Campaign records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Campaign records

        description: |
            Retrieve a list of the Campaign records for the requesting User's Member.

        responses:
            200:
                description: A list of the Campaign records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            try:
                objs = Campaign.objects.filter(
                    member_id=request.user.member['id'],
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_campaign_list_001')

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
            data = CampaignSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Campaign record

        description: |
            Create a new Campaign record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Camapign record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CampaignSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class CampaignResource(APIView):
    """
    Handles methods regarding Campaign records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Campaign record

        description: |
            Attempt to read a Campaign record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Campaign record to be read
                type: integer

        responses:
            200:
                description: Campaign record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_campaign_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=pk, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = CampaignSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Campaign record
        description: |
            Attempt to update a Campaign record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Campaign record to be updated
                type: integer

        responses:
            200:
                description: Campaign record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_campaign_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=pk, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = CampaignUpdateController(
                data=request.data,
                instance=obj,
                partial=partial,
                request=request,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('Serializing_data', child_of=request.span):
            data = CampaignSerializer(instance=controller.instance).data
        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Campaign record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Campaign record

        description: |
            Attempt to delete a Campaign record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Campaign record to delete
                type: integer

        responses:
            204:
                description: Campaign record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_campaign_object', child_of=request.span):
            try:
                obj = Campaign.objects.get(id=pk, member_id=request.user.member['id'])
            except Campaign.DoesNotExist:
                return Http404(error_code='contact_campaign_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
