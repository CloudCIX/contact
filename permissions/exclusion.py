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
from contact.models import Corpus, Exclusion


class Permissions:

    @staticmethod
    def delete(request: Request, obj: Exclusion) -> Optional[Http403]:
        """
        The request to delete an exclusion record is valid if:
        - The exclusion record is not in use with any corpus record
        """
        if Corpus.objects.filter(exclusion=obj).exists():
            return Http403(error_code='contact_exclusion_delete_201')

        return None
