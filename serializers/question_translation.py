# libs
import serpy
# local

__all__ = [
    # Question Translation Serializer
    'QuestionTranslationSerializer',
]


class QuestionTranslationSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Question Translation record was created.
        type: string
    answer:
        description: Expected answer to be given based on the question asked and the chunk provided
        type: string
    chunk:
        description: Paragraph in which the answer to the question should be contained
        type: string
    id:
        description: The ID of the Question Translation
        type: integer
    language_id:
        description: The Id of the language of the question asked
        type: integer
    question:
        description: The question provided by the user
        type: string
    updated:
        description: Timestamp, in ISO format, of when the Question Set record was last updated.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    answer = serpy.Field()
    chunk = serpy.Field()
    id = serpy.Field()
    language_id = serpy.Field()
    question = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
