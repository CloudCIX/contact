from django.db import models

__all__ = [

    # Group Contact
    'GroupContact',
]


class GroupContact(models.Model):

    # Fields
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'group_contact'

        unique_together = ('group', 'contact')
