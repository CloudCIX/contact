"""
Error codes for all the methods in Chatbot
"""

# List
contact_chatbot_list_001 = (
    'One or more of the sent search fields contains invalid values. Please check the sent parameters and ensure they'
    'match the required patterns.'
)

# Create
contact_chatbot_create_101 = 'The "api_key" parameter is invalid. "api_key" is required'
contact_chatbot_create_102 = (
    'The "api_key" parameter is invalid. "api_key" is required and cannot be longer than 64 characters'
)
contact_chatbot_create_103 = 'The "api_key" parameter is invalid. "api_key" should be a valid Address API Key'
contact_chatbot_create_104 = (
    'The "apply_intent_classification" parameter is invalid. The "apply_intent_classification" parameter must be a '
    'boolean'
)
contact_chatbot_create_105 = 'The "apply_reranking" parameter is invalid. "apply_reranking" must be a boolean.'
contact_chatbot_create_106 = 'The "bm25_limit" parameter is invalid. "bm25_limit" must be an integer.'
contact_chatbot_create_107 = (
    'The "bm25_limit" parameter is invalid. "bm25_limit" must be an integer between 1 and 50.'
)
contact_chatbot_create_108 = 'The "bm25_limit" parameter is invalid. "bm25_limit" must be between 1 and 50.'
contact_chatbot_create_109 = (
    'The "button_background_colour" is invalid. "button_background_colour" must be a valid Colour Hex Code'
)
contact_chatbot_create_110 = (
    'The "button_text" parameter is invalid. "button_text" cannot be longer than 50 characters.'
)
contact_chatbot_create_111 = (
    'The "button_text_colour" is invalid. "button_text_colour" must be a valid Colour Hex Code'
)
contact_chatbot_create_112 = (
    'The "chatbot_header_title" parameter is invalid. "chatbot_header_title" cannot be longer than 255 characters.'
)
contact_chatbot_create_113 = (
    'The "chatbot_header_description" parameter is invalid. "chatbot_header_description" cannot be',
    'longer than 255 characters.',
)
contact_chatbot_create_114 = 'The "chunk_overlap" parameter is invalid. "chunk_overlap" must be integer.'
contact_chatbot_create_115 = 'The "chunk_size" parameter is invalid. "chunk_size" must be integer.'
contact_chatbot_create_116 = (
    'The "cookie_consent_text" parameter is invalid. "cookie_consent_text" cannot be longer than 255 characters.'
)
contact_chatbot_create_117 = 'The "corpus_names" parameter is invalid. "corpus_names" must be a list'

