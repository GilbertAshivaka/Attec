# Import all models here for Alembic to detect them
from app.db.session import Base
from app.models.user import User
from app.models.contact import ContactSubmission
from app.models.analytics import AnalyticsEvent
