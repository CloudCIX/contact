from django.db import models

__all__ = [
    # Opportunity Contact
    'OpportunityContact',
]


class OpportunityContact(models.Model):

    # Fields
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    opportunity = models.ForeignKey('Opportunity', on_delete=models.CASCADE)

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'opportunity_contact'

        unique_together = ('contact', 'opportunity')
