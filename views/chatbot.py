"""
Management for Chatbot
"""
# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from contact.controllers import ChatbotListController, ChatbotCreateController, ChatbotUpdateController
from contact.models import Chatbot
from contact.permissions.chatbot import Permissions
from contact.serializers import ChatbotSerializer


__all__ = [
    'ChatbotCollection',
    'ChatbotResource',
]


class ChatbotCollection(APIView):
    """
    Handles methods regarding Chatbot records that do not require an id to be specified, i.e. list
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Chatbot records

        description: |
            Retrieve a list of the Chatbot records for the requesting User's Member.

        responses:
            200:
                description: A list of the Chatbot records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ChatbotListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('applying_member_filters', child_of=request.span) as span:
            member_filtering: Optional[Q] = None
            if not request.user.robot and request.user.id != 1:
                member_filtering = Q(member_id=request.user.member['id'])

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            try:
                objs = Chatbot.objects.filter(
                    **controller.cleaned_data['search'],
                )

                if member_filtering:
                    objs = objs.filter(member_filtering)

                objs = objs.exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_chatbot_list_001')

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

            data = ChatbotSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Chatbot record

        description: |
            Create a new Chatbot record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: chatbot record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ChatbotCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ChatbotSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class ChatbotResource(APIView):
    """
    Handles methods regarding Chatbot records that do require an id to be specified, i.e. read
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Chatbot record

        description: |
            Attempt to read a Chatbot record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Chatbot record to be read
                type: integer

        responses:
            200:
                description: Chatbot record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_chatbot_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(id=pk, member_id=request.user.member['id'])
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_chatbot_read_001')

        with tracer.start_span('retrieving_chatbot_website_html', child_of=request.span):
            url = ''
            if settings.CHATBOT_URL is not None:
                url = settings.CHATBOT_URL.rstrip('/')
            obj.website_html = render_to_string(
                'contact/chatbot/chatbot_html.txt',
                {
                    'button_background_colour': obj.button_background_colour,
                    'horizontal_percentage': obj.horizontal_percentage,
                    'horizontal_position': obj.horizontal_position,
                    'vertical_percentage': obj.vertical_percentage,
                    'vertical_position': obj.vertical_position,
                    'button_text': obj.button_text,
                    'button_text_colour': obj.button_text_colour,
                    'layout': obj.layout,
                    'name': obj.name,
                    'url': url,
                })

        with tracer.start_span('serializing_data', child_of=request.span):
            data = ChatbotSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Chatbot record
        description: |
            Attempt to update a Chatbot record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Chatbot record to be updated
                type: integer

        responses:
            200:
                description: Chatbot record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_chatbot_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(id=pk, member_id=request.user.member['id'])
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_chatbot_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = ChatbotUpdateController(
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

        with tracer.start_span('refreshing_chatbot_from_db', child_of=request.span):
            # Refresh after saving
            controller.instance.refresh_from_db()

        with tracer.start_span('Serializing_data', child_of=request.span):
            data = ChatbotSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Contact record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified Chatbot record

        description: |
            Attempt to delete a Chatbot record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Chatbot record to be deleted
                type: integer

        responses:
            200:
                description: Chatbot record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_chatbot_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(id=pk, member_id=request.user.member['id'])
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_chatbot_delete_001')

        with tracer.start_span('deleting_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
