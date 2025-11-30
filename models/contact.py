# stdlib
from datetime import datetime
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local

__all__ = [
    # Contact
    'Contact',
]


class ContactManager(BaseManager):
    """
    Manager for Contact class which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'campaigns',
            'groups',
            'opportunities',
        )


class Contact(BaseModel):
    """
    The Contact model represents the customer information
    """
    # Minimum 8 Characters - {8,}
    # Include uppercase character - (?=.*?[A-Z])
    # Include lowercase character - (?=.*?[a-z])
    # Include number - (?=.*?[0-9]
    # Include special character - (?=.*?[#?!@$%^&*-])
    PASSWORD_REGEX = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

    # Fields
    address = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    country_id = models.IntegerField(null=True)
    currently_visiting = models.BooleanField(default=False)
    email = models.CharField(max_length=250, blank=True)
    first_name = models.CharField(max_length=50)
    hashed_pwd = models.BinaryField(null=True)
    linkedin_url = models.CharField(max_length=200, blank=True)
    member_id = models.IntegerField()
    notes = models.TextField(blank=True)
    opt_notes = models.TextField(blank=True)
    opt_out = models.BooleanField(default=False)
    phone_number = models.JSONField(default=dict)
    postcode = models.CharField(max_length=20, blank=True)
    salt = models.BinaryField(null=True)
    subdivision_id = models.IntegerField(null=True)
    surname = models.CharField(max_length=50)
    title = models.CharField(max_length=100, blank=True)
    website = models.CharField(max_length=50, blank=True)

    objects = BaseManager()
    list_objects = ContactManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'contact'
        indexes = [
            models.Index(fields=['address'], name='contact_address'),
            models.Index(fields=['address2'], name='contact_address2'),
            models.Index(fields=['city'], name='contact_city'),
            models.Index(fields=['company_name'], name='contact_company_name'),
            models.Index(fields=['country_id'], name='contact_country_id'),
            models.Index(fields=['created'], name='contact_created'),
            models.Index(fields=['currently_visiting'], name='contact_visiting'),
            models.Index(fields=['email'], name='contact_email'),
            models.Index(fields=['first_name'], name='contact_first_name'),
            models.Index(fields=['member_id'], name='contact_member_id'),
            models.Index(fields=['opt_out'], name='contact_opt_out'),
            models.Index(fields=['phone_number'], name='contact_phone_number'),
            models.Index(fields=['postcode'], name='contact_postcode'),
            models.Index(fields=['subdivision_id'], name='contact_subdivision_id'),
            models.Index(fields=['surname'], name='contact_surname'),
            models.Index(fields=['website'], name='contact_website'),
        ]

        ordering = ['surname']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the ContactResource view for this Contact record
        :return: A URL that corresponds to the views for this Contact record
        """
        return reverse('contact_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Contact instance, and the conversations associated it
        """
        for conversation in self.conversations.all().iterator():
            conversation.cascade_delete()
        self.campaigns.clear()
        self.groups.clear()
        self.opportunities.clear()
        self.deleted = datetime.utcnow()
        self.save()
