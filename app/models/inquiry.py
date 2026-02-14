"""
Inquiry model for lead management
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.config.database import Base


class InquiryType(str, enum.Enum):
    """Inquiry type enumeration"""
    GENERAL = "general"
    CALLBACK = "callback"
    SITE_VISIT = "site_visit"


class InquiryStatus(str, enum.Enum):
    """Inquiry status enumeration"""
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"


class InquirySource(str, enum.Enum):
    """Inquiry source enumeration"""
    WEB = "web"
    MOBILE_APP = "mobile_app"


class Inquiry(Base):
    """Inquiry model for lead management"""
    __tablename__ = "inquiries"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    property_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    inquiry_type: Mapped[InquiryType] = mapped_column(
        SQLEnum(InquiryType, name="inquiry_type", create_constraint=True),
        nullable=False,
        default=InquiryType.GENERAL
    )
    preferred_contact_time: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[InquiryStatus] = mapped_column(
        SQLEnum(InquiryStatus, name="inquiry_status", create_constraint=True),
        nullable=False,
        default=InquiryStatus.NEW,
        index=True
    )
    assigned_to: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[InquirySource] = mapped_column(
        SQLEnum(InquirySource, name="inquiry_source", create_constraint=True),
        nullable=False,
        default=InquirySource.WEB
    )
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    property: Mapped[Optional["Property"]] = relationship("Property", back_populates="inquiries")
    
    def __repr__(self) -> str:
        return f"<Inquiry(id={self.id}, full_name={self.full_name}, status={self.status})>"
