"""
error codes for all the methods in Opportunity Contact
"""
# Create
contact_opportunity_contact_create_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid Opportunity record.'
)
contact_opportunity_contact_create_101 = 'The "contacts" parameter is invalid. "contacts" is required'
contact_opportunity_contact_create_102 = (
    'The "contacts" parameter is invalid. "contacts" is required and must be an array.'
)
contact_opportunity_contact_create_103 = (
    'The "contacts" parameter is invalid. "items" in "contacts" array must be integers.'
)
contact_opportunity_contact_create_104 = (
    'The "contacts" parameter is invalid. "items" in "contacts" must belong to valid Contact object '
)

# Delete
contact_opportunity_contact_delete_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid Opportunity record.'
)
contact_opportunity_contact_delete_101 = 'The "contacts" parameter is invalid. "contacts" is required'
contact_opportunity_contact_delete_102 = (
    'The "contacts" parameter is invalid. "contacts" is required and must be an array.'
)
contact_opportunity_contact_delete_103 = (
    'The "contacts" parameter is invalid. "items" in "contacts" array must be integers.'
)
contact_opportunity_contact_delete_104 = (
    'The "contacts" parameter is invalid. "items" in "contacts" must belong to valid Contact object '
)
