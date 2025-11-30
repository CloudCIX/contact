"""
Management for Contact
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
    ContactCreateController,
    ContactListController,
    ContactUpdateController,
)
from contact.models import Contact, Chatbot
from contact.permissions.contact import Permissions
from contact.serializers import ContactSerializer

__all__ = [
    'ContactCollection',
    'ContactResource',
]


class ContactCollection(APIView):
    """
    Handles methods regarding Contact records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Contact records

        description: |
            Retrieve a list of the Contact records for the requesting User's Member.

        responses:
            200:
                description: A list of the Contact records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ContactListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('setting_member_id_search_param', child_of=request.span) as span:
            search_filters = controller.cleaned_data['search']
            chatbot_name = search_filters.pop('chatbot_name', None)
            member_id = request.user.member['id']
            if chatbot_name is not None and request.user.robot:
                try:
                    member_id = Chatbot.objects.values_list('member_id', flat=True).get(name=chatbot_name)
                except Chatbot.DoesNotExist:
                    return Http400(error_code='contact_contact_list_001')

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            try:
                objs = Contact.list_objects.filter(
                    member_id=member_id,
                    **search_filters,
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_contact_list_002')

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

            data = ContactSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Contact record

        description: |
            Create a new Contact record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Contact record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ContactCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, controller.instance)
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ContactSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class ContactResource(APIView):
    """
    Handles methods regarding Contact records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Contact record

        description: |
            Attempt to read a Contact record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Contact record to be read
                type: integer

        responses:
            200:
                description: Contact record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_contact_object', child_of=request.span):
            try:
                obj = Contact.objects.get(id=pk)
            except Contact.DoesNotExist:
                return Http404(error_code='contact_contact_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ContactSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Contact record
        description: |
            Attempt to update a Contact record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Contact record to be updated
                type: integer

        responses:
            200:
                description: Contact record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_contact_object', child_of=request.span):
            try:
                obj = Contact.objects.get(id=pk)
            except Contact.DoesNotExist:
                return Http404(error_code='contact_contact_update_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request, obj)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ContactUpdateController(
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
            data = ContactSerializer(instance=controller.instance).data
        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Contact record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Contact record

        description: |
            Attempt to delete a Contact record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Contact record to delete
                type: integer

        responses:
            204:
                description: Contact record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_contact_object', child_of=request.span):
            try:
                obj = Contact.objects.get(id=pk, member_id=request.user.member['id'])
            except Contact.DoesNotExist:
                return Http404(error_code='contact_contact_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
