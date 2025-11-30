# libs
import serpy
# local

__all__ = [
    # Opportunity History Serializer
    'OpportunityHistorySerializer',
]


class OpportunityHistorySerializer(serpy.Serializer):
    """
    cc:
        description: If type is email, this is the email addresses cc'd on the email
        type: string
    created:
        description: Timestamp, in ISO format, of when the Opportunity History record was created.
        type: string
    heading:
        description: The heading title for history record
        type: string
    history_type:
        description: Type of history record this is, note or email
        type: string
    id:
        description: The ID of the Opportunity History
        type: integer
    message:
        description: |
            If the type is a note this then is the notes for the record. If the type is email this is the body of the
            email.
        type: string
    reply_to:
        description: If type is email, this is the reply-to address on the email
        type: string
    to:
        description: If type is email, this is the email addresses the email was sent to
        type: string
    user_id:
        description: ID of the user who created the Opportunity History record.
        type: integer
    """
    cc = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    heading = serpy.Field()
    history_type = serpy.Field()
    id = serpy.Field()
    message = serpy.Field()
    reply_to = serpy.Field()
    to = serpy.Field()
    user_id = serpy.Field()
