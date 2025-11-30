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
from contact.models import Question, QuestionSet


class Permissions:

    @staticmethod
    def create(request: Request, obj: QuestionSet) -> Optional[Http403]:
        """
        The request to create question for a global QuestionSet is valid if:
        - The User is from the member 1
        """
        if obj.member_id == 0:
            if request.user.member_id != 1:
                return Http403(error_code='contact_question_create_201')
        return None

    @staticmethod
    def update(request: Request, obj: Question) -> Optional[Http403]:
        """
        The request to update question for a global QuestionSet is valid if:
        - The User is from the member 1
        """
        if obj.question_set.member_id == 0:
            if request.user.member_id != 1:
                return Http403(error_code='contact_question_update_201')
        return None

    @staticmethod
    def delete(request: Request, obj: Question) -> Optional[Http403]:
        """
        The request to delete question for a global QuestionSet is valid if:
        - The User is from the member 1
        """
        if obj.question_set.member_id == 0:
            if request.user.member_id != 1:
                return Http403(error_code='contact_question_delete_201')
        return None
