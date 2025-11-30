# stdlib
from typing import Optional
from datetime import datetime
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse
# local
from .question_set import QuestionSet

__all__ = [
    # Question
    'Question',
]


class QuestionManager(BaseManager):
    """
    Manager for Question which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'question_translations',
        )


class Question(BaseModel):
    """
    The Question is used to represent a question in the question_set.
    """
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')

    objects = QuestionManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'question'

        indexes = [
            models.Index(fields=['id'], name='question_id'),
        ]

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the QuestionResource view for this Question record
        :return: A URL that corresponds to the views for this Question record
        """
        return reverse('question_resource', kwargs={'pk': self.pk})

    @property
    def default_question(self) -> Optional[str]:
        """
        Return a defualt question in the repsonse to display in the list. Ordering by language_id ascending will
        ensure that English is the default if available
        """
        objs = list(self.question_translations.order_by('language_id').values_list('question', flat=True).iterator())
        default_question = None
        if len(objs) > 0:
            default_question = objs[0]
        return default_question

    def cascade_delete(self):
        """
        Delete the Question instance, and the translations associated it
        """
        deltime = datetime.utcnow()
        self.question_translations.all().update(deleted=deltime)
        self.deleted = deltime
        self.save()
