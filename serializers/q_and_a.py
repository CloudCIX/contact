# libs
import serpy

# local
from .reference import ReferenceSerializer

__all__ = [
    'QAndASerializer',
]


class QAndASerializer(serpy.Serializer):
    """
    answer:
        description: The answer the chatbot gave to the contacts question.
        type: string
    conversation_id:
        description: ID of Conversation record
        type: integer
    created:
        description: Timestamp, in ISO format, of when the QAndA record was created.
        type: string
    id:
        description: The ID of the Q and A
        type: integer
    question:
        description: The question the contact asked the chatbot.
        type: string
    question_images:
        description: List of (base64 encoded image object, image mime, image name) sent by the user.
        type: array
        items:
            description: A tuple containing (base64 encoded image object, image mime, image name).
            type: array
            items:
                type: string
    references:
        $ref: '#/components/schemas/Reference'
        type: array
    updated:
        description: Timestamp, in ISO format, of when the QAndA record was last updated.
        type: string
    uri:
        description:
            URL that can be used to run methods in the API associated with the QAndA instance.
        type: string
    """
    answer = serpy.Field()
    conversation_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    question = serpy.Field()
    question_images = serpy.Field(required=False)  # new field
    references = ReferenceSerializer(attr='references.all', call=True, many=True)
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
