# stdlib
from typing import List, Optional
from urllib.parse import urlparse
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from ..models import QAndA

__all__ = [
    'QAndAListController',
    'QAndACreateController',
]


class QAndAListController(ControllerBase):
    """
    Validates User data used to list QAndA records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'created',
        )


class QAndACreateController(ControllerBase):
    """
    Validates user data used to create QAndA records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = QAndA
        validation_order = (
            'answer',
            'question',
            'references',
        )

    def validate_answer(self, answer: Optional[str]) -> Optional[str]:
        """
        description: The answer the chatbot gave to the contacts question.
        type: string
        """
        if answer is None:
            return 'contact_q_and_a_create_101'

        answer = str(answer).strip()

        if len(answer) == 0:
            return 'contact_q_and_a_create_102'

        self.cleaned_data['answer'] = answer
        return None

    def validate_question(self, question: Optional[str]) -> Optional[str]:
        """
        description: The question the contact asked the chatbot.
        type: string
        """
        if question is None:
            return 'contact_q_and_a_create_103'

        question = str(question).strip()

        if len(question) == 0:
            return 'contact_q_and_a_create_104'

        self.cleaned_data['question'] = question
        return None

    def validate_references(self, references: Optional[List[str]]) -> Optional[str]:
        """
        description: An array of URLs
        type: array
        """
        if references is None:
            return None

        if not isinstance(references, list):
            return 'contact_q_and_a_create_105'

        for item in references:
            url = urlparse(item)
            if not all([url.scheme, url.netloc]):
                return 'contact_q_and_a_create_106'

        self.cleaned_data['references'] = references
        return None
