"""
Management for Q and A
"""
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
# local
from contact.controllers import QAndACreateController, QAndAListController
from contact.models import Conversation, QAndA, Reference
from contact.permissions.q_and_a import Permissions
from contact.serializers import QAndASerializer
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

__all__ = [
    'QAndACollection',
    'QAndAResource',
]


class QAndACollection(APIView):
    """
    Handles methods regarding QAndA records, i.e. list
    """
    def get(self, request: Request, chatbot_name: str, conversation_id: int) -> Response:
        """
        summary: Retrieve a list of QAndA records

        description: |
            Retrieve a list of the QAndA records for the requesting User's Member.

        path_params:
            chatbot_name:
                description: The name of the Chatbot of the Conversation.
                type: string
            conversation_id:
                description: The id of the Conversation to list QAndA objects for.
                type: integer

        responses:
            200:
                description: A list of the QAndA records, filtered and ordered by the User
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Conversation.objects.get(
                    id=conversation_id,
                    chatbot__name=chatbot_name,
                )
            except Conversation.DoesNotExist:
                return Http404(error_code='contact_q_and_a_list_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.list(request, obj.chatbot)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QAndAListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            objs = QAndA.objects.filter(
                conversation=obj,
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
            data = QAndASerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request, chatbot_name: str, conversation_id: int) -> Response:
        """
        summary: Create a new QAndA record

        description: |
            Create a new QAndA record in the requesting User's Member, using the data supplied by the User.

        path_params:
            chatbot_name:
                description: The name of the Chatbot of the Conversation.
                type: string
            conversation_id:
                description: The id of the conversation record.
                type: integer

        responses:
            201:
                description: QAndA record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER
        # logger = logging.getLogger('contact.views.q_and_a.post')

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Conversation.objects.get(
                    id=conversation_id,
                    chatbot__name=chatbot_name,
                )
            except Conversation.DoesNotExist:
                return Http404(error_code='contact_q_and_a_create_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QAndACreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            references = controller.cleaned_data.pop('references', None)
            controller.instance.conversation = obj
            controller.instance.save()
            controller.instance.refresh_from_db()
            # logger.warning(f'Created QAndA {controller.instance.id} for Conversation {obj.id}')

            # obj.last_message_at = getattr(controller.instance, 'created') or timezone.now()
            # obj.save(update_fields=['last_message_at'])
            # logger.warning(f'Updated Conversation {obj.id} last_message_at to {obj.last_message_at}')

        with tracer.start_span('saving_references', child_of=request.span):
            if references is not None and len(references) > 0:
                Reference.objects.bulk_create(
                    (
                        Reference(
                            hyperlink=link,
                            q_and_a=controller.instance,
                        )
                        for link in references
                    ),
                    ignore_conflicts=True,
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QAndASerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class QAndAResource(APIView):
    """
    Handles methods regarding QAndA records that do require an id to be specified, i.e. read
    """
    def get(self, request: Request, chatbot_name: str, conversation_id: int, pk: int) -> Response:
        """
        summary: Read the details of a specified QAndA record

        description: |
            Attempt to read a QAndA record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            chatbot_name:
                description: The name of the Chatbot of the Conversation.
                type: string
            conversation_id:
                description: The id of the Conversation record
                type: integer
            pk:
                description: The id of the QAndA record to be read
                type: integer

        responses:
            200:
                description: QAndA record was read successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = QAndA.objects.get(
                    id=pk,
                    conversation_id=conversation_id,
                    conversation__chatbot__name=chatbot_name,
                )
            except QAndA.DoesNotExist:
                return Http404(error_code='contact_q_and_a_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, obj.conversation.chatbot)
            if err is not None:
                return err

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QAndASerializer(instance=obj).data

        return Response({'content': data})
