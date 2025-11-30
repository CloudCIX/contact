# libs
import serpy
# local

__all__ = [
    # Campaign Serializer
    'CampaignSerializer',
]


class CampaignSerializer(serpy.Serializer):
    """
    contact_ids:
        description: A list of IDs for Contacts in the Campaign
        type: array
        items:
            description: ID of Contact in the Campaign
            type: integer
    created:
        description: Timestamp, in ISO format, of when the Campaign record was created.
        type: string
    date_of_campaign:
        description: Timestamp, in ISO format, of when the Campaign record is scheduled to be.
        type: string
    id:
        description: The ID of the Campaign
        type: integer
    description:
        description: The description of the Campaign
        type: string
    member_id:
        description: The ID of the member who owns the Campaign
        type: integer
    name:
        description: The name of the Campaign
        type: string
    total_contacts:
        description: The total number of Contacts in the Campaign
        type: integer
    total_responses:
        description: The total number of Campaign Contacts that have responded to the Campaign.
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Campaign record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Campaign instance.
        type: string
    """
    contact_ids = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    date_of_campaign = serpy.Field(attr='date_of_campaign.isoformat', call=True, required=False)
    id = serpy.Field()
    description = serpy.Field()
    member_id = serpy.Field()
    name = serpy.Field()
    total_contacts = serpy.Field()
    total_responses = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
