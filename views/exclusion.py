"""
Management for Exclusion
"""
# stdlib
from datetime import datetime
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
    ExclusionCreateController,
    ExclusionListController,
    ExclusionUpdateController,
)
from contact.models import Exclusion
from contact.permissions.exclusion import Permissions
from contact.serializers import ExclusionSerializer

__all__ = [
    'ExclusionCollection',
    'ExclusionResource',
]


class ExclusionCollection(APIView):
    """
    Handles methods regarding Exclusion records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Exclusion records

        description: |
            Retrieve a list of the Exclusion records for the requesting User's Member.

        responses:
            200:
                description: A list of the exclusion records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ExclusionListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Exclusion.objects.filter(
                    member_id=request.user.member['id'],
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_exclusion_list_001')

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
            data = ExclusionSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Exclusion record

        description: |
            Create a new Exclusion record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Exclusion record was created successfully
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ExclusionCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ExclusionSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class ExclusionResource(APIView):
    """
    Handles methods regarding Exclusion records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Exclusion record

        description: |
            Attempt to read a Exclusion record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Exclusion record to be read
                type: integer

        responses:
            200:
                description: Exclusion record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_exclusion_object', child_of=request.span):
            try:
                obj = Exclusion.objects.get(id=pk, member_id=request.user.member['id'])
            except Exclusion.DoesNotExist:
                return Http404(error_code='contact_exclusion_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ExclusionSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Exclusion record
        description: |
            Attempt to update a Exclusion record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Exclusion record to be updated
                type: integer

        responses:
            200:
                description: Exclusion record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_exclusion_object', child_of=request.span):
            try:
                obj = Exclusion.objects.get(id=pk, member_id=request.user.member['id'])
            except Exclusion.DoesNotExist:
                return Http404(error_code='contact_exclusion_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ExclusionUpdateController(
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
            data = ExclusionSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Exclusion record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Exclusion record

        description: |
            Attempt to delete a Exclusion record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Exclusion record to delete
                type: integer

        responses:
            204:
                description: Exclusion record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_exclusion_object', child_of=request.span):
            try:
                obj = Exclusion.objects.get(id=pk, member_id=request.user.member['id'])
            except Exclusion.DoesNotExist:
                return Http404(error_code='contact_exclusion_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
