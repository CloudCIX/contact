# libs
import serpy
# local
from .campaign import CampaignSerializer
from .group import GroupSerializer
from .opportunity import OpportunitySerializer

__all__ = [
    # Contact Serializer
    'ContactSerializer',
]


class ContactSerializer(serpy.Serializer):
    """
    address:
        description: The first line of the geographic address of the Contact
        type: string
    address2:
        description: The second line of the geographic address of the Contact
        type: string
    campaigns:
        $ref: '#/components/schemas/Campaign'
    city:
        description: The city in which the address of the Contact is located
        type: string
    company_name:
        description: The name of the company where the Contact is employed
        type: string
    country_id:
        description: The ID of the Country of the Contacts geographic address
        type: integer
    created:
        description: Timestamp, in ISO format, of when the Contact record was created.
        type: string
    currently_visiting:
        description: Flag denoting if the Contact is currently visiting the Member
        type: boolean
    email:
        description: The email address of the Contact
        type: string
    first_name:
        description: The first name of the Contact
        type: string
    groups:
        $ref: '#/components/schemas/Group'
    id:
        description: ID of Contact record
        type: integer
    linkedin_url:
        description: URL to the LinkedIn profile of the Contact
        type: string
    member_id:
        description: The ID of the Member who owns the Contact record
        type: integer
    notes:
        description: Notes on the Contact
        type: string
    opportunities:
        $ref: '#/components/schemas/Opportunity'
    opt_notes:
        description: Notes on the Contact recording if the opt in or out of communications from the Member
        type: string
    opt_out:
        description: Flag denoting if the Contact has opted out of communication from the Member
        type: boolean
    phone_number:
        description: An array of named phone numbers used by the Contact
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
    postcode:
        description: The postcode of the geographical address of the Contact
        type: string
    subdivision_id:
        description: The ID of the Subdivision in the Country of the Contacts geographic address
        type: Integer
    surname:
        description: The surname of the Contact
        type: string
    title:
        description: The professional title of the Contact
        type: string
    updated:
        description: Timestamp, in ISO format, of when the Contact record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Contact instance.
        type: string
    website:
        description: A website link of the Contact
        type: string
    """
    address = serpy.Field()
    address2 = serpy.Field()
    campaigns = CampaignSerializer(attr='campaigns.all', call=True, many=True)
    city = serpy.Field()
    company_name = serpy.Field()
    country_id = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    currently_visiting = serpy.Field()
    email = serpy.Field()
    first_name = serpy.Field()
    groups = GroupSerializer(attr='groups.all', call=True, many=True)
    id = serpy.Field()
    linkedin_url = serpy.Field()
    member_id = serpy.Field()
    notes = serpy.Field()
    opportunities = OpportunitySerializer(attr='opportunities.all', call=True, many=True)
    opt_notes = serpy.Field()
    opt_out = serpy.Field()
    phone_number = serpy.Field()
    postcode = serpy.Field()
    subdivision_id = serpy.Field()
    surname = serpy.Field()
    title = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    website = serpy.Field()
