"""
error codes for all the methods in Question
"""
# List
contact_question_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_question_create_101 = (
    'The "question_set_id" parameter is invalid. "question_set_id" is required and must be an integer.'
)
contact_question_create_102 = 'The "question_set_id" parameter is invalid. "question_set_id" must be an integer.'
contact_question_create_103 = (
    'The "question_set_id" parameter is invalid. "question_set_id" does not belong to a valid QuestionSet record'
)
contact_question_create_104 = (
    'The "question_translations" parameter is invalid. "question_translations" is required and must be an array '
)
contact_question_create_105 = (
    'The "question_translations" parameter is invalid. "question_translations" cannot be empty'
)
contact_question_create_106 = (
    'The "question_translations" parameter is invalid. Each item in the array "question_translations" '
    'must be an object. '
)
contact_question_create_107 = (
    'The "question_translations" parameter is invalid. "answer" is required for each item in the array '
    '"question_translations"'
)
contact_question_create_108 = (
    'The "question_translations" parameter is invalid. "chunk" is required for each item in the array '
    '"question_translations"'
)
contact_question_create_109 = (
    'The "question_translations" parameter is invalid. "language_id" is required for each item in the array '
    '"question_translations"'
)
contact_question_create_110 = (
    'The "question_translations" parameter is invalid. "language_id" in the array must be an integer.'
)
contact_question_create_111 = (
    'The "question_translations" parameter is invalid. "language_id" in the array must belong to valid language record'
)
contact_question_create_112 = (
    'The "question_translations" parameter is invalid. "question" is required for each item in the array '
    '"question_translations"'
)
contact_question_create_201 = (
    'You do not have permission to execute this method. You can only create a Question in Question Sets owned '
    'by your Member.'
)

# Read
contact_question_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question record.'

# Update
contact_question_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question record.'
contact_question_update_101 = (
    'The "question_translations" parameter is invalid. "question_translations" is required and must be an array '
)
contact_question_update_102 = (
    'The "question_translations" parameter is invalid. "question_translations" cannot be empty'
)
contact_question_update_103 = (
    'The "question_translations" parameter is invalid. Each item in the array "question_translations" '
    'must be dictionary object. '
)
contact_question_update_104 = (
    'The "question_translations" parameter is invalid. "answer" is required for each item in the array '
    '"question_translations"'
)
contact_question_update_105 = (
    'The "question_translations" parameter is invalid. "chunk" is required for each item in the array '
    '"question_translations"'
)
contact_question_update_106 = (
    'The "question_translations" parameter is invalid. "language_id" is required for each item in the array '
    '"question_translations"'
)
contact_question_update_107 = (
    'The "question_translations" parameter is invalid. "language_id" in the array must be an integer.'
)
contact_question_update_108 = (
    'The "question_translations" parameter is invalid. "language_id" in the array must belong to valid language record'
)
contact_question_update_109 = (
    'The "question_translations" parameter is invalid. "question" is required for each item in the array '
    '"question_translations"'
)
contact_question_update_201 = (
    'You do not have permission to execute this method. You can only update a Question in Question Sets owned '
    'by your Member.'
)

# Delete
contact_question_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Question record.'
contact_question_delete_201 = (
    'You do not have permission to execute this method. You can only delete a Question in Question Sets owned '
    'by your Member.'
)
