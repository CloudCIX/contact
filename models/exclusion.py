# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse
# local

__all__ = [
    # Exclusion
    'Exclusion',
]


class Exclusion(BaseModel):
    """
    The Exclusion model contains the fields for managing the data in a Document (HTML, XML)
    """

    # Fields
    classes = models.JSONField(default=list)
    name = models.CharField(max_length=100)
    tags = models.JSONField(default=list)
    member_id = models.IntegerField()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'exclusion'

        indexes = [
            models.Index(fields=['created'], name='exclusion_created'),
            models.Index(fields=['id'], name='exclusion_id'),
            models.Index(fields=['name'], name='exclusion_name'),
        ]

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the ExclusionResource view for this Exclusion record
        :return: A URL that corresponds to the views for this Exclusion record
        """
        return reverse('exclusion_resource', kwargs={'pk': self.pk})
