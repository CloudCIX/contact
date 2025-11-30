from .campaign import CampaignListController, CampaignCreateController, CampaignUpdateController
from .campaign_contact import (
    CampaignContactCreateController,
    CampaignContactUpdateController,
    CampaignContactDeleteController,
)
from .chatbot import ChatbotListController, ChatbotCreateController, ChatbotUpdateController
from .contact import ContactListController, ContactCreateController, ContactUpdateController
from .conversation import ConversationListController, ConversationCreateController
from .corpus import CorpusListController
from .exclusion import ExclusionListController, ExclusionCreateController, ExclusionUpdateController
from .group import GroupListController, GroupCreateController, GroupUpdateController
from .group_contact import GroupContactCreateController, GroupContactDeleteController
from .opportunity import OpportunityListController, OpportunityCreateController, OpportunityUpdateController
from .opportunity_contact import OpportunityContactCreateController, OpportunityContactDeleteController
from .opportunity_history import OpportunityHistoryListController, OpportunityHistoryCreateController
from .q_and_a import QAndAListController, QAndACreateController
from .question import QuestionListController, QuestionCreateController, QuestionUpdateController
from .question_set import QuestionSetListController, QuestionSetCreateController, QuestionSetUpdateController


__all__ = [
    # Campaign
    'CampaignListController',
    'CampaignCreateController',
    'CampaignUpdateController',

    # CampaignContact
    'CampaignContactCreateController',
    'CampaignContactUpdateController',
    'CampaignContactDeleteController',

    # Chatbot
    'ChatbotListController',
    'ChatbotCreateController',
    'ChatbotUpdateController',

    # Contact
    'ContactListController',
    'ContactCreateController',
    'ContactUpdateController',

    # Conversation
    'ConversationListController',
    'ConversationCreateController',

    # Corpus
    'CorpusListController',
    'CorpusCreateController',
    'CorpusUpdateController',

    # Exclusion
    'ExclusionListController',
    'ExclusionCreateController',
    'ExclusionUpdateController',

    # Group
    'GroupListController',
    'GroupCreateController',
    'GroupUpdateController',

    # Group Contact
    'GroupContactCreateController',
    'GroupContactDeleteController',

    # Opportunity
    'OpportunityListController',
    'OpportunityCreateController',
    'OpportunityUpdateController',

    # Opportunity Contact
    'OpportunityContactCreateController',
    'OpportunityContactDeleteController',

    # Opportunity History
    'OpportunityHistoryListController',
    'OpportunityHistoryCreateController',

    # QAndA
    'QAndAListController',
    'QAndACreateController',

    # Question
    'QuestionListController',
    'QuestionCreateController',
    'QuestionUpdateController',

    # Question Set
    'QuestionSetListController',
    'QuestionSetCreateController',
    'QuestionSetUpdateController',
]
