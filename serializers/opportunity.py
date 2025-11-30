# libs
import serpy
# local
from .opportunity_history import OpportunityHistorySerializer

__all__ = [
    # Opportunity Serializer
    'OpportunitySerializer',
]


class OpportunitySerializer(serpy.Serializer):
    """
    closed:
        description: A flag stating if the Opportunity is open or closed.
        type: boolean
    contact_ids:
        description: A list of IDs for Contacts in the Opportunity
        type: array
        items:
            description: ID of Contact in the Opportunity
            type: integer
    created:
        description: Timestamp, in ISO format, of when the Opportunity record was created.
        type: string
    description:
        description: A description of the Opportunity
        type: string
    history:
        description: An array of Opportunity History objects for all the history records this Opportunity has.
        type: array
        items:
             $ref: '#/components/schemas/OpportunityHistory'
    id:
        description: ID of Opportunity record
        type: integer
    member_id:
        description: The ID of the member who owns the Opportunity
        type: integer
    name:
        description: The name of the Opportunity
        type: string
    outcome:
        description: The description of the result of the Opportunity
        type: string
    probability:
        description: The probability rating of being successful with the Opportunity from 0% to 100%.
        type: string
        format: decimal
    total_contacts:
        description: The total number of Contacts in the Opportunity.
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Opportunity record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Opportunity instance.
        type: string
    value:
        description: The value the Opportunity is worth to the business
        type: string
        format: decimal
    """
    contact_ids = serpy.Field()
    closed = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    description = serpy.Field()
    history = OpportunityHistorySerializer(attr='history.all', call=True, many=True)
    id = serpy.Field()
    member_id = serpy.Field()
    name = serpy.Field()
    outcome = serpy.Field()
    probability = serpy.Field()
    total_contacts = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    value = serpy.Field()
