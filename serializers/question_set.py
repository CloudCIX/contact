# libs
import serpy
# local
from .question import QuestionBaseSerializer
from contact.models import QuestionSet


__all__ = [
    # Question Set Serializer
    'QuestionSetSerializer',
]


class QuestionSetSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Question Set record was created.
        type: string
    id:
        description: The ID of the Question Set
        type: integer
    member_id:
        description: The id of the Member which the QuestionSet belongs to
        type: integer
    name:
        description: The name of the Question Set
        type: string
    questions:
        $ref: '#/components/schemas/Question'
    updated:
        description: Timestamp, in ISO format, of when the Question Set record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Question Set instance.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    member_id = serpy.Field()
    name = serpy.Field()
    questions = serpy.MethodField()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)

    def get_questions(self, obj: QuestionSet):
        return QuestionBaseSerializer(obj.questions.iterator(chunk_size=2000), many=True).data