contact_chatbot_create_119 = 'The "echo" parameter is invalid. The "echo" parameter must be a boolean'
contact_chatbot_create_120 = 'The "encoder" parameter is invalid. "encoder" is required.'
contact_chatbot_create_121 = (
    'The "encoder" parameter is invalid. "encoder" is required and must be an allowed choice. The supported choices '
    'are "dragon_plus", "test_encoder" and "use4".'
)
contact_chatbot_create_122 = (
    'The "horizontal_percentage" parameter is invalid. "horizontal_percentage" must be a decimal.'
)
contact_chatbot_create_123 = (
    'The "horizontal_percentage" parameter is invalid. "horizontal_percentage" must be a decimal between '
    '0 and 100.'
)
contact_chatbot_create_124 = 'The "horizontal_position" parameter is invalid. "horizontal_position" is required.'
contact_chatbot_create_125 = (
    'The "horizontal_position" parameter is invalid. "horizontal_position" is required and must be an allowed choice.'
    'The supported choices are "left" and "right".'
)
contact_chatbot_create_126 = (
    'The "intent_prompt" parameter is invalid. "intent_prompt" is required when "apply_intent_classification" '
    'enabled.'
)
contact_chatbot_create_127 = (
    'The "intent_prompt" parameter is invalid. "intent_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_create_128 = 'The "layout" parameter is invalid. "layout" is required.'
contact_chatbot_create_129 = (
    'The "layout" parameter is invalid. "layout" is required and must be an allowed choice. The supported choices '
    'are "window" and "widget".'
)
contact_chatbot_create_130 = 'The "max_tokens" parameter is invalid. "max_tokens" must be integer.'
contact_chatbot_create_131 = 'The "name" parameter is invalid. "name" is required.'
contact_chatbot_create_132 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_chatbot_create_133 = 'The "name" parameter is invalid. It should contain only [a-zA-Z0-9_-] characters.'
contact_chatbot_create_134 = 'The "name" parameter is invalid. Chatbot names must be unique within CloudCIX Contact.'
contact_chatbot_create_135 = 'The "nn_llm" parameter is invalid. "nn_llm" is required.'
contact_chatbot_create_136 = (
    'The "nn_llm" parameter is invalid. "nn_llm" is required and must be an allowed choice. The supported choices are '
    '"chatgpt4", "UCCIX-Mistral-24B", "uccix_instruct_70b", and "uccix_instruct".'
)
contact_chatbot_create_138 = (
    'The "pdf_scraping" parameter is invalid. "pdf_scraping" is required and must be an allowed choice. The supported '
    'choices are "pdf" and "pdf_hi_res".'
)
contact_chatbot_create_139 = 'The "reference_limit" parameter is invalid. "reference_limit" must be an integer.'
contact_chatbot_create_140 = (
    'The "reference_limit" parameter is invalid. "reference_limit" must be an integer between 1 and 50.'
)
contact_chatbot_create_141 = 'The "reference_limit" parameter is invalid. "reference_limit" must be between 1 and 50.'
contact_chatbot_create_142 = 'The "reranker" parameter is invalid. "reranker" is required.'
contact_chatbot_create_143 = (
    'The "reranker" parameter is invalid. "reranker" is required and must be an allowed choice. The supported choices '
    'are "chatgpt4", "UCCIX-Mistral-24B", "uccix_instruct_70b", "uccix_instruct" and "minilm-l-6-v2".'
)
contact_chatbot_create_144 = 'The "reranking_limit" parameter is invalid. "reranking_limit" must be an integer.'
contact_chatbot_create_145 = (
    'The "reranking_limit" parameter is invalid. "reranking_limit" must be an integer between 1 and 50.'
)
contact_chatbot_create_146 = 'The "reranking_limit" parameter is invalid. "reranking_limit" must be between 1 and 50.'
contact_chatbot_create_147 = 'The "similarity" parameter is invalid. "similarity" is required.'
contact_chatbot_create_148 = (
    'The "similarity" parameter is invalid. "similarity" is required and must be an allowed choice. The supported '
    'choices are "cosine_similarity", "dot_product", and "euclidean_distance".'
)
contact_chatbot_create_149 = (
    'The "smalltalk_prompt" parameter is invalid. "smalltalk_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_create_150 = (
    'The "system_prompt" parameter is invalid. "system_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_create_151 = 'The "temperature" parameter is invalid. "temperature" must be a decimal.'
contact_chatbot_create_152 = 'The "temperature" parameter is invalid. "temperature" must be a decimal between 0 and 1.'
contact_chatbot_create_153 = 'The "threshold" parameter is invalid. "threshold" must be a decimal.'
contact_chatbot_create_154 = (
    'The "user_prompt" parameter is invalid. "user_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_create_155 = 'The "vertical_percentage" parameter is invalid. "vertical_percentage" must be a decimal.'
contact_chatbot_create_156 = (
    'The "vertical_percentage" parameter is invalid. "vertical_percentage" must be a decimal between 0 and 100.'
)
contact_chatbot_create_157 = 'The "vertical_position" parameter is invalid. "vertical_position" is required.'
contact_chatbot_create_158 = (
    'The "vertical_position" parameter is invalid. "vertical_position" is required and must be an allowed choice.'
    'The supported choices are "top" and "bottom".'
)
contact_chatbot_create_159 = (
    'The "welcome_text" parameter is invalid. "welcome_text" cannot be longer than 255 characters.'
)
contact_chatbot_create_160 = (
    'The "logo" parameter is invalid. "logo" must be a dictionary with "name" and "data" as keys.'
)
contact_chatbot_create_161 = 'The "logo" parameter is invalid. "logo" must have both the "name" and "data" keys.'
contact_chatbot_create_162 = (
    'The "logo" parameter is invalid. The value for the "data" key should contain an image encoded in base64.'
)
contact_chatbot_create_163 = 'The "logo" parameter is invalid. The value for the "data" key cannot be empty.'
contact_chatbot_create_164 = 'The location to upload your "logo" to is not available. Please contact CloudCIX.'
contact_chatbot_create_165 = (
    'The "no_reference_answer" parameter is invalid. "no_reference_answer" cannot be longer than 10000 characters.'
)
contact_chatbot_create_201 = 'You do not have permission to make this request. Your Member must be self-managed.'

# Read
contact_chatbot_read_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Chatbot record.'

# Update
contact_chatbot_update_101 = 'The "api_key" parameter is invalid. "api_key" is required'
contact_chatbot_update_102 = (
    'The "api_key" parameter is invalid. "api_key" is required and cannot be longer than 64 characters'
)
contact_chatbot_update_103 = 'The "api_key" parameter is invalid. "api_key" should be a valid Address API Key'
contact_chatbot_update_104 = (
    'The "apply_intent_classification" parameter is invalid. The "apply_intent_classification" parameter must be a '
    'boolean.'
)
contact_chatbot_update_105 = (
    'The "apply_reranking" parameter is invalid. The "apply_reranking" parameter must be a boolean'
)
contact_chatbot_update_106 = 'The "bm25_limit" parameter is invalid. "bm25_limit" must be an integer.'
contact_chatbot_update_107 = (
    'The "bm25_limit" parameter is invalid. "bm25_limit" must be an integer between 1 and 50.'
)
contact_chatbot_update_108 = 'The "bm25_limit" parameter is invalid. "bm25_limit" must be between 1 and 50.'
contact_chatbot_update_109 = (
    'The "button_background_colour" is invalid. "button_background_colour" must be a valid Colour Hex Code.'
)
contact_chatbot_update_110 = (
    'The "button_text" parameter is invalid. "button_text" cannot be longer than 50 characters.'
)
contact_chatbot_update_111 = 'The "button_text_colour" is invalid. "button_text_colour" must be a valid Colour Hex Code'
contact_chatbot_update_112 = (
    'The "chatbot_header_title" parameter is invalid. "chatbot_header_title" cannot be longer than 255 characters.'
)
contact_chatbot_update_113 = (
    'The "chatbot_header_description" parameter is invalid. "chatbot_header_description" cannot be longer than 255 '
    'characters.'
)
contact_chatbot_update_114 = 'The "chunk_overlap" parameter is invalid. "chunk_overlap" must be integer.'
contact_chatbot_update_115 = 'The "chunk_size" parameter is invalid. "chunk_size" must be integer.'
contact_chatbot_update_116 = (
    'The "cookie_consent_text" parameter is invalid. "cookie_consent_text" cannot be longer than 255 characters.'
)
contact_chatbot_update_117 = 'The "corpus_names" parameter is invalid. "corpus_names" must be a list'

contact_chatbot_update_119 = 'The "echo" parameter is invalid. The "echo" parameter must be a boolean'
contact_chatbot_update_120 = 'The "encoder" parameter is invalid. "encoder" is required.'
contact_chatbot_update_121 = (
    'The "encoder" parameter is invalid. "encoder" is required and must be an allowed choice. The supported choices '
    'are "dragon_plus", "test_encoder" and "use4".'
)
contact_chatbot_update_122 = (
    'The "horizontal_percentage" parameter is invalid. "horizontal_percentage" must be a decimal.'
)
contact_chatbot_update_123 = (
    'The "horizontal_percentage" parameter is invalid. "button_position_from_bottom" must be a decimal between '
    '0 and 100.'
)
contact_chatbot_update_124 = 'The "horizontal_position" parameter is invalid. "horizontal_position" is required.'
contact_chatbot_update_125 = (
    'The "horizontal_position" parameter is invalid. "horizontal_position" is required and must be an allowed choice. '
    'The supported choices are "left" and "right".'
)
contact_chatbot_update_126 = (
    'The "intent_promot" parameter is invalid. "intent_prompt" is required when "apply_intent_classification" '
    'enabled.'
)
contact_chatbot_update_127 = (
    'The "intent_prompt" parameter is invalid. "intent_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_update_128 = 'The "layout" parameter is invalid. "layout" is required.'
contact_chatbot_update_129 = (
    'The "layout" parameter is invalid. "layout" is required and must be an allowed choice. The supported choices '
    'are "window" and "widget".'
)
contact_chatbot_update_130 = 'The "max_tokens" parameter is invalid. "max_tokens" must be integer.'
contact_chatbot_update_131 = 'The "name" parameter is invalid. "name" is required.'
contact_chatbot_update_132 = 'The "name" parameter is invalid. "name" cannot be longer than 50 characters.'
contact_chatbot_update_133 = 'The "name" parameter is invalid. It should contain only [a-zA-Z0-9_-] characters.'
contact_chatbot_update_134 = 'The "name" parameter is invalid. Chatbot names must be unique within CloudCIX Contact.'
contact_chatbot_update_135 = 'The "nn_llm" parameter is invalid. "nn_llm" is required.'
contact_chatbot_update_136 = (
    'The "nn_llm" parameter is invalid. "nn_llm" is required and must be an allowed choice. The supported choices are '
    '"chatgpt4", "UCCIX-Mistral-24B", "uccix_instruct_70b", and "uccix_instruct".'
)
contact_chatbot_update_138 = (
    'The "pdf_scraping" parameter is invalid. "pdf_scraping" is required and must be an allowed choice. The supported '
    'choices are "pdf" and "pdf_hi_res".'
)
contact_chatbot_update_139 = '"reference_limit" parameter is invalid. "reference_limit" is a required integer.'
contact_chatbot_update_140 = (
    '"reference_limit" parameter is invalid. "reference_limit" must be an integer between 1 and 50.'
)
contact_chatbot_update_141 = '"reference_limit" parameter is invalid. "reference_limit" must be between 1 and 50.'
contact_chatbot_update_142 = 'The "reranker" parameter is invalid. "reranker" is required.'
contact_chatbot_update_143 = (
    'The "reranker" parameter is invalid. "reranker" is required and must be an allowed choice. The supported choices '
    'are "chatgpt4", "UCCIX-Mistral-24B", "uccix_instruct_70b", "uccix_instruct" and "minilm-l-6-v2".'
)
contact_chatbot_update_144 = '"reranking_limit" parameter is invalid. "reranking_limit" is a required integer.'
contact_chatbot_update_145 = (
    '"reranking_limit" parameter is invalid. "reranking_limit" must be an integer between 1 and 50.'
)
contact_chatbot_update_146 = '"reranking_limit" parameter is invalid. "reranking_limit" must be between 1 and 50.'
contact_chatbot_update_147 = 'The "similarity" parameter is invalid. "similarity" is required.'
contact_chatbot_update_148 = (
    'The "similarity" parameter is invalid. "similarity" is required and must be an allowed choice. The supported '
    'choices are "cosine_similarity", "dot_product", and "euclidean_distance".'
)
contact_chatbot_update_149 = (
    'The "smalltalk_prompt" parameter is invalid. "smalltalk_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_update_150 = (
    'The "system_prompt" parameter is invalid. "system_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_update_151 = 'The "temperature" parameter is invalid. "temperature" must be a decimal.'
contact_chatbot_update_152 = 'The "temperature" parameter is invalid. "temperature" must be a decimal between 0 and 1.'
contact_chatbot_update_153 = 'The "threshold" parameter is invalid. "threshold" must be a decimal'
contact_chatbot_update_154 = (
    'The "user_prompt" parameter is invalid. "user_prompt" cannot be longer than 10000 characters.'
)
contact_chatbot_update_155 = 'The "vertical_percentage" parameter is invalid. "vertical_percentage" must be a decimal.'
contact_chatbot_update_156 = (
    'The "vertical_percentage" parameter is invalid. "vertical_percentage" must be a decimal between 0 and 100.'
)
contact_chatbot_update_157 = 'The "vertical_position" parameter is invalid. "vertical_position" is required.'
contact_chatbot_update_158 = (
    'The "vertical_position" parameter is invalid. "vertical_position" is required and must be an allowed choice.'
    'The supported choices are "bottom" and "top".'
)
contact_chatbot_update_159 = (
    'The "welcome_text" parameter is invalid. "welcome_text" cannot be longer than 255 characters.'
)
contact_chatbot_update_160 = (
    'The "logo" parameter is invalid. "logo" must be a dictionary with "name" and "data" as keys.'
)
contact_chatbot_update_161 = 'The "logo" parameter is invalid. "logo" must have both the "name" and "data" keys.'
contact_chatbot_update_162 = (
    'The "logo" parameter is invalid. The value for the "data" key should contain an image encoded in base64.'
)
contact_chatbot_update_163 = 'The "logo" parameter is invalid. The value for the "data" key cannot be empty.'
contact_chatbot_update_164 = 'The location to upload your "logo" to is not available. Please contact CloudCIX.'
contact_chatbot_update_165 = (
    'The "no_reference_answer" parameter is invalid. "no_reference_answer" cannot be longer than 10000 characters.'
)
contact_chatbot_update_001 = 'The "pk" path parameter is invalid. "pk" must belong to a valid Chatbot record.'
# Delete
contact_chatbot_delete_001 = 'The "pk" path parameters is invalid. "pk" must belong to a valid Chatbot record.'
