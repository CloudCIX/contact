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
from contact.models import Contact


class Permissions:

    @staticmethod
    def create(request: Request, obj: Contact) -> Optional[Http403]:
        """
        The request to create a new Contact record is valid if:
        - The User creating a Contact is a self-managed Member
        - The User is the same Member as the contact
        - The user is robot
        """
        # The requesting User's Member is self-managed
        if not request.user.member['self_managed']:
            return Http403(error_code='contact_contact_create_201')
        # The User is the same Member as the contact
        if obj.member_id != request.user.member_id:
            # The user is robot
            if not request.user.robot:
                return Http403(error_code='contact_contact_create_202')
        return None

    @staticmethod
    def read(request: Request, obj: Contact) -> Optional[Http403]:
        """
        The request to read a new Contact record is valid if:
        - The User is the same Member as the contact
        - The user is robot
        """
        # The User is the same Member as the contact
        if obj.member_id != request.user.member_id:
            # The user is robot
            if not request.user.robot:
                return Http403(error_code='contact_contact_read_201')
        return None

    @staticmethod
    def update(request: Request, obj: Contact) -> Optional[Http403]:
        """
        The request to update a new Contact record is valid if:
        - The User is the same Member as the contact
        - The user is robot
        """
        # The User is the same Member as the contact
        if obj.member_id != request.user.member_id:
            # The user is robot
            if not request.user.robot:
                return Http403(error_code='contact_contact_update_201')
        return None
