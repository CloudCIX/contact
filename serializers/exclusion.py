# libs
import serpy

__all__ = [
    # Exclusion Serializer
    'ExclusionSerializer',
]


class ExclusionSerializer(serpy.Serializer):
    """
    classes:
        description: A list of comma separated classes to exclude in an HTML Document
        type: array
        items:
            description: Name of a class to be excluded
            type: string
    created:
        description: Timestamp, in ISO format, of when the Exclusion record was created.
        type: string
    id:
        description: The ID of the Exclusion
        type: integer
    name:
        description: The name of the Exclusion
        type: string
    tags:
        description: A list of comma separated HTML tags to exclude in an HTML Document
        type: array
        items:
            description: Name of tag to be excluded.
            type: string
    updated:
        description: Timestamp, in ISO format, of when the Exclusion record was last updated.
        type: string
    uri:
        description: URL that can be used to run methods in the API associated with the Exclusion instance.
        type: string
    """
    created = serpy.Field(attr='created.isoformat', call=True)
    classes = serpy.Field()
    id = serpy.Field()
    name = serpy.Field()
    tags = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
