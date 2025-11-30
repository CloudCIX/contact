# stdlib
from typing import List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# local
from ..models import OpportunityHistory

__all__ = [
    'OpportunityHistoryListController',
    'OpportunityHistoryCreateController',
]

HISTORY_TYPE_CHOICES = dict(OpportunityHistory.HISTORY_TYPE_CHOICES)


class OpportunityHistoryListController(ControllerBase):
    """
    Validates User data used to list Opportunity History records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'created',
            'heading',
            'message',
        )


class OpportunityHistoryCreateController(ControllerBase):
    """
    Validates User data used to create a new Opportunity History record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = OpportunityHistory
        validation_order = (
            'heading',
            'history_type',
            'cc',
            'message',
            'reply_to',
            'to',
        )

    def validate_heading(self, heading: Optional[str]) -> Optional[str]:
        """
        description: The Heading of the Opportunity History
        type: string
        required: False
        """
        if heading is None:
            heading = ''

        heading = str(heading).strip()

        if len(heading) > self.get_field('heading').max_length:
            return 'contact_opportunity_history_create_101'

        self.cleaned_data['heading'] = heading
        return None

    def validate_history_type(self, history_type: Optional[str]) -> Optional[str]:
        """
        description: The history_type of Opportunity History
        type: string
        """
        if history_type is None:
            return 'contact_opportunity_history_create_102'

        if history_type not in HISTORY_TYPE_CHOICES:
            return 'contact_opportunity_history_create_103'

        self.cleaned_data['history_type'] = history_type
        return None

    def validate_cc(self, cc: Optional[List[str]]) -> Optional[str]:
        """
        description: array of Email addresses
        type: array
        """
        if 'history_type' not in self.cleaned_data:
            return None
        history_type = self.cleaned_data['history_type']

        if history_type == OpportunityHistory.EMAIL:
            if cc is None:
                cc = []

            if not isinstance(cc, list):
                return 'contact_opportunity_history_create_104'

            for item in cc:
                try:
                    validate_email(item)
                except (ValidationError, TypeError):
                    return 'contact_opportunity_history_create_105'

        self.cleaned_data['cc'] = cc
        return None

    def validate_message(self, message: Optional[str]) -> Optional[str]:
        """
        description: |
            If the history type is a note then this is the notes for the record.
            If the history type is email this is the body of the email.
        type: string
        """
        if message is None:
            return 'contact_opportunity_history_create_106'

        message = str(message).strip()

        if message == '':
            return 'contact_opportunity_history_create_107'

        self.cleaned_data['message'] = message
        return None

    def validate_reply_to(self, reply_to: Optional[str]) -> Optional[str]:
        """
        description: |
            The email address that should be set as reply-to for the email.
            If null the User's email will be used instead.
        type: string
        required: False
        """
        if 'history_type' not in self.cleaned_data:
            return None

        history_type = self.cleaned_data['history_type']

        if history_type == OpportunityHistory.EMAIL:
            if not reply_to:
                reply_to = self.request.user.email
            try:
                validate_email(reply_to)
            except (ValidationError, TypeError):
                return 'contact_opportunity_history_create_108'

        self.cleaned_data['reply_to'] = reply_to
        return None

    def validate_to(self, to: Optional[List[str]]) -> Optional[str]:
        """
        description: A list of email addresses, required if the history type is "email".
        type: array
        """
        if 'history_type' not in self.cleaned_data:
            return None

        history_type = self.cleaned_data['history_type']

        if history_type == OpportunityHistory.EMAIL:
            if to is None:
                to = []
            if not isinstance(to, list):
                return 'contact_opportunity_history_create_109'
            if len(to) == 0:
                return 'contact_opportunity_history_create_110'
            for item in to:
                try:
                    validate_email(item)
                except (ValidationError, TypeError):
                    return 'contact_opportunity_history_create_111'

        self.cleaned_data['to'] = to
        return None
