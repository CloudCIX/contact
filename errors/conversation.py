"""
error codes for all the methods in Conversation
"""

# List
contact_conversation_list_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_conversation_list_002 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)
contact_conversation_list_201 = 'You do not have Permission to make this request.'

# Create
contact_conversation_create_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_conversation_create_101 = 'The "contact_id" parameter is invalid. "contact_id" must be an integer'
contact_conversation_create_102 = (
    'The "contact_id" is invalid. "contact_id" must belong to a valid Contact in your member.'
)
contact_conversation_create_103 = (
    'The "cookie" parameter is invalid. If "contact_id" is not sent, "cookie" is required.'
)
contact_conversation_create_104 = 'The "cookie" parameter is invalid. "cookie" cannot be longer than 50 characters.'
contact_conversation_create_105 = 'The "name" parameter is invalid. "name" is required'
contact_conversation_create_106 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_conversation_create_201 = 'You do not have Permission to make this request.'

# Read
contact_conversation_read_001 = (
    'The "chatbot_name" or "pk" path parameter is invalid. "chatbot_name" and "pk" must belong to a valid '
    'Conversation record in the specified Chatbot.'
)
contact_conversation_read_201 = 'You do not have Permission to make this request.'

# Delete
contact_conversation_delete_001 = (
    'The "chatbot_name" or "pk" path parameter is invalid. "chatbot_name" and "pk" must belong to a valid '
    'Conversation record in the specified Chatbot.'
)
contact_conversation_delete_201 = 'You do not have Permission to make this request.'
