"""
error codes for all the methods in Group
"""
# List
contact_group_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_group_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_group_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_group_create_103 = 'The "name" parameter is invalid. A Group with that name already exists.'
contact_group_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
contact_group_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Group record.'

# Update
contact_group_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Group record.'
contact_group_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_group_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_group_update_103 = 'The "name" parameter is invalid. A Group with that name already exists.'

# Delete
contact_group_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Group record.'
