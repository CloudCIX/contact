# stdlib
from datetime import datetime
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from contact.models import Campaign


__all__ = [
    'CampaignListController',
    'CampaignCreateController',
    'CampaignUpdateController',
]


class CampaignListController(ControllerBase):
    """
    Validates User data used to list Campaign records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'date_of_campaign',
            'id',
        )
        search_fields = {
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'date_of_campaign': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class CampaignCreateController(ControllerBase):
    """
    Validates user data used to create Campaign records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Campaign
        validation_order = (
            'date_of_campaign',
            'description',
            'name',
        )

    def validate_date_of_campaign(self, campaign_date: Optional[str]) -> Optional[str]:
        """
        description: The date of the Campaign
        type: string
        """
        try:
            date_of_campaign = datetime.strptime(str(campaign_date).split('T')[0], '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return 'contact_campaign_create_101'
        self.cleaned_data['date_of_campaign'] = date_of_campaign
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Campaign
        required: false
        type: string
        """
        self.cleaned_data['description'] = str(description).strip() if description else ''
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Campaign
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_campaign_create_102'
        if len(name) > self.get_field('name').max_length:
            return 'contact_campaign_create_103'
        if Campaign.objects.filter(name=name, member_id=self.request.user.member['id']).exists():
            return 'contact_campaign_create_104'
        self.cleaned_data['name'] = name
        return None


class CampaignUpdateController(ControllerBase):
    """
    Validates user data used to update Campaign records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Campaign
        validation_order = (
            'date_of_campaign',
            'description',
            'name',
        )

    def validate_date_of_campaign(self, campaign_date: Optional[str]) -> Optional[str]:
        """
        description: The date of the Campaign
        type: string
        """
        try:
            date_of_campaign = datetime.strptime(str(campaign_date).split('T')[0], '%Y-%m-%d').date()
        except (TypeError, ValueError):
            return 'contact_campaign_update_101'
        self.cleaned_data['date_of_campaign'] = date_of_campaign
        return None

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Campaign
        required: false
        type: string
        """
        self.cleaned_data['description'] = str(description).strip() if description else ''
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Campaign
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_campaign_update_102'
        if len(name) > self.get_field('name').max_length:
            return 'contact_campaign_update_103'
        if Campaign.objects.filter(
            name=name,
            member_id=self.request.user.member['id'],
        ).exclude(pk=self._instance.pk).exists():
            return 'contact_campaign_update_104'
        self.cleaned_data['name'] = name
        return None
