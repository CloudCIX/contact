# stdlib
from datetime import datetime

# libs
from cloudcix_rest.models import BaseModel
from django.db import models
from django.urls import reverse

# local
from .chatbot import Chatbot
from .contact import Contact

__all__ = [
    # Conversation
    'Conversation',
]


class Conversation(BaseModel):
    """
    The Conversation model contains the fields for information about the conversations
    """

    # Fields
    chatbot = models.ForeignKey(Chatbot, on_delete=models.PROTECT, related_name='conversations')
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='conversations', null=True)
    cookie = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'conversation'

        indexes = [
            models.Index(fields=['created'], name='conversation_created'),
            models.Index(fields=['updated'], name='conversation_updated'),
            models.Index(fields=['id'], name='conversation_id'),
            models.Index(fields=['name'], name='conversation_name'),
        ]

        ordering = ['-updated']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the ConversationResource view for this Conversation record
        :return: A URL that corresponds to the views for this Conversation record
        """
        return reverse('conversation_resource', kwargs={'pk': self.pk, 'chatbot_name': self.chatbot.name})

    def cascade_delete(self):
        """
        Delete the Conversation instance, and the questions associated it
        """
        deltime = datetime.utcnow()
        self.questions.all().update(deleted=deltime)
        self.deleted = deltime
        self.save()
