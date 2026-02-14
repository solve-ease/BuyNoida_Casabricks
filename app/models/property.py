"""
Property model
"""
import uuid
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import String, Integer, Boolean, DateTime, Numeric, ForeignKey, Enum as SQLEnum, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.config.database import Base


class PropertyType(str, enum.Enum):
    """Property type enumeration"""
    FLAT = "flat"
    VILLA = "villa"
    PLOT = "plot"
    COMMERCIAL = "commercial"


class ListingType(str, enum.Enum):
    """Listing type enumeration"""
    SALE = "sale"
    RENT = "rent"


class FacingDirection(str, enum.Enum):
    """Facing direction enumeration"""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    NORTH_EAST = "north_east"
    NORTH_WEST = "north_west"
    SOUTH_EAST = "south_east"
    SOUTH_WEST = "south_west"


class FurnishingStatus(str, enum.Enum):
    """Furnishing status enumeration"""
    FURNISHED = "furnished"
    SEMI_FURNISHED = "semi_furnished"
    UNFURNISHED = "unfurnished"


class Property(Base):
    """Property model"""
    __tablename__ = "properties"
    __table_args__ = (
        CheckConstraint('vastu_score >= 0 AND vastu_score <= 100', name='check_vastu_score'),
        CheckConstraint('natural_light_score >= 0 AND natural_light_score <= 100', name='check_natural_light_score'),
    )
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    locality: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False, index=True)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 7), nullable=False, index=True)
    property_type: Mapped[PropertyType] = mapped_column(
        SQLEnum(PropertyType, name="property_type", create_constraint=True),
        nullable=False,
        index=True
    )
    listing_type: Mapped[ListingType] = mapped_column(
        SQLEnum(ListingType, name="listing_type", create_constraint=True),
        nullable=False
    )
    bhk: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True)
    area_sqft: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, index=True)
    price_per_sqft: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        # This will be calculated as a generated column in the migration
    )
    facing_direction: Mapped[Optional[FacingDirection]] = mapped_column(
        SQLEnum(FacingDirection, name="facing_direction", create_constraint=True),
        nullable=True
    )
    furnishing_status: Mapped[Optional[FurnishingStatus]] = mapped_column(
        SQLEnum(FurnishingStatus, name="furnishing_status", create_constraint=True),
        nullable=True
    )
    floor_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_floors: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    age_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vastu_score: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    natural_light_score: Mapped[int] = mapped_column(Integer, nullable=False, default=50)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    inquiry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    images: Mapped[List["PropertyImage"]] = relationship(
        "PropertyImage",
        back_populates="property",
        cascade="all, delete-orphan"
    )
    inquiries: Mapped[List["Inquiry"]] = relationship(
        "Inquiry",
        back_populates="property"
    )
    
    def __repr__(self) -> str:
        return f"<Property(id={self.id}, title={self.title}, type={self.property_type})>"
