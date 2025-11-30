# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from contact.models import Group


__all__ = [
    'GroupListController',
    'GroupCreateController',
    'GroupUpdateController',
]


class GroupListController(ControllerBase):
    """
    Validates User data used to list Group records
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


class GroupCreateController(ControllerBase):
    """
    Validates user data used to create Group records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Group
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Group
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_group_create_101'
        if len(name) > self.get_field('name').max_length:
            return 'contact_group_create_102'
        self.cleaned_data['name'] = name
        if Group.objects.filter(name=name, member_id=self.request.user.member['id']).exists():
            return 'contact_group_create_103'
        self.cleaned_data['name'] = name
        return None


class GroupUpdateController(ControllerBase):
    """
    Validates User data used to update a Group
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Group
        validation_order = (
            'name',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Group
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_group_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'contact_group_update_102'
        if Group.objects.filter(
                name=name,
                member_id=self.request.user.member['id'],
        ).exclude(pk=self._instance.pk).exists():
            return 'contact_group_update_103'
        self.cleaned_data['name'] = name
        return None
