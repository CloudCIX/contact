# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from ..models import QuestionSet

__all__ = [
    'QuestionSetListController',
    'QuestionSetCreateController',
    'QuestionSetUpdateController',
]


class QuestionSetListController(ControllerBase):
    """
    Validates User data used to list Question Set records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'id',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class QuestionSetCreateController(ControllerBase):
    """
    Validates user data used to create Question Set records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = QuestionSet
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Question Set
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_question_set_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'contact_question_set_create_102'
        if QuestionSet.objects.filter(name=name, member_id__in=[0, self.request.user.member['id']]).exists():
            return 'contact_question_set_create_103'
        self.cleaned_data['name'] = name
        return None


class QuestionSetUpdateController(ControllerBase):
    """
    Validates user data used to update Question Set records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = QuestionSet
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Question Set
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_question_set_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'contact_question_set_update_102'
        if QuestionSet.objects.filter(
                name=name,
                member_id__in=[0, self.request.user.member['id']],
        ).exclude(pk=self._instance.pk).exists():
            return 'contact_question_set_update_103'
        self.cleaned_data['name'] = name
        return None
