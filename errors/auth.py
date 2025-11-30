"""
Error Codes for all of the Methods in the Auth Service
"""

# Create
contact_auth_create_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_auth_create_002 = 'Both the "email" and "password" keys are required in the sent data.'
contact_auth_create_003 = 'The sent email and password combination is invalid. Please check both and try again.'
contact_auth_create_201 = 'You do not have Permission to make this request.'
