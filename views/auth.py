"""
Handling for Contact authentication
"""
# stdlib
# libs
import bcrypt
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
# local
from contact.models import Chatbot, Contact
from contact.permissions.auth import Permissions
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response

__all__ = [
    'AuthResource',
]


class AuthResource(APIView):
    """
    Handles the authenticating for contacts
    """

    def post(self, request: Request, chatbot_name: str) -> Response:
        """
        summary: Validate a Contacts's credentials.

        description: |
            The Contact sends an email and password, this service will attempt to authenticate them, returning a
            200 if the details are valid, and a 400 otherwise.

        path_params:
            chatbot_name:
                description: The name of the Chatbot to authenticate the credentials for
                type: string

        responses:
            200:
                description: |
                    Sent email and password are valid. The 'contact_id` will be returned in the response for the
                    Gateway Agent to identify.
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                contact_id:
                                    description: The ID of the Contact for sent credential
                                    type: integer
            400: {}
            404: {}
        """
        # Check that the necessary information is provided
        tracer = settings.TRACER
        data = request.data

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Chatbot.objects.get(name=chatbot_name)
            except Chatbot.DoesNotExist:
                return Http404(error_code='contact_auth_create_001')

        with tracer.start_span('checking_for_required_fields', child_of=request.span):
            if 'email' not in data or 'password' not in data:
                return Http400(error_code='contact_auth_create_002')

        # Fetch contact for sent email in requesting users member
        with tracer.start_span('fetching_contact', child_of=request.span):
            try:
                contact = Contact.objects.get(email=data['email'], member_id=obj.member_id)
            except Contact.DoesNotExist:
                return Http400(error_code='contact_auth_create_003')

        # Validate sent password
        with tracer.start_span('validating_credentials', child_of=request.span):
            # 'salt' and 'hashed_pwd' are 'memoryview' objects and needs to converted to bytes
            salt = bytes(contact.salt)
            stored_hashed_pwd = bytes(contact.hashed_pwd)
            sent_hashed_pwd = bcrypt.hashpw(data['password'].encode('utf-8'), salt)

            if sent_hashed_pwd != stored_hashed_pwd:
                return Http400(error_code='contact_auth_create_003')

        # Return 200 to let the user know the auth is valid
        content = {
            'contact_id': contact.pk,
            'first_name': contact.first_name,
        }
        return Response({'content': content})
