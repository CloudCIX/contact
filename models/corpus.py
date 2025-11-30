# libs
from cloudcix_rest.models import BaseModel
from django.db import models
# local
from .chatbot import Chatbot
from .exclusion import Exclusion

__all__ = [
    # Corpus
    'Corpus',
]


class Corpus(BaseModel):
    """
    The Corpus model contains the fields for managing the data in a Chatbot
    """

    # Fields
    content_type = models.CharField(max_length=50, null=True)
    filename = models.CharField(max_length=255, null=True)
    hyperlink = models.URLField(max_length=255, null=True)
    status_code = models.IntegerField(null=True)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.PROTECT, related_name='corpora')
    exclusion = models.ForeignKey(Exclusion, on_delete=models.PROTECT, related_name='exclusions', null=True)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'corpus'

        indexes = [
            models.Index(fields=['created'], name='corpus_created'),
            models.Index(fields=['content_type'], name='corpus_content_type'),
            models.Index(fields=['hyperlink'], name='corpus_hyperlink'),
            models.Index(fields=['id'], name='corpus_id'),
        ]
