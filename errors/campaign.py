"""
error codes for all the methods in Campaign
"""
# List
contact_campaign_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_campaign_create_101 = (
    'The "ndate_of_campaigname" parameter is invalid. "date_of_campaign" is required and must be in the correct format'
)
contact_campaign_create_102 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_campaign_create_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_campaign_create_104 = 'The "name" parameter is invalid. A Campaign with that name already exists.'
contact_campaign_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
contact_campaign_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Campaign record.'

# Update
contact_campaign_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Campaign record.'
contact_campaign_update_101 = (
    'The "ndate_of_campaigname" parameter is invalid. "date_of_campaign" is required and must be in the correct format'
)
contact_campaign_update_102 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_campaign_update_103 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_campaign_update_104 = 'The "name" parameter is invalid. A Campaign with that name already exists.'

# Delete
contact_campaign_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Campaign record.'
