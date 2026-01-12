# stdlib

# libs
from datetime import datetime

from cloudcix_rest.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

# local

__all__ = [
    # Chatbot
    'Chatbot',
]


class Chatbot(BaseModel):
    """
    The Chatbot model contains the fields for the chatbot
    """
    HEX_CODE_REGEX = '^#(?:[0-9a-fA-F]{3}){1,2}$'

    # Encoder Choice Options
    CIX_ENCODER = 'cix_encoder'
    DRAGON_PLUS = 'dragon_plus'
    TEST_ENCODER = 'test_encoder'
    USE4 = 'use4'
    ENCODER_CHOICES = (
        (CIX_ENCODER, CIX_ENCODER),
        (DRAGON_PLUS, DRAGON_PLUS),
        (USE4, USE4),
        (TEST_ENCODER, TEST_ENCODER),
    )

    # Button Position Options
    LEFT = 'left'
    RIGHT = 'right'
    HORIZONTAL_POSITION_CHOICES = (
        (LEFT, LEFT),
        (RIGHT, RIGHT),
    )

    TOP = 'top'
    BOTTOM = 'bottom'
    VERTICAL_POSITION_CHOICES = (
        (TOP, TOP),
        (BOTTOM, BOTTOM),
    )

    # Layout Choice Options
    WINDOW = 'window'
    WIDGET = 'widget'
    LAYOUT_CHOICES = (
        (WINDOW, WINDOW),
        (WIDGET, WIDGET),
    )

    # NN Choice Options
    CHATGPT4 = 'chatgpt4'
    CHATGPT4_1 = 'chatgpt4.1'
    UCCIX_INSTRUCT = 'uccix_instruct'
    UCCIX_INSTRUCT_70B = 'uccix_instruct_70b'
    MISTRAL = 'UCCIX-Mistral-24B'

    NN_LLM_CHOICES = (
        (CHATGPT4_1, CHATGPT4_1),
        (CHATGPT4, CHATGPT4),
        (MISTRAL, MISTRAL),
        (UCCIX_INSTRUCT, UCCIX_INSTRUCT),
        (UCCIX_INSTRUCT_70B, UCCIX_INSTRUCT_70B),
    )

    # PDF Scraping Choices
    BASIC_SCRAPING = 'pdf'
    HI_RES_SCRAPING = 'pdf_hi_res'

    PDF_SCRAPING_CHOICES = (
        (BASIC_SCRAPING, BASIC_SCRAPING),
        (HI_RES_SCRAPING, HI_RES_SCRAPING),
    )

    # Vector Similarity Choices
    COSINE_SIMILARITY = 'cosine_similarity'
    DOT_PRODUCT = 'dot_product'
    EUCLIDEAN_DISTANCE = 'euclidean_distance'

    SIMILARITY_CHOICES = (
        (COSINE_SIMILARITY, COSINE_SIMILARITY),
        (DOT_PRODUCT, DOT_PRODUCT),
        (EUCLIDEAN_DISTANCE, EUCLIDEAN_DISTANCE),
    )

    MINILM_L_6_v2 = 'minilm-l-6-v2'

    RERANKER_CHOICES = NN_LLM_CHOICES + (
        (MINILM_L_6_v2, MINILM_L_6_v2),
    )

    # Fields
    api_key = models.CharField(max_length=64, null=True)
    bm25_limit = models.IntegerField(default=0)
    button_background_colour = models.CharField(max_length=7, default='#47B2E4')
    button_text = models.CharField(max_length=50, default='Chatbot')
    button_text_colour = models.CharField(max_length=7, default='#FFFFFF')
    chatbot_header_title = models.CharField(default='', max_length=255)
    chatbot_header_description = models.CharField(default='', max_length=255)
    chunk_size = models.IntegerField(default=1000)
    chunk_overlap = models.IntegerField(default=100)
    cookie_consent_text = models.CharField(
        default='This Chatbot uses only essential cookies. You must accept the essential cookies to use this Chatbot.',
        max_length=255,
    )
    corpus_names = models.JSONField(default=list)
    echo = models.BooleanField(default=False)
    encoder = models.CharField(choices=ENCODER_CHOICES, max_length=12, default=USE4)
    horizontal_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=3)
    horizontal_position = models.CharField(choices=HORIZONTAL_POSITION_CHOICES, max_length=6, default=RIGHT)
    layout = models.CharField(choices=LAYOUT_CHOICES, max_length=6, default=WINDOW)
    logo = models.URLField(null=True)
    member_id = models.IntegerField()
    name = models.CharField(max_length=50)
    nn_llm = models.CharField(choices=NN_LLM_CHOICES, max_length=20, default=MISTRAL)
    nn_embedding = models.CharField(max_length=50, blank=True)
    similarity = models.CharField(choices=SIMILARITY_CHOICES, max_length=20, default=EUCLIDEAN_DISTANCE)
    system_prompt = models.CharField(max_length=10000, null=True)
    smalltalk_prompt = models.CharField(max_length=10000, null=True)
    apply_safety_classifier = models.BooleanField(default=False)
    intent_prompt = models.CharField(max_length=10000, null=True)
    threshold = models.DecimalField(max_digits=5, decimal_places=2, default=25)
    user_prompt = models.CharField(max_length=10000, null=True)
    welcome_text = models.CharField(max_length=255, default='Please login to Chatbot')
    max_tokens = models.IntegerField(default=100)
    pdf_scraping = models.CharField(choices=PDF_SCRAPING_CHOICES, max_length=16, default=BASIC_SCRAPING)
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    reference_limit = models.IntegerField(default=1)
    vertical_position = models.CharField(choices=VERTICAL_POSITION_CHOICES, max_length=6, default=BOTTOM)
    vertical_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=2)
    contact_information = models.CharField(max_length=100, null=True)
    apply_reranking = models.BooleanField(default=False)
    reranking_limit = models.IntegerField(default=5)
    reranker = models.CharField(choices=RERANKER_CHOICES, max_length=128, default=MINILM_L_6_v2)
    apply_intent_classification = models.BooleanField(default=False)
    # Fallback answer if no similar references are retrieved. If not empty and retrieval returns zero chunks,
    # this text will be streamed back instead of calling the LLM.
    no_reference_answer = models.CharField(max_length=1000, default='')

    class Meta:
        """
        Metadata about the model for Django to use in whatever way it sees fit
        """
        # Django default table names are f'{app_label}_{table}' but we only
        # need the table name since we have multiple DBs
        db_table = 'chatbot'

        indexes = [
            models.Index(fields=['created'], name='chatbot_created'),
            models.Index(fields=['id'], name='chatbot_id'),
            models.Index(fields=['member_id'], name='chatbot_member_id'),
            models.Index(fields=['name'], name='chatbot_name'),
        ]

        ordering = ['name']

    def get_absolute_url(self):
        """
        Generates the absolute URL that corresponds to the ChatbotResource view for this Chatbot record
        :return: A URL that corresponds to the views for this Chatbot record
        """
        return reverse('chatbot_resource', kwargs={'pk': self.pk})

    def cascade_delete(self):
        """
        Delete the Chatbot instance, and the conversations and corpus associated it
        """
        deltime = datetime.utcnow()
        self.corpora.all().update(deleted=deltime)
        for conversation in self.conversations.all().iterator():
            conversation.cascade_delete()
        self.deleted = deltime
        self.save()
