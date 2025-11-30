"""
error codes for all the methods in Opportunity
"""
# List
contact_opportunity_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_opportunity_create_101 = 'The "description" parameter is invalid. "description" cant be empty.'
contact_opportunity_create_102 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_opportunity_create_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_opportunity_create_104 = 'The "probability" parameter is invalid. "probability" should be a decimal.'
contact_opportunity_create_105 = 'The "probability" parameter is invalid. probability should be in the range [0,100].'
contact_opportunity_create_106 = 'The "closed" parameter is invalid. It should be a boolean field.'
contact_opportunity_create_107 = 'The "closed" parameter is invalid. Probability should be 0 or 100.'
contact_opportunity_create_108 = 'The "value" parameter is invalid. "value" should be a decimal.'
contact_opportunity_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
contact_opportunity_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid opportunity record.'

# Update
contact_opportunity_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid opportunity record.'
contact_opportunity_update_101 = 'The "description" parameter is invalid. "description" cant be empty.'
contact_opportunity_update_102 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_opportunity_update_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_opportunity_update_104 = 'The "probability" parameter is invalid. "probability" should be a decimal.'
contact_opportunity_update_105 = 'The "probability" parameter is invalid. probability should be in the range [0,100].'
contact_opportunity_update_106 = 'The "closed" parameter is invalid. It should be a boolean field.'
contact_opportunity_update_107 = 'The "closed" parameter is invalid. Probability should be 0 or 100.'
contact_opportunity_update_108 = 'The "value" parameter is invalid. "value" should be a decimal.'

# Delete
contact_opportunity_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid opportunity record.'
