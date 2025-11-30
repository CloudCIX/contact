# stdlib
from collections import deque
from typing import Any, Dict, Deque, List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
from cloudcix.api import Membership
# local
from ..models import Question, QuestionSet

__all__ = [
    'QuestionListController',
    'QuestionCreateController',
    'QuestionUpdateController',
]


class QuestionListController(ControllerBase):
    """
    Validates User data used to list Question records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'id',
        )
        search_fields = {
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'question_set_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'question_set__member_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'question_set__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class QuestionCreateController(ControllerBase):
    """
    Validates user data used to create Question records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Question
        validation_order = (
            'question_set_id',
            'question_translations',
        )

    def validate_question_set_id(self, question_set_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the QuestionSet that the question belongs to
        type: integer
        """
        if question_set_id is None:
            return 'contact_question_create_101'

        try:
            question_set_id = int(question_set_id)
        except (ValueError, TypeError):
            return 'contact_question_create_102'

        try:
            obj = QuestionSet.objects.get(pk=question_set_id, member_id__in=[0, self.request.user.member['id']])
        except QuestionSet.DoesNotExist:
            return 'contact_question_create_103'

        self.cleaned_data['question_set'] = obj
        return None

    def validate_question_translations(self, question_translations: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """
        description: A list of question_translation objects for the intended question
        type: array
        items:
            type: object
            properties:
                answer:
                    description: Expected answer to be given based on the question asked and the chunk provided
                    type: string
                chunk:
                    description: Paragraph in which the answer to the question should be contained
                    type: string
                language_id:
                    description: The id of language of the question
                    type: integer
                question:
                    description: The question provided by the user
                    type: string
        """
        question_translations = question_translations or []
        if not isinstance(question_translations, list):
            return 'contact_question_create_104'
        if len(question_translations) == 0:
            return 'contact_question_create_105'
        results: Deque = deque()
        for i, item in enumerate(question_translations):
            if not isinstance(item, dict):
                return 'contact_question_create_106'

            answer = item.get('answer', None)
            if answer is None:
                answer = ''
            answer = str(answer).strip()
            if len(answer) == 0:
                return 'contact_question_create_107'
            chunk = item.get('chunk', None)
            if chunk is None:
                chunk = ''
            chunk = str(chunk).strip()
            if len(chunk) == 0:
                return 'contact_question_create_108'
            language_id = item.get('language_id', None)
            if language_id is None:
                return 'contact_question_create_109'
            try:
                language_id = int(language_id)
            except (ValueError, TypeError):
                return 'contact_question_create_110'

            response = Membership.language.read(
                pk=language_id,
                token=self.request.user.token,
                span=self.span,
            )
            if response.status_code != 200:
                return 'contact_question_create_111'

            question = item.get('question', None)
            if question is None:
                question = ''
            question = str(question).strip()
            if len(question) == 0:
                return 'contact_question_create_112'
            results.append(
                {
                    'answer': answer,
                    'chunk': chunk,
                    'language_id': language_id,
                    'question': question,
                },
            )
        self.cleaned_data['question_translations'] = results
        return None


class QuestionUpdateController(ControllerBase):
    """
    Validates user data used to Update Question records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Question
        validation_order = (
            'question_translations',
        )

    def validate_question_translations(self, question_translations: Optional[List[Dict[str, Any]]]) -> Optional[str]:
        """
        description: A list of question_translation objects for the intended question
        type: array
        items:
            type: object
            properties:
                answer:
                    description: Expected answer to be given based on the question asked and the chunk provided
                    type: string
                chunk:
                    description: Paragraph in which the answer to the question should be contained
                    type: string
                language_id:
                    description: The id of language of the question
                    type: integer
                question:
                    description: The question provided by the user
                    type: string
        """
        question_translations = question_translations or []
        if not isinstance(question_translations, list):
            return 'contact_question_update_101'
        if len(question_translations) == 0:
            return 'contact_question_update_102'
        results: Deque = deque()
        for i, item in enumerate(question_translations):
            if not isinstance(item, dict):
                return 'contact_question_update_103'

            answer = item.get('answer', None)
            if answer is None:
                answer = ''
            answer = str(answer).strip()
            if len(answer) == 0:
                return 'contact_question_update_104'
            chunk = item.get('chunk', None)
            if chunk is None:
                chunk = ''
            chunk = str(chunk).strip()
            if len(chunk) == 0:
                return 'contact_question_update_105'
            language_id = item.get('language_id', None)
            if language_id is None:
                return 'contact_question_update_106'
            try:
                language_id = int(language_id)
            except (ValueError, TypeError):
                return 'contact_question_update_107'

            response = Membership.language.read(
                pk=language_id,
                token=self.request.user.token,
                span=self.span,
            )
            if response.status_code != 200:
                return 'contact_question_update_108'

            question = item.get('question', None)
            if question is None:
                question = ''
            question = str(question).strip()
            if len(question) == 0:
                return 'contact_question_update_109'
            results.append(
                {
                    'answer': answer,
                    'chunk': chunk,
                    'language_id': language_id,
                    'question': question,
                },
            )
        self.cleaned_data['question_translations'] = results
        return None
