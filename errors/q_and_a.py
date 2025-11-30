"""
error codes for all the methods in QAndA
"""

# List
contact_q_and_a_list_001 = (
    'The "chatbot_name" or "conversation_id" path parameters are invalid. "chatbot_name" and "conversation_id" must '
    'belong to a valid Conversation record.'
)
contact_q_and_a_list_201 = 'You do not have Permission to make this request.'

# Create
contact_q_and_a_create_001 = (
    'The "chatbot_name" or "conversation_id" path parameters are invalid. "chatbot_name" and "conversation_id" must '
    'belong to a valid Conversation record.'
)
contact_q_and_a_create_101 = 'The "answer" parameter is invalid. "answer" is required and must be a string.'
contact_q_and_a_create_102 = 'The "answer" parameter is invalid. "answer" cannot be empty.'
contact_q_and_a_create_103 = 'The "question" parameter is invalid. "question" is required and must be a string.'
contact_q_and_a_create_104 = 'The "question" parameter is invalid. "question" cannot be empty.'
contact_q_and_a_create_105 = 'The "references" parameter is invalid. "references" must be an array.'
contact_q_and_a_create_106 = 'The "references" parameter is invalid. Every item in "references" must be a valid url.'
contact_q_and_a_create_201 = 'You do not have Permission to make this request.'

# Read
contact_q_and_a_read_001 = (
    'The "pk", "chatbot_name" or "conversation_id" path parameters are invalid. "pk", "chatbot_name" and '
    '"conversation_id" must belong to a valid QAndA object.'
)
contact_q_and_a_read_201 = 'You do not have Permission to make this request.'
