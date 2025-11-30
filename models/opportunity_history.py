# libs
from cloudcix_rest.models import BaseModel
from django.db import models
# local
from .opportunity import Opportunity

__all__ = [
    # Opportunity History
    'OpportunityHistory',
]


class OpportunityHistory(BaseModel):
    """
    The OpportunityHistory model represents the information about the opportunities
    """
    EMAIL = 'email'
    NOTE = 'note'
    HISTORY_TYPE_CHOICES = (
        (EMAIL, EMAIL),
        (NOTE, NOTE),
    )

    # Fields
    cc = models.JSONField(null=True)
    heading = models.CharField(max_length=50, blank=True, default='')
    history_type = models.CharField(choices=HISTORY_TYPE_CHOICES, max_length=5)
    message = models.TextField()
    opportunity = models.ForeignKey(Opportunity, related_name='history', on_delete=models.CASCADE)
    reply_to = models.EmailField(max_length=250, null=True)
    to = models.JSONField(null=True)
    user_id = models.IntegerField()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'opportunity_history'

        ordering = ['-created']
