from .answer import AnswerCollection
from .auth import AuthResource
from .campaign import CampaignCollection, CampaignResource
from .campaign_contact import CampaignContactCollection
from .chatbot import ChatbotCollection, ChatbotResource
from .contact import ContactCollection, ContactResource
from .conversation import ConversationCollection, ConversationResource
from .corpus import CorpusCollection
from .embeddings import EmbeddingsResource
from .exclusion import ExclusionCollection, ExclusionResource
from .group import GroupCollection, GroupResource
from .group_contact import GroupContactCollection
from .opportunity import OpportunityCollection, OpportunityResource
from .opportunity_contact import OpportunityContactCollection
from .opportunity_history import OpportunityHistoryCollection
from .q_and_a import QAndACollection, QAndAResource
from .question import QuestionCollection, QuestionResource
from .question_set import QuestionSetCollection, QuestionSetResource
from .summary import SummaryCollection


__all__ = [

    # Answer
    'AnswerCollection',

    # Auth
    'AuthResource',

    # Campaign
    'CampaignCollection',
    'CampaignResource',

    # Campaign Contact
    'CampaignContactCollection',

    # Chatbot
    'ChatbotCollection',
    'ChatbotResource',

    # Contact
    'ContactCollection',
    'ContactResource',

    # Corpus
    'CorpusCollection',
    'CorpusResource',

    # Conversation
    'ConversationCollection',
    'ConversationResource',

    # Embeddings
    'EmbeddingsCollection',
    'EmbeddingsResource',

    # Exclusion
    'ExclusionCollection',
    'ExclusionResource',

    # Group
    'GroupCollection',
    'GroupResource',

    # Group Contact
    'GroupContactCollection',

    # Opportunity
    'OpportunityCollection',
    'OpportunityResource',

    # Opportunity Contact
    'OpportunityContactCollection',

    # Opportunity History
    'OpportunityHistoryCollection',

    # QAndA
    'QAndACollection',
    'QAndAResource',

    # Question
    'QuestionCollection',
    'QuestionResource',

    # Question Set
    'QuestionSetCollection',
    'QuestionSetResource',

    # Summary
    'SummaryCollection',
]
