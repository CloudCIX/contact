# stdlib
from decimal import Decimal, InvalidOperation
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from contact.models import Opportunity

__all__ = [
    'OpportunityListController',
    'OpportunityCreateController',
    'OpportunityUpdateController',
]


class OpportunityListController(ControllerBase):
    """
    Validates User data used to list Opportunity records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'closed',
            'created',
            'id',
            'probability',
            'updated',
            'value',
        )
        search_fields = {
            'closed': (),
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'description': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'date': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'outcome': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'probability': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'value': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class OpportunityCreateController(ControllerBase):
    """
    Validates user data used to create Opportunity records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Opportunity
        validation_order = (
            'description',
            'name',
            'outcome',
            'probability',
            'closed',
            'value',
        )

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Opportunity
        type: string
        """
        if description is None:
            description = ''
        description = str(description).strip()
        if len(description) == 0:
            return 'contact_opportunity_create_101'
        self.cleaned_data['description'] = description
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Opportunity
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_opportunity_create_102'
        if len(name) > self.get_field('name').max_length:
            return 'contact_opportunity_create_103'
        self.cleaned_data['name'] = name
        return None

    def validate_outcome(self, outcome: Optional[str]) -> Optional[str]:
        """
        description: The outcome of the Opportunity
        type: string
        """
        self.cleaned_data['outcome'] = str(outcome).strip() if outcome else ''
        return None

    def validate_probability(self, probability: Optional[Decimal]) -> Optional[str]:
        """
        description: The probability of the Opportunity's success
        type: string
        format: decimal
        """
        try:
            probability = Decimal(str(probability))
        except InvalidOperation:
            return 'contact_opportunity_create_104'
        if probability < 0 or probability > 100:
            return 'contact_opportunity_create_105'
        self.cleaned_data['probability'] = probability
        return None

    def validate_closed(self, closed: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if opportunity is closed
        type: boolean
        """
        if not isinstance(closed, bool):
            return 'contact_opportunity_create_106'
        if 'probability' not in self.cleaned_data:
            return None
        if closed is True:
            p = self.cleaned_data['probability']
            if p != 0 or p != 100:
                return 'contact_opportunity_create_107'
        self.cleaned_data['closed'] = closed
        return None

    def validate_value(self, value: Optional[Decimal]) -> Optional[str]:
        """
        description: The monetary value of the opportunity.
        type: string
        format: decimal
        """
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_opportunity_create_108'
        self.cleaned_data['value'] = value
        return None


class OpportunityUpdateController(ControllerBase):
    """
    Validates user data used to update Opportunity records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Opportunity
        validation_order = (
            'description',
            'name',
            'outcome',
            'probability',
            'closed',
            'value',
        )

    def validate_description(self, description: Optional[str]) -> Optional[str]:
        """
        description: The description of the Opportunity
        type: string
        """
        if description is None:
            description = ''
        description = str(description).strip()
        if len(description) == 0:
            return 'contact_opportunity_update_101'
        self.cleaned_data['description'] = description
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Opportunity
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_opportunity_update_102'
        if len(name) > self.get_field('name').max_length:
            return 'contact_opportunity_update_103'
        self.cleaned_data['name'] = name
        return None

    def validate_outcome(self, outcome: Optional[str]) -> Optional[str]:
        """
        description: The outcome of the Opportunity
        type: string
        """
        self.cleaned_data['outcome'] = str(outcome).strip() if outcome else ''
        return None

    def validate_probability(self, probability: Optional[Decimal]) -> Optional[str]:
        """
        description: The probability of the Opportunity's success
        type: string
        format: decimal
        """
        if self._instance.closed:
            return None
        try:
            probability = Decimal(str(probability))
        except InvalidOperation:
            return 'contact_opportunity_update_104'
        if probability < 0 or probability > 100:
            return 'contact_opportunity_update_105'
        self.cleaned_data['probability'] = probability
        return None

    def validate_closed(self, closed: Optional[bool]) -> Optional[str]:
        """
        description: Flag stating if opportunity is closed
        type: boolean
        """
        if not isinstance(closed, bool):
            return 'contact_opportunity_update_106'
        probability = self.cleaned_data.get('probability', self._instance.probability)
        if closed is True:
            if 0 < probability < 100:
                return 'contact_opportunity_update_107'
        self.cleaned_data['closed'] = closed
        return None

    def validate_value(self, value: Optional[Decimal]) -> Optional[str]:
        """
        description: The monetary value of the opportunity.
        type: string
        format: decimal
        """
        try:
            value = Decimal(str(value))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_opportunity_update_108'
        self.cleaned_data['value'] = value
        return None
