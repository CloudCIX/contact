"""
error codes for all the methods in Opportunity History
"""
# List
contact_opportunity_history_list_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid Opportunity record.'
)

# Create
contact_opportunity_history_create_001 = (
    'The "pk" path parameter is invalid. "pk" must belong to a valid Opportunity record.'
)
contact_opportunity_history_create_101 = 'The "heading" parameter is invalid. "heading" must be less than 50 characters'
contact_opportunity_history_create_102 = (
    'The "history_type" parameter is invalid. "history_type" is required and must be a string'
)
contact_opportunity_history_create_103 = (
    'The "history_type" parameter is invalid. "history_type" is required and must be an allowed choice'
)
contact_opportunity_history_create_104 = 'The "cc" parameter is invalid. "cc" must be an array of Email addresses'
contact_opportunity_history_create_105 = 'The "cc" parameter is invalid. "item" in "cc" must be a valid mail address'
contact_opportunity_history_create_106 = 'The "message" parameter is invalid. "message" is required and cannot be empty'
contact_opportunity_history_create_107 = 'The "message" parameter is invalid. "message" cannot be empty'
contact_opportunity_history_create_108 = 'The "reply_to" parameter is invalid. "reply_to" must be a valid Email address'
contact_opportunity_history_create_109 = 'The "to" parameter is invalid. "to" must be an array of Email addresses'
contact_opportunity_history_create_110 = 'The "to" parameter is invalid. "to" cannot be an Empty array'
contact_opportunity_history_create_111 = (
    'The "to parameter is invalid. "items" in "to" array must be valid Email addresses'
)
