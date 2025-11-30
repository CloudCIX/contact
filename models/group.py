# stdlib
from datetime import datetime
from typing import List
# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse
# local
from .contact import Contact
from .group_contact import GroupContact

__all__ = [
    # Group
    'Group',
]


class Group(BaseModel):
    """
    The Group model represents the groups
    """

    # Fields
    contacts = models.ManyToManyField(Contact, through=GroupContact, related_name='groups')
    member_id = models.IntegerField()
    name = models.CharField(max_length=50)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'group'
        indexes = [
            models.Index(fields=['created'], name='group_created'),
            models.Index(fields=['id'], name='group_id'),
            models.Index(fields=['member_id'], name='group_member_id'),
            models.Index(fields=['name'], name='group_name'),
        ]

        ordering = ['name']

    @property
    def contact_ids(self) -> List[int]:
        """
        Returns a List of IDs for the contacts in the Group
        """
        return list(self.contacts.values_list('id', flat=True))

    @property
    def total_contacts(self) -> str:
        """
        The total number of Contacts in the Group.
        """
        return self.contacts.count()

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the GroupResource view for this Group record
        :return: A URL that corresponds to the views for this Group record
        """
        return reverse('group_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Group instance, and clear the gorup_contacts associated it
        """
        self.contacts.clear()
        self.deleted = datetime.utcnow()
        self.save()
