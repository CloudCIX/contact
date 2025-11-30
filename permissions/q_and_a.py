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
from contact.models import Chatbot


class Permissions:

    @staticmethod
    def list(request: Request, obj: Chatbot) -> Optional[Http403]:
        """
        The request to list Conversations for a Chatbot is valid if:
        - The User is from the same member as the Chatbot
        - The User is Robot
        """
        if request.user.member_id != obj.member_id:
            if not request.user.robot:
                return Http403(error_code='contact_q_and_a_list_201')
        return None

    @staticmethod
    def create(request: Request) -> Optional[Http403]:
        """
        The request to create a Conversation for a Chatbot is valid if:
        - The User is Robot
        """
        if not request.user.robot:
            return Http403(error_code='contact_q_and_a_create_201')
        return None

    @staticmethod
    def read(request: Request, obj: Chatbot) -> Optional[Http403]:
        """
        The request to read a Conversations for a Chatbot is valid if:
        - The User is from the same member as the Chatbot
        - The User is Robot
        """
        if request.user.member_id != obj.member_id:
            if not request.user.robot:
                return Http403(error_code='contact_q_and_a_read_201')
        return None
