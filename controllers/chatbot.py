# stdlib
import base64
import binascii
import re
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Union
from uuid import uuid4

# libs
from cloudcix.api.membership import Membership
from cloudcix_rest.controllers import ControllerBase
from django.conf import settings

# local
from ..models import Chatbot

__all__ = [
    'ChatbotListController',
    'ChatbotCreateController',
    'ChatbotUpdateController',
]

ENCODER_CHOICES = dict(Chatbot.ENCODER_CHOICES)
HORIZONTAL_POSITION_CHOICES = dict(Chatbot.HORIZONTAL_POSITION_CHOICES)
LAYOUT_CHOICES = dict(Chatbot.LAYOUT_CHOICES)
NN_LLM_CHOICES = dict(Chatbot.NN_LLM_CHOICES)
NAME_ALLOWED_CHARS_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')
PDF_SCRAPING_CHOICES = dict(Chatbot.PDF_SCRAPING_CHOICES)
RERANKER_CHOICES = dict(Chatbot.RERANKER_CHOICES)
SIMILARITY_CHOICES = dict(Chatbot.SIMILARITY_CHOICES)
VERTICAL_POSITION_CHOICES = dict(Chatbot.VERTICAL_POSITION_CHOICES)


class ChatbotListController(ControllerBase):
    """
    Validates User data used to list Chatbot records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'created',
            'id',
        )
        search_fields = {
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class ChatbotCreateController(ControllerBase):
    """
    Validates user data used to create Chatbot records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Chatbot
        validation_order = (
            'api_key',
            'apply_intent_classification',
            'apply_reranking',
            'bm25_limit',
            'button_background_colour',
            'button_text',
            'button_text_colour',
            'chatbot_header_title',
            'chatbot_header_description',
            'chunk_overlap',
            'chunk_size',
            'cookie_consent_text',
            'corpus_names',
            'echo',
            'encoder',
            'horizontal_percentage',
            'horizontal_position',
            'intent_prompt',
            'layout',
            'max_tokens',
            'name',
            'nn_llm',
            'pdf_scraping',
            'reference_limit',
            'no_reference_answer',
            'reranker',
            'reranking_limit',
            'similarity',
            'smalltalk_prompt',
            'system_prompt',
            'temperature',
            'threshold',
            'user_prompt',
            'vertical_position',
            'vertical_percentage',
            'welcome_text',
            'logo',
        )

    def validate_api_key(self, api_key: Optional[str]) -> Optional[str]:
        """
        description: The Address API Key for AI/ML operations
        type: string
        """
        if api_key is None:
            api_key = ''

        api_key = api_key.strip()

        if len(api_key) == 0:
            return 'contact_chatbot_create_101'

        if len(api_key) > self.get_field('api_key').max_length:
            return 'contact_chatbot_create_102'

        response = Membership.api_key.head(pk=api_key)

        if response.status_code != 200:
            return 'contact_chatbot_create_103'

        self.cleaned_data['api_key'] = api_key
        return None

    def validate_apply_intent_classification(self, apply_intent_classification: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, chunks are sent to intent clasifier LLM.
        required: false
        type: boolean
        """
        if apply_intent_classification is None:
            return None
        if not isinstance(apply_intent_classification, bool):
            return 'contact_chatbot_create_104'
        self.cleaned_data['apply_intent_classification'] = apply_intent_classification
        return None

    def validate_apply_reranking(self, apply_reranking: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, chunks are sent to reranker.
        required: false
        type: boolean
        """
        if apply_reranking is None:
            return None
        if not isinstance(apply_reranking, bool):
            return 'contact_chatbot_create_105'
        self.cleaned_data['apply_reranking'] = apply_reranking
        return None

    def validate_bm25_limit(self, bm25_limit: int) -> Optional[str]:
        """
        description: Number of best chunks between 1 and 10.
        type: integer
        """
        if bm25_limit is None:
            return 'contact_chatbot_create_106'
        try:
            bm25_limit = int(bm25_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_create_107'
        if bm25_limit < 0 or bm25_limit > 50:
            return 'contact_chatbot_create_108'

        self.cleaned_data['bm25_limit'] = bm25_limit
        return None

    def validate_button_background_colour(self, button_background_colour: Optional[str]) -> Optional[str]:
        """
        description: |
            The hex code for the background colour of the button embded on your website to launch the iframe for the
            Chatbot.  If not sent the default value #47b2e4 (light blue) will be used.
        required: false
        type: string
        """
        if not button_background_colour:
            return None

        if not re.search(Chatbot.HEX_CODE_REGEX, button_background_colour):
            return 'contact_chatbot_create_109'

        self.cleaned_data['button_background_colour'] = button_background_colour
        return None

    def validate_button_text(self, button_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the button embded on your website to launch the iframe for the Chatbot.
            If not sent the default value "Chatbot" will be used.
        required: false
        type: string
        """
        if not button_text:
            return None

        if len(button_text) > self.get_field('button_text').max_length:
            return 'contact_chatbot_create_110'

        self.cleaned_data['button_text'] = button_text
        return None

    def validate_button_text_colour(self, button_text_colour: Optional[str]) -> Optional[str]:
        """
        description: |
            The hex code for the colour of the text on the button embded on your website to launch the iframe for the
            Chatbot. If not sent the default value #FFFFFF (white) will be used.
        required: false
        type: string
        """
        if not button_text_colour:
            return None

        if not re.search(Chatbot.HEX_CODE_REGEX, button_text_colour):
            return 'contact_chatbot_create_111'

        self.cleaned_data['button_text_colour'] = button_text_colour
        return None

    def validate_chatbot_header_title(self, chatbot_header_title: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed as the chatbot's header title when the chatbot layout is set to "widget".
            This is displayed only if the title is not blank.
        required: false
        type: string
        """
        if chatbot_header_title is None:
            return None

        chatbot_header_title = str(chatbot_header_title).strip()

        if len(chatbot_header_title) > self.get_field('chatbot_header_title').max_length:
            return 'contact_chatbot_create_112'

        self.cleaned_data['chatbot_header_title'] = chatbot_header_title
        return None

    def validate_chatbot_header_description(self, chatbot_header_description: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed as the chatbot's header description when the chatbot layout is set to "widget".
            This is displayed only if the description is not blank.
        required: false
        type: string
        """
        if chatbot_header_description is None:
            return None

        chatbot_header_description = str(chatbot_header_description).strip()

        if len(chatbot_header_description) > self.get_field('chatbot_header_description').max_length:
            return 'contact_chatbot_create_113'

        self.cleaned_data['chatbot_header_description'] = chatbot_header_description
        return None

    def validate_chunk_overlap(self, chunk_overlap: Optional[int]) -> Optional[str]:
        """
        description: The number of characters that overlap between the consecutive chunks
        required: false
        type: integer
        """
        if chunk_overlap is None:
            return None

        try:
            chunk_overlap = int(chunk_overlap)
        except (ValueError, TypeError):
            return 'contact_chatbot_create_114'

        self.cleaned_data['chunk_overlap'] = chunk_overlap
        return None

    def validate_chunk_size(self, chunk_size: Optional[int]) -> Optional[str]:
        """
        description: The maximum length (number of characters) of the chunk
        required: false
        type: integer
        """
        if chunk_size is None:
            return None

        try:
            chunk_size = int(chunk_size)
        except (ValueError, TypeError):
            return 'contact_chatbot_create_115'

        self.cleaned_data['chunk_size'] = chunk_size
        return None

    def validate_cookie_consent_text(self, cookie_consent_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the page when your website visitor sees the cookie popup open.
            If not sent the default value "This Chatbot uses only essential cookies.
                You must accept the essential cookies to use this Chatbot." will be used.
        required: false
        type: string
        """
        if not cookie_consent_text:
            return None

        if len(cookie_consent_text) > self.get_field('cookie_consent_text').max_length:
            return 'contact_chatbot_create_116'

        self.cleaned_data['cookie_consent_text'] = cookie_consent_text
        return None

    def validate_corpus_names(self, corpus_names: Optional[List[str]]) -> Optional[str]:
        """
        description: An array of Corpus Names that can be used by Chatbot
        type: array
        items:
            type: string
        required: false
        """
        corpus_names = corpus_names or []

        if not isinstance(corpus_names, list):
            return 'contact_chatbot_create_117'

        corpus_names = [str(i).strip() for i in corpus_names if str(i).strip()]

        self.cleaned_data['corpus_names'] = list(corpus_names)
        return None

    def validate_echo(self, echo: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, questions sent to the answer service will return the prompt that would be sent to the selected
            NN LLM. This is for debug purposes only.
        required: false
        type: boolean
        """
        if echo is None:
            return None
        if not isinstance(echo, bool):
            return 'contact_chatbot_create_119'
        self.cleaned_data['echo'] = echo
        return None

    def validate_encoder(self, encoder: Optional[str]) -> Optional[str]:
        """
        description: The Encoder model for the chatbot
        type: string
        """
        if encoder is None:
            return 'contact_chatbot_create_120'

        if encoder not in ENCODER_CHOICES:
            return 'contact_chatbot_create_121'

        self.cleaned_data['encoder'] = encoder
        return None

    def validate_horizontal_percentage(self, horizontal_percentage: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            The percentage value from the left or right of your website to position the button embedded on your website
            to launch the iframe for the Chatbot. If not sent the default value 3% will be used.
        required: false
        type: string
        format: Decimal
        """
        if not horizontal_percentage:
            return None

        try:
            horizontal_percentage = Decimal(str(horizontal_percentage))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_create_122'

        if horizontal_percentage < 0 or horizontal_percentage > 100:
            return 'contact_chatbot_create_123'

        self.cleaned_data['horizontal_percentage'] = horizontal_percentage
        return None

    def validate_horizontal_position(self, horizontal_position: Optional[str]) -> Optional[str]:
        """
        description: Positions the Chatbot button from the left or right side of the page.
        type: string
        """
        if horizontal_position is None:
            return 'contact_chatbot_create_124'

        if horizontal_position not in HORIZONTAL_POSITION_CHOICES:
            return 'contact_chatbot_create_125'

        self.cleaned_data['horizontal_position'] = horizontal_position
        return None

    def validate_intent_prompt(self, intent_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the prompt sent to the intention LLM.
        type: string
        required: false
        """
        if 'apply_intent_classification' not in self.cleaned_data:
            return None

        if intent_prompt is None:
            if self.cleaned_data['apply_intent_classification']:
                return 'contact_chatbot_create_126'
            return None

        intent_prompt = str(intent_prompt).strip()

        if len(intent_prompt) > self.get_field('intent_prompt').max_length:
            return 'contact_chatbot_create_127'

        self.cleaned_data['intent_prompt'] = intent_prompt
        return None

    def validate_layout(self, layout: Optional[str]) -> Optional[str]:
        """
        description: The Layout model for the chatbot
        type: string
        """
        if layout is None:
            return 'contact_chatbot_create_128'

        if layout not in LAYOUT_CHOICES:
            return 'contact_chatbot_create_129'

        self.cleaned_data['layout'] = layout
        return None

    def validate_max_tokens(self, max_tokens: int) -> Optional[str]:
        """
        description: Getting the response up to max_tokens
        type: integer
        """
        if not max_tokens:
            return None
        try:
            max_tokens = int(max_tokens)
        except (TypeError, ValueError):
            return 'contact_chatbot_create_130'
        self.cleaned_data['max_tokens'] = max_tokens
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: Name of the Chatbot used to form part of the URL
        type: string
        """
        if name is None:
            name = ''

        name = str(name).replace(' ', '')

        if len(name) == 0:
            return 'contact_chatbot_create_131'

        if len(name) > self.get_field('name').max_length:
            return 'contact_chatbot_create_132'

        if (NAME_ALLOWED_CHARS_REGEX.match(name) is None):
            return 'contact_chatbot_create_133'

        if Chatbot.objects.filter(name__iexact=name).exists():
            return 'contact_chatbot_create_134'

        self.cleaned_data['name'] = name
        return None

    def validate_nn_llm(self, nn_llm: Optional[str]) -> Optional[str]:
        """
        description: The Neural Network Large Language model for the chatbot
        type: string
        """
        if nn_llm is None:
            return 'contact_chatbot_create_135'

        if nn_llm not in NN_LLM_CHOICES:
            return 'contact_chatbot_create_136'

        self.cleaned_data['nn_llm'] = nn_llm
        return None

    def validate_pdf_scraping(self, pdf_scraping: str) -> Optional[str]:
        """
        description: The scraping method for PDF documents
        type: string
        required: false
        """
        if pdf_scraping is None:
            pdf_scraping = Chatbot.BASIC_SCRAPING

        if pdf_scraping not in PDF_SCRAPING_CHOICES:
            return 'contact_chatbot_create_138'

        self.cleaned_data['pdf_scraping'] = pdf_scraping
        return None

    def validate_reference_limit(self, reference_limit: int) -> Optional[str]:
        """
        description: Number of references between 1 and 10
        type: integer
        """
        if not reference_limit:
            return 'contact_chatbot_create_139'
        try:
            reference_limit = int(reference_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_create_140'
        if reference_limit < 1 or reference_limit > 50:
            return 'contact_chatbot_create_141'

        self.cleaned_data['reference_limit'] = reference_limit
        return None

    def validate_reranker(self, reranker: Optional[str]) -> Optional[str]:
        """
        description: The Neural Network Large Language model for the reranker
        type: string
        """
        if reranker is None:
            return 'contact_chatbot_create_142'

        if reranker not in RERANKER_CHOICES:
            return 'contact_chatbot_create_143'

        self.cleaned_data['reranker'] = reranker
        return None

    def validate_reranking_limit(self, reranking_limit: int) -> Optional[str]:
        """
        description: Number of references between 1 and 50
        type: integer
        """
        if not reranking_limit:
            return 'contact_chatbot_create_144'
        try:
            reranking_limit = int(reranking_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_create_145'
        if reranking_limit < 1 or reranking_limit > 50:
            return 'contact_chatbot_create_146'

        self.cleaned_data['reranking_limit'] = reranking_limit
        return None

    def validate_similarity(self, similarity: Optional[str]) -> Optional[str]:
        """
        description: The Vector Similarity formula for the retrieval of Embeddings for the chatbot
        type: string
        """
        if similarity is None:
            return 'contact_chatbot_create_147'

        if similarity not in SIMILARITY_CHOICES:
            return 'contact_chatbot_create_148'

        self.cleaned_data['similarity'] = similarity
        return None

    def validate_smalltalk_prompt(self, smalltalk_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the prompt sent to the smalltalk LLM.
        type: string
        required: false
        """
        if smalltalk_prompt is None:
            return None

        smalltalk_prompt = str(smalltalk_prompt).strip()

        if len(smalltalk_prompt) > self.get_field('smalltalk_prompt').max_length:
            return 'contact_chatbot_create_149'

        self.cleaned_data['smalltalk_prompt'] = smalltalk_prompt
        return None

    def validate_system_prompt(self, system_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the item with the role "system" added to the prompt sent to the LLM.
        type: string
        required: false
        """
        if system_prompt is None:
            return None

        system_prompt = str(system_prompt).strip()

        if len(system_prompt) > self.get_field('system_prompt').max_length:
            return 'contact_chatbot_create_150'

        self.cleaned_data['system_prompt'] = system_prompt
        return None

    def validate_no_reference_answer(self, no_reference_answer: Optional[str]) -> Optional[str]:
        """
        description: The fallback answer returned when no references are found.
        type: string
        required: false
        """
        if no_reference_answer is None:
            return None

        no_reference_answer = str(no_reference_answer).strip()

        if len(no_reference_answer) > self.get_field('no_reference_answer').max_length:
            return 'contact_chatbot_create_165'

        self.cleaned_data['no_reference_answer'] = no_reference_answer
        return None

    def validate_temperature(self, temperature: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            Temperature is a parameter that controls the "creativity" or randomness of the text generated. A higher
            temperature (e.g., 0.7) results in more diverse and creative output, while a lower temperature (e.g., 0.2)
            makes the output more deterministic and focused.
        type: string
        format: decimal
        """
        if not temperature:
            return None
        try:
            temperature = Decimal(str(temperature))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_create_151'

        if temperature < 0 or temperature > 1:
            return 'contact_chatbot_create_152'

        self.cleaned_data['temperature'] = temperature
        return None

    def validate_threshold(self, threshold: Optional[Decimal]) -> Optional[str]:
        """
        description: The fixed Euclidean Distance in order to retrieve the chunks
        required: false
        type: string
        format: decimal
        """
        if not threshold:
            return None
        try:
            threshold = Decimal(str(threshold))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_create_153'

        self.cleaned_data['threshold'] = threshold
        return None

    def validate_user_prompt(self, user_prompt: Optional[str]) -> Optional[str]:
        """
        description: The value to be appended to questions sent to the LLM in the constructed prompt.
        type: string
        """
        if user_prompt is None:
            return None

        user_prompt = str(user_prompt).strip()

        if len(user_prompt) > self.get_field('user_prompt').max_length:
            return 'contact_chatbot_create_154'

        self.cleaned_data['user_prompt'] = user_prompt
        return None

    def validate_vertical_percentage(self, vertical_percentage: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            The percentage value from the bottom or top of your website to position the button embedded on your website
            to launch the iframe for the Chatbot. If not sent the default value 2% will be used.
        required: false
        type: string
        """
        if not vertical_percentage:
            return None

        try:
            vertical_percentage = Decimal(str(vertical_percentage))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_create_155'

        if vertical_percentage < 0 or vertical_percentage > 100:
            return 'contact_chatbot_create_156'

        self.cleaned_data['vertical_percentage'] = vertical_percentage
        return None

    def validate_vertical_position(self, vertical_position: Optional[str]) -> Optional[str]:
        """
        description: Positions the Chatbot button from the bottom or top side of the page.
        type: string
        """
        if vertical_position is None:
            return 'contact_chatbot_create_157'

        if vertical_position not in VERTICAL_POSITION_CHOICES:
            return 'contact_chatbot_create_158'

        self.cleaned_data['vertical_position'] = vertical_position
        return None

    def validate_welcome_text(self, welcome_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the page your website visitor sees when logging into your Chatbot.
            If not sent the default value "Please login to Chatbot" will be used.
        required: false
        type: string
        """
        if not welcome_text:
            return None

        if len(welcome_text) > self.get_field('welcome_text').max_length:
            return 'contact_chatbot_create_159'

        self.cleaned_data['welcome_text'] = welcome_text
        return None

    def validate_logo(self, logo: Optional[Union[Dict[str, str], str]]):
        """
        description: The data of the logo to use on the Chatbot iframe.
        type: object
        properties:
            name:
                description: name of the logo file
                type: string
            data:
                description: The logo encoded in base64
                type: string
        required: false
        """
        if logo is None:
            return None

        if not isinstance(logo, dict):
            return 'contact_chatbot_create_160'

        try:
            filename: str = f'{uuid4()}.{logo["name"].split(".")[1]}'
            data: bytes = base64.b64decode(logo['data'])
            filesize: int = len(data)
        except KeyError:
            return 'contact_chatbot_create_161'
        except binascii.Error:
            return 'contact_chatbot_create_162'

        # Check that our variables are valid
        if filesize == 0:
            return 'contact_chatbot_create_163'

        # If any errors have occurred we are not going to upload logo
        if len(self._errors) > 0:
            return None

        if settings.CHATBOT_URL is None:  # pragma: no cover
            return 'contact_chatbot_create_164'

        chatbot_name = self.cleaned_data['name']
        # TODO: Upload image to CHATBOT_LOGO_LOCATION

        logo = f'{settings.CHATBOT_URL.rstrip("/")}/{chatbot_name}/{filename}'

        self.cleaned_data['logo'] = logo
        return None


class ChatbotUpdateController(ControllerBase):
    """
    Validates user data used to update Chatbot records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Chatbot
        validation_order = (
            'api_key',
            'apply_intent_classification',
            'apply_reranking',
            'bm25_limit',
            'button_background_colour',
            'button_text',
            'button_text_colour',
            'chatbot_header_title',
            'chatbot_header_description',
            'chunk_overlap',
            'chunk_size',
            'cookie_consent_text',
            'corpus_names',
            'echo',
            'encoder',
            'horizontal_percentage',
            'horizontal_position',
            'intent_prompt',
            'layout',
            'max_tokens',
            'name',
            'nn_llm',
            'pdf_scraping',
            'reference_limit',
            'reranker',
            'reranking_limit',
            'similarity',
            'smalltalk_prompt',
            'system_prompt',
            'temperature',
            'threshold',
            'no_reference_answer',
            'user_prompt',
            'vertical_percentage',
            'vertical_position',
            'welcome_text',
            'logo',
        )

    def validate_api_key(self, api_key: Optional[str]) -> Optional[str]:
        """
        description: The Address API Key for AI/ML operations
        type: string
        """
        if api_key is None:
            api_key = ''

        api_key = api_key.strip()

        if len(api_key) == 0:
            return 'contact_chatbot_update_101'

        if len(api_key) > self.get_field('api_key').max_length:
            return 'contact_chatbot_update_102'

        response = Membership.api_key.head(pk=api_key)

        if response.status_code != 200:
            return 'contact_chatbot_update_103'

        self.cleaned_data['api_key'] = api_key
        return None

    def validate_apply_intent_classification(self, apply_intent_classification: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, question is sent to intent classifier LLM
        required: false
        type: boolean
        """
        if apply_intent_classification is None:
            return None
        if not isinstance(apply_intent_classification, bool):
            return 'contact_chatbot_update_104'
        self.cleaned_data['apply_intent_classification'] = apply_intent_classification
        return None

    def validate_apply_reranking(self, apply_reranking: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, chunks are sent to reranker
        required: false
        type: boolean
        """
        if apply_reranking is None:
            return None
        if not isinstance(apply_reranking, bool):
            return 'contact_chatbot_update_105'
        self.cleaned_data['apply_reranking'] = apply_reranking
        return None

    def validate_bm25_limit(self, bm25_limit: int) -> Optional[str]:
        """
        description: Number of best chunks between 1 and 10
        type: integer
        """
        if bm25_limit is None:
            return 'contact_chatbot_update_106'
        try:
            bm25_limit = int(bm25_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_update_107'
        if bm25_limit < 0 or bm25_limit > 50:
            return 'contact_chatbot_update_108'

        self.cleaned_data['bm25_limit'] = bm25_limit
        return None

    def validate_button_background_colour(self, button_background_colour: Optional[str]) -> Optional[str]:
        """
        description: |
            The hex code for the background colour of the button embded on your website to launch the iframe for the
            Chatbot.
        required: false
        type: string
        """
        if not button_background_colour:
            return None

        if not re.search(Chatbot.HEX_CODE_REGEX, button_background_colour):
            return 'contact_chatbot_update_109'

        self.cleaned_data['button_background_colour'] = button_background_colour
        return None

    def validate_button_text(self, button_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the button embded on your website to launch the iframe for the Chatbot.
        required: false
        type: string
        """
        if not button_text:
            return None

        if len(button_text) > self.get_field('button_text').max_length:
            return 'contact_chatbot_update_110'

        self.cleaned_data['button_text'] = button_text
        return None

    def validate_button_text_colour(self, button_text_colour: Optional[str]) -> Optional[str]:
        """
        description: |
            The hex code for the colour of the text on the button embded on your website to launch the iframe for the
            Chatbot.
        required: false
        type: string
        """
        if not button_text_colour:
            return None

        if not re.search(Chatbot.HEX_CODE_REGEX, button_text_colour):
            return 'contact_chatbot_update_111'

        self.cleaned_data['button_text_colour'] = button_text_colour
        return None

    def validate_chatbot_header_title(self, chatbot_header_title: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed as the chatbot's header title when the chatbot layout is set to "widget".
            This is displayed only if the title is not blank.
        required: false
        type: string
        """
        if chatbot_header_title is None:
            chatbot_header_title = ''

        chatbot_header_title = str(chatbot_header_title).strip()

        if len(chatbot_header_title) > self.get_field('chatbot_header_title').max_length:
            return 'contact_chatbot_update_112'

        self.cleaned_data['chatbot_header_title'] = chatbot_header_title
        return None

    def validate_chatbot_header_description(self, chatbot_header_description: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed as the chatbot's header description when the chatbot layout is set to "widget".
            This is displayed only if the description is not blank.
        required: false
        type: string
        """
        if chatbot_header_description is None:
            chatbot_header_description = ''

        chatbot_header_description = str(chatbot_header_description).strip()

        if len(chatbot_header_description) > self.get_field('chatbot_header_description').max_length:
            return 'contact_chatbot_update_113'

        self.cleaned_data['chatbot_header_description'] = chatbot_header_description
        return None

    def validate_chunk_overlap(self, chunk_overlap: Optional[int]) -> Optional[str]:
        """
        description: The number of characters that overlap between the consecutive chunks
        required: false
        type: integer
        """
        if chunk_overlap is None:
            return None

        try:
            chunk_overlap = int(chunk_overlap)
        except (ValueError, TypeError):
            return 'contact_chatbot_update_114'

        self.cleaned_data['chunk_overlap'] = chunk_overlap
        return None

    def validate_chunk_size(self, chunk_size: Optional[int]) -> Optional[str]:
        """
        description: The maximum length (number of characters) of the chunk
        required: false
        type: integer
        """
        if chunk_size is None:
            return None

        try:
            chunk_size = int(chunk_size)
        except (ValueError, TypeError):
            return 'contact_chatbot_update_115'

        self.cleaned_data['chunk_size'] = chunk_size
        return None

    def validate_cookie_consent_text(self, cookie_consent_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the page when your website visitor sees the cookie popup open.
            If not sent the default value "This Chatbot uses only essential cookies.
                You must accept the essential cookies to use this Chatbot." will be used.
        required: false
        type: string
        """
        if not cookie_consent_text:
            return None

        if len(cookie_consent_text) > self.get_field('cookie_consent_text').max_length:
            return 'contact_chatbot_update_116'

        self.cleaned_data['cookie_consent_text'] = cookie_consent_text
        return None

    def validate_corpus_names(self, corpus_names: Optional[List[str]]) -> Optional[str]:
        """
        description: The array of Corpus Names to be used by the Chatbot
        type: array
        items:
            type: string
        required: false
        """
        if corpus_names is None:
            corpus_names = []

        if not isinstance(corpus_names, list):
            return 'contact_chatbot_update_117'

        corpus_names = [str(i).strip() for i in corpus_names if str(i).strip()]

        self.cleaned_data['corpus_names'] = list(corpus_names)
        return None

    def validate_echo(self, echo: Optional[bool]) -> Optional[str]:
        """
        description: |
            If True, questions sent to the answer service will return the prompt that would be sent to the selected
            NN LLM. This is for debug purposes only.
        required: false
        type: boolean
        """
        if echo is None:
            return None
        if not isinstance(echo, bool):
            return 'contact_chatbot_update_119'
        self.cleaned_data['echo'] = echo
        return None

    def validate_encoder(self, encoder: Optional[str]) -> Optional[str]:
        """
        description: The Encoder model for the chatbot
        type: string
        """
        if encoder is None:
            return 'contact_chatbot_update_120'

        if encoder not in ENCODER_CHOICES:
            return 'contact_chatbot_update_121'

        self.cleaned_data['encoder'] = encoder
        return None

    def validate_horizontal_percentage(self, horizontal_percentage: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            The percentage value from the left or right of your website to position the button embedded on your website
            to launch the iframe for the Chatbot. If not sent the default value 3% will be used.
        required: false
        type: string
        """
        if not horizontal_percentage:
            return None

        try:
            horizontal_percentage = Decimal(str(horizontal_percentage))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_update_122'

        if horizontal_percentage < 0 or horizontal_percentage > 100:
            return 'contact_chatbot_update_123'

        self.cleaned_data['horizontal_percentage'] = horizontal_percentage
        return None

    def validate_horizontal_position(self, horizontal_position: Optional[str]) -> Optional[str]:
        """
        description: Positions the Chatbot button from the left or right side of the page.
        type: string
        """
        if horizontal_position is None:
            return 'contact_chatbot_update_124'

        if horizontal_position not in HORIZONTAL_POSITION_CHOICES:
            return 'contact_chatbot_update_125'

        self.cleaned_data['horizontal_position'] = horizontal_position
        return None

    def validate_intent_prompt(self, intent_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the item with the role "system" added to the prompt sent to the LLM.
        type: string
        """
        # intent classification disabled no need to validate intent prompt
        if 'apply_intent_classification' not in self.cleaned_data:
            return None

        if intent_prompt is None:
            if self.cleaned_data['apply_intent_classification']:
                return 'contact_chatbot_update_126'
            intent_prompt = ''

        intent_prompt = str(intent_prompt).strip()

        if len(intent_prompt) > self.get_field('intent_prompt').max_length:
            return 'contact_chatbot_update_127'

        self.cleaned_data['intent_prompt'] = intent_prompt
        return None

    def validate_layout(self, layout: Optional[str]) -> Optional[str]:
        """
        description: The Layout model for the chatbot
        type: string
        """
        if layout is None:
            return 'contact_chatbot_update_128'

        if layout not in LAYOUT_CHOICES:
            return 'contact_chatbot_update_129'

        self.cleaned_data['layout'] = layout
        return None

    def validate_max_tokens(self, max_tokens: int) -> Optional[str]:
        """
        description: Getting the response up to max_tokens
        type: integer
        """
        if not max_tokens:
            return None

        try:
            max_tokens = int(max_tokens)
        except (TypeError, ValueError):
            return 'contact_chatbot_update_130'
        self.cleaned_data['max_tokens'] = max_tokens
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: Name of the Chatbot
        type: string
        """
        if name is None:
            name = ''

        name = str(name).replace(' ', '')

        if len(name) == 0:
            return 'contact_chatbot_update_131'

        if len(name) > self.get_field('name').max_length:
            return 'contact_chatbot_update_132'

        if (NAME_ALLOWED_CHARS_REGEX.match(name) is None):
            return 'contact_chatbot_update_133'

        if Chatbot.objects.filter(name__iexact=name).exclude(pk=self._instance.pk).exists():
            return 'contact_chatbot_update_134'

        self.cleaned_data['name'] = name
        return None

    def validate_nn_llm(self, nn_llm: Optional[str]) -> Optional[str]:
        """
        description: The Neural Network Large Language model for the chatbot
        type: string
        """
        if nn_llm is None:
            return 'contact_chatbot_update_135'

        if nn_llm not in NN_LLM_CHOICES:
            return 'contact_chatbot_update_136'

        self.cleaned_data['nn_llm'] = nn_llm
        return None

    def validate_pdf_scraping(self, pdf_scraping: str) -> Optional[str]:
        """
        description: The Scraping method for PDF documents
        type: string
        """
        if pdf_scraping is None:
            return None

        if pdf_scraping not in PDF_SCRAPING_CHOICES:
            return 'contact_chatbot_update_138'

        self.cleaned_data['pdf_scraping'] = pdf_scraping
        return None

    def validate_reference_limit(self, reference_limit: int) -> Optional[str]:
        """
        description: Number of references between 1 and 10
        type: integer
        """
        if not reference_limit:
            return 'contact_chatbot_update_139'
        try:
            reference_limit = int(reference_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_update_140'
        if reference_limit < 1 or reference_limit > 50:
            return 'contact_chatbot_update_141'

        self.cleaned_data['reference_limit'] = reference_limit
        return None

    def validate_reranker(self, reranker: Optional[str]) -> Optional[str]:
        """
        description: The Neural Network Large Language model for Re-Ranking
        type: string
        """
        if reranker is None:
            return 'contact_chatbot_update_142'

        if reranker not in RERANKER_CHOICES:
            return 'contact_chatbot_update_143'

        self.cleaned_data['reranker'] = reranker
        return None

    def validate_reranking_limit(self, reranking_limit: int) -> Optional[str]:
        """
        description: Number of references between 1 and 10
        type: integer
        """
        if not reranking_limit:
            return 'contact_chatbot_update_144'
        try:
            reranking_limit = int(reranking_limit)
        except (TypeError, ValueError):
            return 'contact_chatbot_update_145'
        if reranking_limit < 1 or reranking_limit > 50:
            return 'contact_chatbot_update_146'

        self.cleaned_data['reranking_limit'] = reranking_limit
        return None

    def validate_similarity(self, similarity: Optional[str]) -> Optional[str]:
        """
        description: The Vector Similarity formula for the retrieval of Embeddings for the chatbot
        type: string
        """
        if similarity is None:
            return 'contact_chatbot_update_147'

        if similarity not in SIMILARITY_CHOICES:
            return 'contact_chatbot_update_148'

        self.cleaned_data['similarity'] = similarity
        return None

    def validate_smalltalk_prompt(self, smalltalk_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the prompt sent to the smalltalk LLM.
        type: string
        """
        if smalltalk_prompt is None:
            smalltalk_prompt = ''

        smalltalk_prompt = str(smalltalk_prompt).strip()

        if len(smalltalk_prompt) > self.get_field('smalltalk_prompt').max_length:
            return 'contact_chatbot_update_149'

        self.cleaned_data['smalltalk_prompt'] = smalltalk_prompt
        return None

    def validate_system_prompt(self, system_prompt: Optional[str]) -> Optional[str]:
        """
        description: The content of the item with the role "system" added to the prompt sent to the LLM.
        type: string
        """
        if system_prompt is None:
            system_prompt = ''

        system_prompt = str(system_prompt).strip()

        if len(system_prompt) > self.get_field('system_prompt').max_length:
            return 'contact_chatbot_update_150'

        self.cleaned_data['system_prompt'] = system_prompt
        return None

    def validate_no_reference_answer(self, no_reference_answer: Optional[str]) -> Optional[str]:
        """
        description: The fallback answer returned when no references are found.
        type: string
        required: false
        """
        if no_reference_answer is None:
            return None

        no_reference_answer = str(no_reference_answer).strip()

        if len(no_reference_answer) > self.get_field('no_reference_answer').max_length:
            return 'contact_chatbot_update_165'

        self.cleaned_data['no_reference_answer'] = no_reference_answer
        return None

    def validate_temperature(self, temperature: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            Temperature is a parameter that controls the "creativity" or randomness of the text generated. A higher
            temperature (e.g., 0.7) results in more diverse and creative output, while a lower temperature (e.g., 0.2)
            makes the output more deterministic and focused.
        type: string
        format: decimal
        """
        if not temperature:
            return None

        try:
            temperature = Decimal(str(temperature))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_update_151'

        if temperature < 0 or temperature > 1:
            return 'contact_chatbot_update_152'

        self.cleaned_data['temperature'] = temperature
        return None

    def validate_threshold(self, threshold: Optional[Decimal]) -> Optional[str]:
        """
        description: The fixed Euclidean Distance in order to retrieve the chunks
        required: false
        type: string
        format: decimal
        """
        if not threshold:
            return None
        try:
            threshold = Decimal(str(threshold))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_update_153'

        self.cleaned_data['threshold'] = threshold
        return None

    def validate_user_prompt(self, user_prompt: Optional[str]) -> Optional[str]:
        """
        description: The value to be appended to questions sent to the LLM in the constructed prompt.
        type: string
        """
        if user_prompt is None:
            user_prompt = ''

        user_prompt = str(user_prompt).strip()

        if len(user_prompt) > self.get_field('user_prompt').max_length:
            return 'contact_chatbot_update_154'

        self.cleaned_data['user_prompt'] = user_prompt
        return None

    def validate_vertical_percentage(self, vertical_percentage: Optional[Decimal]) -> Optional[str]:
        """
        description: |
            The percentage value from the bottom or top of your website to position the button embedded on your website
            to launch the iframe for the Chatbot. If not sent the default value 2% will be used.
        required: false
        type: string
        """
        if not vertical_percentage:
            return None

        try:
            vertical_percentage = Decimal(str(vertical_percentage))
        except (ValueError, TypeError, InvalidOperation):
            return 'contact_chatbot_update_155'

        if vertical_percentage < 0 or vertical_percentage > 100:
            return 'contact_chatbot_update_156'

        self.cleaned_data['vertical_percentage'] = vertical_percentage
        return None

    def validate_vertical_position(self, vertical_position: Optional[str]) -> Optional[str]:
        """
        description: Positions the Chatbot button from the bottom or top side of the page.
        type: string
        """
        if vertical_position is None:
            return 'contact_chatbot_update_157'

        if vertical_position not in VERTICAL_POSITION_CHOICES:
            return 'contact_chatbot_update_158'

        self.cleaned_data['vertical_position'] = vertical_position
        return None

    def validate_welcome_text(self, welcome_text: Optional[str]) -> Optional[str]:
        """
        description: |
            The text displayed on the page your website visitor sees when logging into your Chatbot.
            If not sent the default value "Please login to Chatbot" will be used.
        required: false
        type: string
        """
        if not welcome_text:
            return None

        if len(welcome_text) > self.get_field('welcome_text').max_length:
            return 'contact_chatbot_update_159'

        self.cleaned_data['welcome_text'] = welcome_text
        return None

    def validate_logo(self, logo: Optional[Union[Dict[str, str], str]]):
        """
        description: The data of the logo to use on the Chatbot iframe.
        type: object
        properties:
            name:
                description: name of the logo file
                type: string
            data:
                description: The logo encoded in base64
                type: string
        required: false
        """
        if logo is None:
            return None

        if not isinstance(logo, dict):
            return 'contact_chatbot_update_160'

        try:
            filename: str = f'{uuid4()}.{logo["name"].split(".")[1]}'
            data: bytes = base64.b64decode(logo['data'])
            filesize: int = len(data)
        except KeyError:
            return 'contact_chatbot_update_161'
        except binascii.Error:
            return 'contact_chatbot_update_162'

        # Check that our variables are valid
        if filesize == 0:
            return 'contact_chatbot_update_163'

        # If any errors have occurred we are not going to upload logo
        if len(self._errors) > 0:
            return None

        if settings.CHATBOT_URL is None:  # pragma: no cover
            return 'contact_chatbot_update_164'

        chatbot_name = self.cleaned_data['name']
        # TODO: Upload image to CHATBOT_LOGO_LOCATION

        logo = f'{settings.CHATBOT_URL.rstrip("/")}/{chatbot_name}/{filename}'

        self.cleaned_data['logo'] = logo
        return None
