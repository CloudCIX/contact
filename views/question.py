"""
Management for Question
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
from ..controllers import QuestionListController, QuestionCreateController, QuestionUpdateController
from ..permissions.question import Permissions
from ..serializers import QuestionSerializer
from contact.models import Question, QuestionTranslation

__all__ = [
    'QuestionCollection',
    'QuestionResource',
]


class QuestionCollection(APIView):
    """
    Handles methods regarding Question records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Question records

        description: |
            Retrieve a list of the Question records for the requesting User's Member.

        responses:
            200:
                description: A list of the Question records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = Question.objects.filter(
                    question_set__member_id__in=[0, request.user.member['id']],
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_question_list_001')

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
            data = QuestionSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Question record

        description: |
            Create a new Question record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Question record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request, controller.cleaned_data['question_set'])
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            translations = controller.cleaned_data.pop('question_translations')
            controller.instance.save()

        with tracer.start_span('refreshing_question_from_db', child_of=request.span):
            # Refresh after saving
            controller.instance.refresh_from_db()

        with tracer.start_span('saving_translation_object', child_of=request.span):
            # Set Required Values and save validated translations
            for item in translations:
                QuestionTranslation.objects.create(
                    question_id=controller.instance,
                    **item,
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QuestionSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class QuestionResource(APIView):
    """
    Handles methods regarding Question records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Question record

        description: |
            Attempt to read a Question record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Question record to be read
                type: integer

        responses:
            200:
                description: Question record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Question.objects.get(
                    id=pk,
                    question_set__member_id__in=[0, request.user.member['id']],
                )
            except Question.DoesNotExist:
                return Http404(error_code='contact_question_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QuestionSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Question record
        description: |
            Attempt to update a Question record in the requesting User's Member by the given 'pk',
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Question record to be updated
                type: integer

        responses:
            200:
                description: Question record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_question_object', child_of=request.span):
            try:
                obj = Question.objects.get(id=pk, question_set__member_id__in=[0, request.user.member['id']])
            except Question.DoesNotExist:
                return Http404(error_code='contact_question_update_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request, obj)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionUpdateController(
                data=request.data,
                instance=obj,
                partial=partial,
                request=request,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            translations = controller.cleaned_data.pop('question_translations')
            controller.instance.save()

        with tracer.start_span('delete_existing_translation_object', child_of=request.span):
            # Set deleted translation to current time for existing translations
            obj.question_translations.all().update(deleted=datetime.now())
            # Refresh after deleting
            controller.instance.refresh_from_db()

        with tracer.start_span('saving_translation_object', child_of=request.span):
            # create new validated translations
            for item in translations:
                QuestionTranslation.objects.create(
                    question_id=controller.instance,
                    **item,
                )

        with tracer.start_span('Serializing_data', child_of=request.span):
            data = QuestionSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Question record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Question record

        description: |
            Attempt to delete a Question record in the requesting User's Member by the given 'pk',
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Question record to delete
                type: integer

        responses:
            204:
                description: Question record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_question_set_object', child_of=request.span):
            try:
                obj = Question.objects.get(id=pk, question_set__member_id__in=[0, request.user.member['id']])
            except Question.DoesNotExist:
                return Http404(error_code='contact_question_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('cascade_delete_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
