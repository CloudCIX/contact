# stdlib
from typing import List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from ..models import Contact, GroupContact

__all__ = [
    'GroupContactCreateController',
    'GroupContactDeleteController',
]


class GroupContactCreateController(ControllerBase):
    """
    Validates User data used to create a new Group Contact record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = GroupContact
        validation_order = (
            'contacts',
        )

    def validate_contacts(self, contacts: Optional[List[int]]) -> Optional[str]:
        """
        description: An array of contact ids
        type: array
        items:
            type: integers
        """
        if contacts is None:
            return 'contact_group_contact_create_101'

        if not isinstance(contacts, list):
            return 'contact_group_contact_create_102'

        for contact_id in contacts:
            if not isinstance(contact_id, int):
                return 'contact_group_contact_create_103'

        contact_objs = Contact.objects.filter(
            id__in=contacts,
            member_id=self.request.user.member['id'],
        )

        if len(contact_objs) != len(contacts):
            return 'contact_group_contact_create_104'

        self.cleaned_data['contacts'] = contact_objs
        return None


class GroupContactDeleteController(ControllerBase):
    """
    Validates User data used to delete an Group Contact record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = GroupContact
        validation_order = (
            'contacts',
        )

    def validate_contacts(self, contacts: Optional[List[int]]) -> Optional[str]:
        """
        description: An array of contact ids
        type: array
        items:
            type: integers
        """
        if contacts is None:
            return 'contact_group_contact_delete_101'

        if not isinstance(contacts, list):
            return 'contact_group_contact_delete_102'

        for contact_id in contacts:
            if not isinstance(contact_id, int):
                return 'contact_group_contact_delete_103'

        contact_objs = Contact.objects.filter(
            id__in=contacts,
            member_id=self.request.user.member['id'],
        )

        if len(contact_objs) != len(contacts):
            return 'contact_group_contact_delete_104'

        self.cleaned_data['contacts'] = contact_objs
        return None
