# libs
import serpy
# local
from .question_translation import QuestionTranslationSerializer
from contact.models import Question


__all__ = [
    # Question Base Serializer
    'QuestionBaseSerializer',
    # Question Serializer
    'QuestionSerializer',
]


class QuestionBaseSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Question record was created.
        type: string
    default_question:
        description: A question from the translations to identify the group.
        type: string
    id:
        description: The ID of the Question
        type: integer
    question_set_id:
        description: The Id of the Question Set the question belongs to
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Question record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Question instance.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    default_question = serpy.Field()
    id = serpy.Field()
    question_set_id = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)


class QuestionSerializer(QuestionBaseSerializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Question record was created.
        type: string
    default_question:
        description: A question from the translations to identify the group.
        type: string
    id:
        description: The ID of the Question
        type: integer
    question_set_id:
        description: The Id of the Question Set the question belongs to
        type: integer
    question_translations:
        $ref: '#/components/schemas/QuestionTranslation'
    updated:
        description: Timestamp, in ISO format, of when the Question record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Question instance.
        type: string
    """
    question_translations = serpy.MethodField()

    def get_question_translations(self, obj: Question):
        return QuestionTranslationSerializer(obj.question_translations.iterator(chunk_size=2000), many=True).data
