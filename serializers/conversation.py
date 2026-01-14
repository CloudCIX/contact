# libs
import serpy

# local


__all__ = [
    # Conversation Serializer
    'ConversationSerializer',
]


class ConversationSerializer(serpy.Serializer):
    """
    created:
        description: Timestamp, in ISO format, of when the Conversation record was created.
        type: string
    chatbot_id:
        description: The Chatbot ID of the Conversation
        type: integer
    contact_id:
        description: The ID of the contact who owns the Conversation
        type: integer
    id:
        description: The ID of the Conversation
        type: integer
    name:
        description: The name of the Conversation
        type: string
    updated:
        description: Timestamp, in ISO format, of when the Conversation record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Conversation instance.
        type: string
    last_message_at:
        description: Timestamp, in ISO format, of when the last message was sent in the Conversation
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    chatbot_id = serpy.Field()
    contact_id = serpy.Field()
    id = serpy.Field()
    name = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    last_message_at = serpy.Field(attr='last_message_at.isoformat', call=True)
