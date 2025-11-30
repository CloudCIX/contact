"""
error codes for all the methods in Contact
"""
# List
contact_contact_list_001 = (
    'The "chatbot_name" search parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_contact_list_002 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they '
    'match the required patterns.'
)

# Create
contact_contact_create_101 = 'The "address" parameter is invalid. "address" cannot be longer than 200 characters.'
contact_contact_create_102 = 'The "address2" parameter is invalid. "address2" cannot be longer than 100 characters.'
contact_contact_create_103 = 'The "city" parameter is invalid. "city" cannot be longer than 50 characters.'
contact_contact_create_104 = '"company_name" parameter is invalid. "company_name" cant be longer than 50 characters.'
contact_contact_create_105 = 'The "country_id" parameter is invalid. "country_id" must be an integer'
contact_contact_create_106 = 'The "country_id" parameter is invalid. "country_id" must belong to a valid Country'
contact_contact_create_107 = 'The "currently_visiting" parameter is invalid. "currently_visiting" must be a boolean.'
contact_contact_create_108 = 'The "member_id" parameter is invalid. "member_id" must belong to a valid Member.'
contact_contact_create_109 = 'The "email" parameter is invalid. "email" cannot be longer than 250 characters.'
contact_contact_create_110 = 'The "email" parameter is invalid. "email" should be valid'
contact_contact_create_111 = (
    'The "email" parameter is invalid. A Contact with this "email" already exists in your Member.'
)
contact_contact_create_112 = 'The "first_name" parameter is invalid. "first_name" is required.'
contact_contact_create_113 = 'The "first_name" parameter is invalid. "first_name" cannot be longer than 50 characters.'
contact_contact_create_114 = (
    'The "linkedin_url" parameter is invalid. "linkedin_url" cant be longer than 200 characters.'
)
contact_contact_create_115 = 'The "linkedin_url" parameter is invalid. "linkedin_url" should be a url.'
contact_contact_create_116 = (
    'The "password" parameter is invailid. A valid "password" must be at least 8 characters long and include at least '
    'one uppercase letter, one lowercase letter, one number and one special character from the following: '
    '# ? ! @ $ % ^ & * - '
)
contact_contact_create_117 = 'The "phone_number" parameter is invalid. "phone_number" must be an array.'
contact_contact_create_118 = 'The "phone_number" parameter is invalid. Each item in the array must be an object.'
contact_contact_create_119 = (
    'The "phone_number" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
contact_contact_create_120 = (
    'The "phone_number" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
contact_contact_create_121 = 'The "postcode" parameter is invalid. "postcode" cannot be longer than 20 characters.'
contact_contact_create_122 = 'The "subdivision_id" parameter is invalid. "subdivision_id" must be an integer.'
contact_contact_create_123 = (
    'The "subdivision_id" parameter is invalid. "subdivision_id" must belong to a valid Subdivision in the chosen '
    'Country.'
)
contact_contact_create_124 = 'The "surname" parameter is invalid. "surname" is required and must be a string.'
contact_contact_create_125 = 'The "surname" parameter is invalid. "surname" cannot be longer than 50 characters.'
contact_contact_create_126 = 'The "title" parameter is invalid. "title" cannot be longer than 100 characters.'
contact_contact_create_127 = 'The "website" parameter is invalid. "website" cannot be longer than 50 characters.'
contact_contact_create_128 = 'The "website" parameter is invalid. "website" should be a valid url.'
contact_contact_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'
contact_contact_create_202 = (
    'You do not have permission to make this request. You cannot create a Contact for another Member'
)
# Read
contact_contact_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Contact record.'
contact_contact_read_201 = (
    'You do not have permission to make this request. You cannot read a Contact for another Member'
)
# Update
contact_contact_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Contact record.'
contact_contact_update_101 = 'The "address" parameter is invalid. "address" cannot be longer than 200 characters.'
contact_contact_update_102 = 'The "address2" parameter is invalid. "address2" cannot be longer than 100 characters.'
contact_contact_update_103 = 'The "city" parameter is invalid. "city" cannot be longer than 50 characters.'
contact_contact_update_104 = '"company_name" parameter is invalid. "company_name" cant be longer than 50 characters.'
contact_contact_update_105 = 'The "country_id" parameter is invalid. "country_id" must be an integer'
contact_contact_update_106 = 'The "country_id" parameter is invalid. "country_id" must belong to a valid Country'
contact_contact_update_107 = 'The "currently_visiting" parameter is invalid. "currently_visiting" must be a boolean.'
contact_contact_update_108 = 'The "email" parameter is invalid. "email" cannot be longer than 250 characters.'
contact_contact_update_109 = 'The "email" parameter is invalid. "email" should be valid'
contact_contact_update_110 = (
    'The "email" parameter is invalid. A Contact with this "email" already exists in your Member.'
)
contact_contact_update_111 = 'The "first_name" parameter is invalid. "first_name" is required and must be a string.'
contact_contact_update_112 = 'The "first_name" parameter is invalid. "first_name" cannot be longer than 50 characters.'
contact_contact_update_113 = (
    'The "linkedin_url" parameter is invalid. "linkedin_url" cant be longer than 200 characters.'
)
contact_contact_update_114 = 'The "linkedin_url" parameter is invalid. "linkedin_url" should be a url.'
contact_contact_update_115 = 'The "opt_out" parameter is invalid. "opt_out" must be a boolean.'
contact_contact_update_116 = (
    'The "password" parameter is invailid. A valid "password" must be at least 8 characters long and include at least '
    'one uppercase letter, one lowercase letter, one number and one special character from the following: '
    '# ? ! @ $ % ^ & * - '
)
contact_contact_update_117 = 'The "phone_number" parameter is invalid. "phone_number" must be an array.'
contact_contact_update_118 = 'The "phone_number" parameter is invalid. Each item in the array must be an object.'
contact_contact_update_119 = (
    'The "phone_number" parameter is invalid. Each item in the array must have both the "name" and "number" keys.'
)
contact_contact_update_120 = (
    'The "phone_number" parameter is invalid. One of the sent values for "number" is not a valid phone number.'
)
contact_contact_update_121 = 'The "postcode" parameter is invalid. "postcode" cannot be longer than 20 characters.'
contact_contact_update_122 = 'The "subdivision_id" parameter is invalid. "subdivision_id" must be an integer.'
contact_contact_update_123 = (
    'The "subdivision_id" parameter is invalid. "subdivision_id" must belong to a valid Subdivision in the chosen '
    'Country.'
)
contact_contact_update_124 = 'The "surname" parameter is invalid. "surname" is required and must be a string.'
contact_contact_update_125 = 'The "surname" parameter is invalid. "surname" cannot be longer than 50 characters.'
contact_contact_update_126 = 'The "title" parameter is invalid. "title" cannot be longer than 100 characters.'
contact_contact_update_127 = 'The "website" parameter is invalid. "website" cannot be longer than 50 characters.'
contact_contact_update_128 = 'The "website" parameter is invalid. "website" should be a valid url.'
contact_contact_update_201 = (
    'You do not have permission to make this request. You cannot update a Contact for another Member'
)
# Delete
contact_contact_delete_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Contact record.'
