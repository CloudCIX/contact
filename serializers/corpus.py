# libs
import serpy
# local
from .chatbot import ChatbotSerializer
from .exclusion import ExclusionSerializer


__all__ = [
    # Corpus Serializer
    'CorpusSerializer',
]


class CorpusSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Corpus record was created.
        type: string
    chatbot:
        $ref: '#/components/schemas/Chatbot'
    chatbot_id:
        description: The ID of the Chatbot
        type: integer
    content_type:
        description: The Content Type of the rendered content of the hyperlink
        type: string
    exclusion:
        $ref: '#/components/schemas/Exclusion'
    exclusion_id:
        description: The ID of the Exclusion
        type: integer
    hyperlink:
        description: |
            A URL pointing to a public resource. The resource's contents will be converted to a vector embedding
            before being used by the Chatbot.
        type: string
    filename:
        description: |
            A file name to identify the file uploaded as a Corpus
        type: string
    id:
        description: The ID of the Corpus
        type: integer
    status_code:
        description: The status code of response of request to hyperlink
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Corpus record was last updated.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    chatbot = ChatbotSerializer()
    chatbot_id = serpy.Field()
    content_type = serpy.Field()
    exclusion = ExclusionSerializer(required=False)
    exclusion_id = serpy.Field()
    hyperlink = serpy.Field()
    filename = serpy.Field()
    id = serpy.Field()
    status_code = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
