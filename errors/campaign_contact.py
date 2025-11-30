"""
Error Codes for all the Methods in the CampaignContact Service
"""

# Create
contact_campaign_contact_create_001 = 'The "pk" parameter is invalid. "pk" must belong to a valid Campaign record.'
contact_campaign_contact_create_101 = (
    'The "contacts" parameter is invalid.  "contacts" is required and must be an array.'
)
contact_campaign_contact_create_102 = 'The "contacts" parameter is invalid. "contacts" array cannot be empty.'
contact_campaign_contact_create_103 = (
    'The "contacts" parameter is invalid. Each item in the "contacts" list must be an integer.'
)
contact_campaign_contact_create_104 = (
    'The "contacts" parameter is invalid. All IDs in the list must correspond to a valid Contact record in your Member.'
)

# Update
contact_campaign_contact_update_001 = 'The "pk" parameter is invalid. "pk" must belong to a valid Campaign record.'
contact_campaign_contact_update_101 = (
    'The "contacts" parameter is invalid.  "contacts" is required and must be an array.'
)
contact_campaign_contact_update_102 = 'The "contacts" parameter is invalid. "contacts" array cannot be empty.'
contact_campaign_contact_update_103 = (
    'The "contacts" parameter is invalid. Each item in the "contacts" list must be an integer.'
)
contact_campaign_contact_update_104 = (
    'The "contacts" parameter is invalid. All IDs in the list must correspond to a valid Contact record in your Member.'
)
contact_campaign_contact_update_105 = (
    'The "responded" parameter is invalid. The "responded" parameter must be a boolean'
)

# Delete
contact_campaign_contact_delete_001 = 'The "pk" parameter is invalid. "pk" must belong to a valid Campaign record.'
contact_campaign_contact_delete_101 = (
    'The "contacts" parameter is invalid.  "contacts" is required and must be an array.'
)
contact_campaign_contact_delete_102 = 'The "contacts" parameter is invalid. "contacts" array cannot be empty.'
contact_campaign_contact_delete_103 = (
    'The "contacts" parameter is invalid. Each item in the "contacts" list must be an integer.'
)
contact_campaign_contact_delete_104 = (
    'The "contacts" parameter is invalid. All IDs in the list must correspond to a valid Contact record in your Member.'
)
