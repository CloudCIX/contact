# stdlib
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from ..models import Contact, Conversation


__all__ = [
    'ConversationListController',
    'ConversationCreateController',
]


class ConversationListController(ControllerBase):
    """
    Validates User data used to list Conversation records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'created',
            'name',
        )
        search_fields = {
            'contact_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'cookie': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class ConversationCreateController(ControllerBase):
    """
    Validates user data used to create Conversation records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Conversation
        validation_order = (
            'contact_id',
            'cookie',
            'name',
        )

    def validate_contact_id(self, contact_id: Optional[int]) -> Optional[str]:
        """
        description: The Contact ID of the Conversation
        type: integer
        """
        if contact_id is None:
            return None

        try:
            contact_id = int(contact_id)
        except (TypeError, ValueError):
            return 'contact_conversation_create_101'

        try:
            contact = Contact.objects.get(
                pk=contact_id,
                member_id=self.kwargs['member_id'],
            )
        except Contact.DoesNotExist:
            return 'contact_conversation_create_102'

        self.cleaned_data['contact'] = contact
        return None

    def validate_cookie(self, cookie: Optional[str]) -> Optional[str]:
        """
        description: The unique identifier of a guest mode user
        type: string
        required: False
        """
        if cookie is None:
            # If contact is not in the cleansed data or errors, it was not sent.
            # Both contact_id and cookie cannot be None
            if 'contact' not in self.cleaned_data and 'contact_id' not in self._errors:
                return 'contact_conversation_create_103'
            return None

        cookie = cookie.strip()
        if len(cookie) == 0:
            return None

        if len(cookie) > self.get_field('cookie').max_length:
            return 'contact_conversation_create_104'

        self.cleaned_data['cookie'] = cookie
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Conversation
        type: string
        """
        if name is None:
            return 'contact_conversation_create_105'

        if len(name) > self.get_field('name').max_length:
            return 'contact_conversation_create_106'

        self.cleaned_data['name'] = name
        return None
