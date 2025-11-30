# libs
import serpy
# local

__all__ = [
    # Group Serializer
    'GroupSerializer',
]


class GroupSerializer(serpy.Serializer):
    """
    contact_ids:
        description: A list of IDs for Contacts in the Group
        type: array
        items:
            description: ID of Contact in the Group
            type: integer
    created:
        description: Timestamp, in ISO format, of when the Group record was created.
        type: string
    id:
        description: The ID of the Group
        type: integer
    member_id:
        description: The ID of the member who owns the Group
        type: integer
    name:
        description: The name of the Group
        type: string
    total_contacts:
        description: The total number of Contacts in the Group.
        type: integer
    updated:
        description: Timestamp, in ISO format, of when the Group record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Group instance.
        type: string
    """
    contact_ids = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    id = serpy.Field()
    member_id = serpy.Field()
    name = serpy.Field()
    total_contacts = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
