"""
Error codes for all the methods in Summary
"""
# List
contact_embeddings_list_001 = (
    'The sent data in the request is invalid. "hyperlink" key is required in the sent data.'
)
contact_embeddings_list_002 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)

# Create
contact_embeddings_create_001 = (
    'The "chatbot_name" path parameter is invalid. "chatbot_name" must belong to a valid Chatbot record.'
)
contact_embeddings_create_201 = (
    'Embeddings cannot be processed, the retrieval of the "content_type" for the "hyperlinks" in the Corpus is still '
    'in progress. Please wait for this to complete before requesting to embed the Corpus.'
)

# Read
contact_embeddings_read_001 = (
    'The "chatbot_name" or "chatbot_id" path parameter is invalid. "chatbot_name" & "chatbot_id" must belong '
    'to a valid Chatbot record.'
)
contact_embeddings_read_002 = (
    'The sent data in the request is invalid. "query" key is required in the sent data.'
)
