# stdlib
# libs
from cloudcix_rest.controllers import ControllerBase
# local


__all__ = [
    'CorpusListController',
]


class CorpusListController(ControllerBase):
    """
    Validates User data used to list Corpus records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'hyperlink',
            'created',
            'id',
        )
        search_fields = {
            'hyperlink': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
