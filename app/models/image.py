"""
Property Image model
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.config.database import Base


class ImageType(str, enum.Enum):
    """Image type enumeration"""
    FRONT_EXTERIOR = "front_exterior"
    INTERIOR = "interior"
    FLOOR_PLAN = "floor_plan"
    OTHER = "other"


class EnhancementStatus(str, enum.Enum):
    """Image enhancement status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class PropertyImage(Base):
    """Property Image model"""
    __tablename__ = "property_images"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    enhanced_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_type: Mapped[ImageType] = mapped_column(
        SQLEnum(ImageType, name="image_type", create_constraint=True),
        nullable=False,
        default=ImageType.OTHER
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    enhancement_status: Mapped[EnhancementStatus] = mapped_column(
        SQLEnum(EnhancementStatus, name="enhancement_status", create_constraint=True),
        nullable=False,
        default=EnhancementStatus.PENDING,
        index=True
    )
    ai_job_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    enhancement_requested_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    enhancement_completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    enhancement_error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    property: Mapped["Property"] = relationship("Property", back_populates="images")
    
    def __repr__(self) -> str:
        return f"<PropertyImage(id={self.id}, property_id={self.property_id}, status={self.enhancement_status})>"
