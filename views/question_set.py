"""
Management for Question Set
"""
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from ..controllers import QuestionSetListController, QuestionSetCreateController, QuestionSetUpdateController
from ..serializers import QuestionSetSerializer
from contact.models import QuestionSet

__all__ = [
    'QuestionSetCollection',
    'QuestionSetResource',
]


class QuestionSetCollection(APIView):
    """
    Handles methods regarding Question Set records that do not require an id to be specified, i.e. list, create
    """
    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Question Set records

        description: |
            Retrieve a list of the Question set records for the requesting User's Member.

        responses:
            200:
                description: A list of the Question Set records, filtered and ordered by the User
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionSetListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('get_objects', child_of=request.span):
            try:
                objs = QuestionSet.objects.filter(
                    member_id__in=[0, request.user.member['id']],
                    **controller.cleaned_data['search'],
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    controller.cleaned_data['order'],
                )
            except (ValueError, ValidationError):
                return Http400(error_code='contact_question_set_list_001')

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
            data = QuestionSetSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Question Set record

        description: |
            Create a new Question Set record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Question Set record was created successfully
            400: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionSetCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QuestionSetSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class QuestionSetResource(APIView):
    """
    Handles methods regarding QuestionSet records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified QuestionSet record

        description: |
            Attempt to read a QuestionSet record in the requesting User's Member by the given 'pk', returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the QuestionSet record to be read
                type: integer

        responses:
            200:
                description: QuestionSet record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_question_set_object', child_of=request.span):
            try:
                obj = QuestionSet.objects.get(id=pk, member_id__in=[0, request.user.member['id']])
            except QuestionSet.DoesNotExist:
                return Http404(error_code='contact_question_set_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = QuestionSetSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Question Set record

        description: |
            Attempt to update a Question Set record in the requesting User's Member by the given 'pk',
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Question Set record to be updated
                type: integer

        responses:
            200:
                description: Question Set record was updated successfully
            400: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_question_set_object', child_of=request.span):
            try:
                obj = QuestionSet.objects.get(id=pk, member_id__in=[0, request.user.member['id']])
            except QuestionSet.DoesNotExist:
                return Http404(error_code='contact_question_set_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = QuestionSetUpdateController(
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
            data = QuestionSetSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a Question Set record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Question Set record

        description: |
            Attempt to delete a Question Set record in the requesting User's Member by the given 'pk',
            returning a 404 if it does not exist

        path_params:
            pk:
                description: The id of the Question Set record to delete
                type: integer

        responses:
            204:
                description: Question Set record was deleted successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_question_set_object', child_of=request.span):
            try:
                obj = QuestionSet.objects.get(id=pk, member_id=request.user.member['id'])
            except QuestionSet.DoesNotExist:
                return Http404(error_code='contact_question_set_delete_001')

        with tracer.start_span('cascade_delete_object', child_of=request.span):
            obj.cascade_delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
