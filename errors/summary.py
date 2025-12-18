"""
Error codes for all the methods in Summary
"""
# Create
contact_summary_create_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_summary_create_002 = (
    'The sent data in the request is invalid. "question" and either "contact_id" or "cookie" are required.'
)
contact_summary_create_003 = (
    'The send "contact_id" parameter in data is invalid. "contact_id" must belong to a valid Contact record in the '
    'same Member as the Chatbot.'
)
contact_summary_create_004 = (
    'An unknown error has occurred in the CloudCIX OpenAI service. Please try again later or contact CloudCIX support '
    'if this persists.'
)
contact_summary_create_201 = 'You do not have Permission to make this request.'
