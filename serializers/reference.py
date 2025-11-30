# libs
import serpy

__all__ = [
    'ReferenceSerializer',
]


class ReferenceSerializer(serpy.Serializer):
    """
    hyperlink:
        description: A URL to create the assigned chatbots vector embeddings from.
        type: string
    id:
        description: The ID of the Reference
        type: integer
    """
    hyperlink = serpy.Field()
    id = serpy.Field()
