# libs
from cloudcix_rest.models import BaseModel
from django.db import models
# local
from .question import Question

__all__ = [
    # Question Translation
    'QuestionTranslation',
]


class QuestionTranslation(BaseModel):
    """
     Question Translation is to store the question in multiple languages
    """
    answer = models.TextField()
    chunk = models.TextField()
    language_id = models.IntegerField()
    question = models.TextField()
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_translations')

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'question_translation'

        indexes = [
            models.Index(fields=['created'], name='question_translation_created'),
            models.Index(fields=['id'], name='question_translation_id'),
        ]
