from django.db import models

__all__ = [
    # Campaign Contact
    'CampaignContact',
]


class CampaignContact(models.Model):

    # Fields
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    responded = models.BooleanField(default=False)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'campaign_contact'

        indexes = [
            models.Index(fields=['responded'], name='campaign_contact_responded'),
        ]

        unique_together = ('campaign', 'contact')
