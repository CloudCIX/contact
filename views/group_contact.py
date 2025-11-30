"""
Management for Group Contact
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
from ..controllers import GroupContactCreateController, GroupContactDeleteController
from ..models import Group, GroupContact

__all__ = [
    'GroupContactCollection',
]


class GroupContactCollection(APIView):
    """
    Handles methods regarding Group Contact records
    """
    def post(self, request: Request, group_id: int) -> Response:
        """
        summary: Create a new Group Contact record

        description: |
            Create a new Group Contact record in the requesting User's Member, using the data
            supplied by the User.

        path_params:
            group_id:
                description: The id of the Group record
                type: integer

        responses:
            201:
                description: Group Contact record was created successfully
                content: none
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_group_object', child_of=request.span):
            try:
                group_obj = Group.objects.get(
                    id=group_id,
                    member_id=request.user.member['id'],
                )
            except Group.DoesNotExist:
                return Http404(error_code='contact_group_contact_create_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = GroupContactCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        contacts: Optional[QuerySet] = controller.cleaned_data.pop('contacts', None)

        with tracer.start_span('saving_group_contact_object', child_of=request.span):
            if contacts is not None and contacts.count() > 0:
                GroupContact.objects.bulk_create(
                    (
                        GroupContact(
                            contact=contact,
                            group=group_obj,
                        )
                        for contact in contacts.iterator()
                    ),
                    ignore_conflicts=True,
                )
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, group_id: int):
        """
        summary: Delete a specified Group Contact record

        description: |
            Attempt to delete an Group Contact record in the requesting User's Member by the
            given 'group_id', returning a 404 if it does not exist

        path_params:
            group_id:
                description: The id of the Group record associated with Group contact record to delete
                type: integer

        responses:
            204:
                description: Group Contact record was deleted successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_group_object', child_of=request.span):
            try:
                group_obj = Group.objects.get(
                    id=group_id,
                    member_id=request.user.member['id'],
                )
            except Group.DoesNotExist:
                return Http404(error_code='contact_group_contact_delete_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = GroupContactDeleteController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        contacts: Optional[QuerySet] = controller.cleaned_data.pop('contacts', None)

        with tracer.start_span('deleting_object', child_of=request.span):
            if contacts is not None and contacts.count() > 0:
                GroupContact.objects.filter(
                    contact__in=contacts,
                    group=group_obj,
                ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
