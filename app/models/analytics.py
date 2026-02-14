"""
Analytics Event model for tracking user interactions
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.config.database import Base


class EventType(str, enum.Enum):
    """Event type enumeration"""
    PROPERTY_VIEW = "property_view"
    SEARCH_PERFORMED = "search_performed"
    INQUIRY_SUBMITTED = "inquiry_submitted"


class AnalyticsEvent(Base):
    """Analytics Event model for tracking"""
    __tablename__ = "analytics_events"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    event_type: Mapped[EventType] = mapped_column(
        SQLEnum(EventType, name="event_type", create_constraint=True),
        nullable=False,
        index=True
    )
    property_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    event_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    
    def __repr__(self) -> str:
        return f"<AnalyticsEvent(id={self.id}, event_type={self.event_type})>"
