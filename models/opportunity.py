# stdlib
from datetime import datetime
from typing import List
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .contact import Contact
from .opportunity_contact import OpportunityContact

__all__ = [
    # Opportunity
    'Opportunity',
]


class OpportunityManager(BaseManager):
    """
    Manager for Opportunity class which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'history',
        )


class Opportunity(BaseModel):
    """
    The Opportunity model represents the opportunities with regards to new clients
    """

    # Fields
    closed = models.BooleanField(default=False)
    contacts = models.ManyToManyField(Contact, through=OpportunityContact, related_name='opportunities')
    description = models.TextField()
    member_id = models.IntegerField()
    name = models.CharField(max_length=50)
    outcome = models.TextField()
    probability = models.DecimalField(max_digits=5, decimal_places=2)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    objects = OpportunityManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'opportunity'
        indexes = [
            models.Index(fields=['closed'], name='opportunity_closed'),
            models.Index(fields=['created'], name='opportunity_created'),
            models.Index(fields=['id'], name='opportunity_id'),
            models.Index(fields=['name'], name='opportunity_name'),
            models.Index(fields=['member_id'], name='opportunity_member_id'),
            models.Index(fields=['probability'], name='opportunity_probability'),
            models.Index(fields=['value'], name='opportunity_value'),
        ]

        ordering = ['name']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the OpportunityResource view for this Opportunity record
        :return: A URL that corresponds to the views for this Opportunity record
        """
        return reverse('opportunity_resource', kwargs={'pk': self.pk})

    @property
    def contact_ids(self) -> List[int]:
        """
        Returns a List of IDs for the contacts in the Opportunity
        """
        return list(self.contacts.values_list('id', flat=True))

    @property
    def total_contacts(self) -> str:
        """
        The total number of Contacts in the Opportunity
        """
        return self.contacts.count()

    def cascade_delete(self):
        """
        Delete the Opportunity Class, and delete the history records that are related to it
        """
        deltime = datetime.utcnow()
        self.history.all().update(deleted=deltime)
        self.contacts.clear()
        self.deleted = deltime
        self.save()
