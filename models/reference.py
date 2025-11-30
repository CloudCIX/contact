# libs
from cloudcix_rest.models import BaseModel
from django.db import models
# local
from .q_and_a import QAndA

__all__ = [
    # Reference
    'Reference',
]


class Reference(BaseModel):
    """
    The Reference model contains the fields for the references
    """

    # Fields
    hyperlink = models.URLField()
    q_and_a = models.ForeignKey(QAndA, on_delete=models.PROTECT, related_name='references')

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'reference'

        indexes = [
            models.Index(fields=['created'], name='reference_created'),
            models.Index(fields=['hyperlink'], name='reference_hyperlink'),
            models.Index(fields=['id'], name='reference_id'),
        ]
