# stdlib
from typing import List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from ..models import CampaignContact, Contact


__all__ = [
    'CampaignContactCreateController',
    'CampaignContactUpdateController',
    'CampaignContactDeleteController',
]


class CampaignContactCreateController(ControllerBase):
    """
    Validates User data used to create a new CampaignContact record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = CampaignContact
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
        contacts = contacts or []
        if not isinstance(contacts, list):
            return 'contact_campaign_contact_create_101'

        if len(contacts) == 0:
            return 'contact_campaign_contact_create_102'

        for contact_id in contacts:
            if not isinstance(contact_id, int):
                return 'contact_campaign_contact_create_103'

        objs = Contact.objects.filter(id__in=contacts, member_id=self.request.user.member['id'])

        if len(contacts) != len(objs):
            return 'contact_campaign_contact_create_104'

        self.cleaned_data['contacts'] = objs
        return None


class CampaignContactUpdateController(ControllerBase):
    """
    Validates User data used to update a new CampaignContact record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = CampaignContact
        validation_order = (
            'contacts',
            'responded',
        )

    def validate_contacts(self, contacts: Optional[List[int]]) -> Optional[str]:
        """
        description: An array of contact ids
        type: array
        items:
            type: integers
        """
        contacts = contacts or []
        if not isinstance(contacts, list):
            return 'contact_campaign_contact_update_101'

        if len(contacts) == 0:
            return 'contact_campaign_contact_update_102'

        for contact_id in contacts:
            if not isinstance(contact_id, int):
                return 'contact_campaign_contact_update_103'

        objs = Contact.objects.filter(id__in=contacts, member_id=self.request.user.member['id'])

        if len(contacts) != len(objs):
            return 'contact_campaign_contact_update_104'

        self.cleaned_data['contacts'] = objs
        return None

    def validate_responded(self, responded: Optional[bool]) -> Optional[str]:
        """
        description: It indicates if the contacts have responded to the campagin.
        required: False
        type: Boolean
        """
        if responded is None:
            return None
        if not isinstance(responded, bool):
            return 'contact_campaign_contact_update_105'
        self.cleaned_data['responded'] = responded
        return None


class CampaignContactDeleteController(ControllerBase):
    """
    Validates User data used to create a new CampaignContact record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = CampaignContact
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
        contacts = contacts or []
        if not isinstance(contacts, list):
            return 'contact_campaign_contact_delete_101'

        if len(contacts) == 0:
            return 'contact_campaign_contact_delete_102'

        for contact_id in contacts:
            if not isinstance(contact_id, int):
                return 'contact_campaign_contact_delete_103'

        objs = Contact.objects.filter(id__in=contacts, member_id=self.request.user.member['id'])

        if len(contacts) != len(objs):
            return 'contact_campaign_contact_delete_104'

        self.cleaned_data['contacts'] = objs
        return None
