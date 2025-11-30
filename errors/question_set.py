"""
error codes for all the methods in Question Set
"""
# List
contact_question_set_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_question_set_create_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_question_set_create_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_question_set_create_103 = 'The "name" parameter is invalid. A Question Set with that name already exists.'

# Read
contact_question_set_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question Set record.'

# Update
contact_question_set_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question Set record.'
contact_question_set_update_101 = 'The "name" parameter is invalid. "name" is required and must be a string.'
contact_question_set_update_102 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_question_set_update_103 = 'The "name" parameter is invalid. A Question Set with that name already exists.'

# Delete
contact_question_set_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question Set record.'
