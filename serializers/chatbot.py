
# libs
import serpy
from contact.models import Chatbot

__all__ = [
    'ChatbotSerializer',
]


class ChatbotSerializer(serpy.Serializer):
    """
    api_key:
        description: The Address API Key used for ML Services.
        type: string
    apply_intent_classification:
        description: |
            If True, question sent to intent classification LLM.
        type: boolean
    apply_reranking:
        description: |
            If True, chunks sent to reranker.
        type: boolean
    bm25_limit:
        description: Number of best chunks between 1-10
        type: int
    button_background_colour:
        description: |
            The hex code for the background colour of the button embded on your website to launch the iframe for the
            Chatbot.
        type: string
    button_text:
        description: The text displayed on the button embded on your website to launch the iframe for the Chatbot.
        type: string
    button_text_colour:
        description: |
            The hex code for the colour of the text on the button embded on your website to launch the iframe for the
            Chatbot.
        type: string
    chatbot_header_title:
        description: |
            The title displayed in the header of the Chatbot interface.
        type: string
    chatbot_header_description:
        description: |
            The description displayed in the header of the Chatbot interface.
        type: string
    chunk_overlap:
        description: The number of characters that overlap between the consecutive chunks
        type: integer
    chunk_size:
        description: The maximum length ( number of characters ) of the chunk
        type: integer
    cookie_consent_text:
        description: The message shown to visitors about cookies when they log into the Chatbot.
        type: string
    corpus_names:
        description: An array of corpus names for chatbot.
        type: array
        items:
            type: string
    created:
        description: Timestamp, in ISO format, of when the Chatbot record was created.
        type: string
    echo:
        description: |
            If True, questions sent to the answer service will return the prompt that would be sent to the selected
            NN LLM. This is for debug purposes only.
        type: boolean
    encoder:
        description: The name of the Encoder Model of the Chatbot instance.
        type: string
    horizontal_percentage:
        description: |
            The percentage value from the left or right of your website to position the button embded on your website to
            launch the iframe for the Chatbot.
        type: string
        format: decimal
    horizontal_position:
        description: The horizontal position of the Chatbot UI.
        type: string
    id:
        description: ID of Chatbot record
        type: integer
    intent_prompt:
        description: The content of the prompt sent to the intent classification LLM
        type: string
    layout:
        description: The layout style of the Chatbot UI.
        type: string
    logo:
        description: The URL of the logo of the Chatbot.
        type: string
    max_tokens:
        description: This parameter controls the maximum number of tokens or words in the generated text.
        type: integer
    member_id:
        description: The ID of the member who owns the Chatbot
        type: integer
    name:
        description: The name of the Chatbot
        type: string
    nn_llm:
        description: The name of the Neural Network Large Language Model of the Chatbot instance.
        type: string
    nn_embedding:
        description: The neural network embeddings created
        type: string
    pdf_scraping:
        description: The Scraping method for PDF documents
        type: string
    reference_limit:
        description: Number of references between 1-50
        type: int
    no_reference_answer:
        description: |
            Fallback text to return when no similar references are found. If this is a non-empty string and the
            retrieval step yields zero chunks, this text is returned instead of calling the LLM.
        type: string
    reranker:
        description: The name of the Neural Network Large Language Model of the Reranker of Chatbot instance.
        type: string
    reranking_limit:
        description: Number of references between 1-50
        type: int
    similarity:
        description: The Vector Similarity formula for retrieval of Embeddings for Chatbot instance.
        type: string
    smalltalk_prompt:
        description: The content of the prompt sent to the smalltalk LLM
        type: string
    system_prompt:
        description: The content of the item with the role "system" added to the prompt sent to the LLM
        type: string
    temperature:
        description: |
            Temperature is a parameter that controls the "creativity" or randomness of the text generated. A higher
            temperature (e.g., 0.7) results in more diverse and creative output, while a lower temperature (e.g., 0.2)
            makes the output more deterministic and focused.
        type: string
        format: decimal
    threshold:
        description: The fixed Euclidean Distance to retrieve the Chunks
        type: string
        format: decimal
    updated:
        description: Timestamp, in ISO format, of when the Chatbot record was last updated.
        type: string
    uri:
        description:
            URL that can be used to run methods in the API associated with the Chatbot instance.
        type: string
    user_prompt:
        description: A message that gets appended to every question that the service sends to the LLM.
        type: string
    vertical_percentage:
        description: |
            The percentage value from the bottom or top of your website to position the button embded on your website to
            launch the iframe for the Chatbot.
        type: string
        format: decimal
    vertical_position:
        description: The vertical position of the Chatbot UI.
        type: string
    website_html:
        description: |
            The HTML to be embedded on your website to apply the Chatbot Login button with customized settings.
        type: string
    welcome_text:
        description: The text displayed on the page your website visitor sees when logging into your Chatbot.
        type: string
    """
    api_key = serpy.Field()
    apply_intent_classification = serpy.Field()
    apply_reranking = serpy.Field()
    bm25_limit = serpy.Field()
    button_background_colour = serpy.Field()
    horizontal_percentage = serpy.Field()
    horizontal_position = serpy.Field()
    vertical_percentage = serpy.Field()
    vertical_position = serpy.Field()
    button_text = serpy.Field()
    button_text_colour = serpy.Field()
    chunk_overlap = serpy.Field()
    chunk_size = serpy.Field()
    chatbot_header_title = serpy.Field()
    chatbot_header_description = serpy.Field()
    cookie_consent_text = serpy.Field()
    corpus_names = serpy.Field()
    created = serpy.Field(attr='created.isoformat', call=True)
    echo = serpy.Field()
    encoder = serpy.Field()
    id = serpy.Field()
    intent_prompt = serpy.Field()
    layout = serpy.Field()
    logo = serpy.Field()
    max_tokens = serpy.Field()
    member_id = serpy.Field()
    name = serpy.Field()
    nn_llm = serpy.Field()
    nn_embedding = serpy.Field()
    pdf_scraping = serpy.Field()
    reference_limit = serpy.Field()
    no_reference_answer = serpy.Field()
    reranker = serpy.Field()
    reranking_limit = serpy.Field()
    similarity = serpy.Field()
    system_prompt = serpy.Field()
    smalltalk_prompt = serpy.Field()
    temperature = serpy.Field()
    threshold = serpy.Field()
    updated = serpy.Field(attr='updated.isoformat', call=True)
    uri = serpy.Field(attr='get_absolute_url', call=True)
    user_prompt = serpy.Field()
    website_html = serpy.MethodField()
    welcome_text = serpy.Field()

    def get_website_html(self, obj: Chatbot):
        return getattr(obj, 'website_html', None)
