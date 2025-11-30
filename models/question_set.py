# stdlib
from datetime import datetime
# libs
from cloudcix_rest.models import BaseManager, BaseModel
from django.db import models
from django.urls import reverse


__all__ = [
    # Question Set
    'QuestionSet',
]


class QuestionSetManager(BaseManager):
    """
    Manager for Question Set which pre-fetches foreign keys
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Extend the BaseManager QuerySet to prefetch all related data in every query to speed up serialization
        :return: A base queryset which can be further extended but always pre-fetches necessary data
        """
        return super().get_queryset().prefetch_related(
            'questions',
        )


class QuestionSet(BaseModel):
    """
    The Questions Set is used to group questions into a set that the test will execute.
    """

    name = models.CharField(max_length=100)
    member_id = models.IntegerField()

    objects = QuestionSetManager()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'question_set'

        indexes = [
            models.Index(fields=['id'], name='question_set_id'),
            models.Index(fields=['name'], name='question_set_name'),
        ]

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the QuestionSetResource view for this QuestionSet record
        :return: A URL that corresponds to the views for this QuestionSet record
        """
        return reverse('question_set_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Question Set instance, and the questions associated with it
        """
        deltime = datetime.utcnow()
        for question in self.questions.all().iterator(chunk_size=2000):
            question.cascade_delete()
        self.deleted = deltime
        self.save()
