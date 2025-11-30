# Model file for the embedding table in the vector_db table in cloudcix/pgvector database.
# Migrations are not ran via Django, database and table are created in cloudcix/pgvector provision script
# libs
from django.db import models


__all__ = [
    # Embedding
    'Embedding',
]


class Embedding(models.Model):
    """
    The Embedding model contains the fields for managing the vectors for the corpus of a Chatbot
    """

    # Fields
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True)

    chatbot_id = models.IntegerField()
    chunk = models.TextField()
    hyperlink = models.TextField(null=True)
    filename = models.TextField(null=True)
    vector = models.TextField()

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        db_table = 'embedding'
        # Do not want to include in migrations as it will be in a different database
        abstract = True
