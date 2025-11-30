"""
Permissions classes will use their methods to validate permissions for a
request.
These methods will raise any errors that may occur all you have to do is
call the method in the view
"""
# stdlib
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http403
from rest_framework.request import Request
# local
from contact.models import Chatbot, Corpus


class Permissions:

    @staticmethod
    def create(request: Request, obj: Chatbot) -> Optional[Http403]:
        """
        The request to create embedding records is valid if:
        - All the respective Corpus objects has Content Type
        """
        if Corpus.objects.filter(chatbot=obj, content_type=None).exists():
            return Http403(error_code='contact_embeddings_create_201')

        return None
