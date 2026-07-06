from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.ai_jobs import AIJobRepository
from app.database.repositories.ai_profiles import AIProfileRepository
from app.database.repositories.event_feedback import EventFeedbackRepository
from app.database.repositories.event_participants import (
    EventParticipantRepository,
)
from app.database.repositories.events import EventRepository
from app.database.repositories.hobbies import HobbyRepository
from app.database.repositories.imports import ImportRepository
from app.database.repositories.interests import InterestRepository
from app.database.repositories.knowledge_articles import (
    KnowledgeArticleRepository,
)
from app.database.repositories.knowledge_sources import (
    KnowledgeSourceRepository,
)
from app.database.repositories.knowledge_tags import (
    KnowledgeTagRepository,
)
from app.database.repositories.message_attachments import (
    MessageAttachmentRepository,
)
from app.database.repositories.messages import MessageRepository
from app.database.repositories.notifications import (
    NotificationRepository,
)
from app.database.repositories.organizations import (
    OrganizationRepository,
)
from app.database.repositories.profiles import ProfileRepository
from app.database.repositories.saved_messages import (
    SavedMessageRepository,
)
from app.database.repositories.settings import SettingRepository
from app.database.repositories.skills import SkillRepository
from app.database.repositories.tags import TagRepository
from app.database.repositories.tag_relations import (
    TagRelationRepository,
)
from app.database.repositories.timeline import TimelineRepository
from app.database.repositories.users import UserRepository
from app.database.repositories.statistics import StatisticsRepository

class UnitOfWork:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.users = UserRepository(session)
        self.messages = MessageRepository(session)
        self.attachments = MessageAttachmentRepository(session)

        self.profiles = ProfileRepository(session)

        self.events = EventRepository(session)
        self.event_participants = EventParticipantRepository(session)
        self.event_feedback = EventFeedbackRepository(session)

        self.organizations = OrganizationRepository(session)

        self.timeline = TimelineRepository(session)

        self.notifications = NotificationRepository(session)

        self.saved_messages = SavedMessageRepository(session)

        self.knowledge_articles = KnowledgeArticleRepository(session)
        self.knowledge_sources = KnowledgeSourceRepository(session)
        self.knowledge_tags = KnowledgeTagRepository(session)

        self.ai_jobs = AIJobRepository(session)
        self.ai_profiles = AIProfileRepository(session)

        self.skills = SkillRepository(session)
        self.interests = InterestRepository(session)
        self.hobbies = HobbyRepository(session)

        self.tags = TagRepository(session)
        self.tag_relations = TagRelationRepository(session)

        self.settings = SettingRepository(session)

        self.statistics = StatisticsRepository(session)
        
        self.imports = ImportRepository(session)