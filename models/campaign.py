# stdlib
from datetime import datetime
from typing import List
# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse
# local
from .contact import Contact
from .campaign_contact import CampaignContact


__all__ = [
    # Campaign
    'Campaign',
]


class Campaign(BaseModel):
    """
    The Campaign model represents the newest campaigns
    """

    # Fields
    contacts = models.ManyToManyField(Contact, through=CampaignContact, related_name='campaigns')
    date_of_campaign = models.DateField(blank=True)
    description = models.TextField()
    member_id = models.IntegerField()
    name = models.CharField(max_length=50)

    # objects = CampaignManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'campaign'
        indexes = [
            models.Index(fields=['date_of_campaign'], name='campaign_date_of_campaign'),
            models.Index(fields=['id'], name='campaign_id'),
            models.Index(fields=['member_id'], name='campaign_member_id'),
            models.Index(fields=['name'], name='campaign_name'),
        ]

        ordering = ['name']

    @property
    def contact_ids(self) -> List[int]:
        """
        Returns a List of IDs for the contacts in the Campaign
        """
        return list(self.contacts.values_list('id', flat=True))

    @property
    def total_contacts(self) -> int:
        """
        The total number of Contacts in the Campaign.
        """
        return self.contacts.count()

    @property
    def total_responses(self) -> int:
        """
        The total number of responses in the Campaign.
        """
        return self.campaigncontact_set.filter(responded=True).count()

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the CampaignResource view for this Campaign record
        :return: A URL that corresponds to the views for this Campaign record
        """
        return reverse('campaign_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Campaign instance, and clear the group_contacts associated it
        """
        self.contacts.clear()
        self.deleted = datetime.utcnow()
        self.save()
