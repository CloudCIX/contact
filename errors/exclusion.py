"""
error codes for all the methods in Exclusion
"""
# List
contact_exclusion_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_exclusion_create_101 = 'The "classes" parameter is invalid. "classes" should be an array'
contact_exclusion_create_102 = 'The "classes" parameter is invalid. item in "classes" array should not be empty'
contact_exclusion_create_103 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_exclusion_create_104 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_exclusion_create_105 = 'The "name" parameter is invalid. An Exclusion with that name already exists.'
contact_exclusion_create_106 = 'The "tags" parameter is invalid. "tags" should be an array.'
contact_exclusion_create_107 = 'The "tags" parameter is invalid. item in "tags" array should not be empty'

# Read
contact_exclusion_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Exclusion record.'

# Update
contact_exclusion_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Exclusion record.'
contact_exclusion_update_101 = 'The "classes" parameter is invalid. "classes" should be an array'
contact_exclusion_update_102 = 'The "classes" parameter is invalid. item in "classes" array should not be empty'
contact_exclusion_update_103 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_exclusion_update_104 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_exclusion_update_105 = 'The "name" parameter is invalid. An Exclusion with that name already exists.'
contact_exclusion_update_106 = 'The "tags" parameter is invalid. "tags" should be an array.'
contact_exclusion_update_107 = 'The "tags" parameter is invalid. item in "tags" array should not be empty'

# Delete
contact_exclusion_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Exclusion record.'
contact_exclusion_delete_201 = 'You do not have permission to make this request. One of the Corpus uses this exclusion'
