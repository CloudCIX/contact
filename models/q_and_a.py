# stdlib
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse

# local
from .conversation import Conversation

__all__ = [
    # QAndA
    'QAndA',
]


class QAndAManager(BaseManager):
    """
    Manager for QAndA which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'references',
        )


class QAndA(BaseModel):
    """
    The QAndA model contains the fields for information about the questions and answers
    """

    # Fields
    answer = models.TextField()
    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT, related_name='questions')
    question = models.TextField()
    intent = models.TextField(blank=True, null=True)
    question_images = models.JSONField(default=list, blank=True)  # list of (base64 object, image mime, image name)

    objects = QAndAManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'q_and_a'

        indexes = [
            models.Index(fields=['created'], name='q_and_a_created'),
            models.Index(fields=['id'], name='q_and_a_id'),
        ]

        ordering = ['question']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the QAndAResource view for this QAndA record
        :return: A URL that corresponds to the views for this QAndA record
        """
        return reverse(
            'q_and_a_resource',
            kwargs={
                'pk': self.pk,
                'conversation_id': self.conversation_id,
                'chatbot_name': self.conversation.chatbot.name,
            },
        )
