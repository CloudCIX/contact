"""
Management for Conversation
"""
# stdlib
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import (
    ConversationListController,
    ConversationCreateController,
)
from contact.models import Chatbot, Conversation
from contact.permissions.conversation import Permissions
from contact.serializers import ConversationSerializer

__all__ = [
    'ConversationCollection',
    'ConversationResource',
]


class ConversationCollection(APIView):
    """
    Handles methods regarding Conversation records that do not require an id to be specified, i.e. list
    """

    def get(self, request: Request, chatbot_name: str) -> Response:
        """
        summary: Retrieve a list of Conversation records

        description: |
            Retrieve a list of the Conversation records for the specified Chatbot.

        path_params:
            chatbot_name:
                description: The name of the Chatbot to list Conversations for
                type: string

        responses:
            200:
                description: A list of the Conversation records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(name=chatbot_name)
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_conversation_list_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.list(request, obj)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ConversationListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Conversation.objects.filter(
                    chatbot=obj,
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_conversation_list_002')

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
            data = ConversationSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request, chatbot_name: str) -> Response:
        """
        summary: Create a new Conversation record

        description: |
            Create a new Conversation record in the requesting User's Member, using the data supplied by the User.

        path_params:
            chatbot_name:
                description: The name of the Chatbot to create a Conversation for
                type: string

        responses:
            201:
                description: Conversation record was created successfully
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(name=chatbot_name)
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_conversation_create_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ConversationCreateController(data=request.data, request=request, span=span)
            controller.kwargs = {'member_id': obj.member_id}
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.chatbot = obj
            controller.instance.last_message_at = timezone.now()
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ConversationSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class ConversationResource(APIView):
    """
    Handles methods regarding Conversation records that do require an id to be specified, i.e. read
    """

    def get(self, request: Request, chatbot_name: str, pk: int) -> Response:
        """
        summary: Read the details of a specified Conversation record

        description: |
            Attempt to read a Conversation record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            chatbot_name:
                description: The name of the Chatbot to read a Conversation for
                type: string
            pk:
                description: The id of the Conversation record to be read
                type: integer

        responses:
            200:
                description: Conversation record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_conversation_object', child_of=request.span):
            try:
                obj = Conversation.objects.get(id=pk, chatbot__name=chatbot_name)
            except Conversation.DoesNotExist:
                return Http404(error_code='contact_conversation_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ConversationSerializer(instance=obj).data

        return Response({'content': data})

    def delete(self, request: Request, chatbot_name: str, pk: int):
        """
        summary: Delete a specified Conversation record

        description: |
            Attempt to delete a Conversation record by the given 'pk', returning a 404 if it does not exist

        path_params:
            chatbot_name:
                description: The name of the Chatbot to read a Conversation for
                type: string
            pk:
                description: The id of the Conversation record to delete
                type: integer

        responses:
            204:
                description: Conversation record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_conversation_object', child_of=request.span):
            try:
                obj = Conversation.objects.get(id=pk, chatbot__name=chatbot_name)
            except Conversation.DoesNotExist:
                return Http404(error_code='contact_conversation_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
