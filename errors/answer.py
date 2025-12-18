"""
Error codes for all the methods in Answer
"""
# Create
contact_answer_create_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_answer_create_002 = (
    'The sent data in the request is invalid. "question" and "conversation_id" are both required.'
)
contact_answer_create_003 = (
    'The send "conversation_id" parameter in data is invalid. "conversation_id" must belong to a valid Conversation '
    'record in the Chatbot.'
)
contact_answer_create_201 = 'You do not have Permission to make this request.'
