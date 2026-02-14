"""
Property schemas for API requests and responses
"""
from typing import Optional, List, Literal
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, UUID4
from app.models.property import PropertyType, ListingType, FacingDirection, FurnishingStatus


class PropertyBase(BaseModel):
    """Base property schema"""
    title: str = Field(..., min_length=5, max_length=500)
    description: Optional[str] = None
    locality: str = Field(..., min_length=2, max_length=255)
    sector: str = Field(..., min_length=1, max_length=100)
    latitude: Decimal = Field(..., ge=-90, le=90)
    longitude: Decimal = Field(..., ge=-180, le=180)
    property_type: PropertyType
    listing_type: ListingType
    bhk: Optional[int] = Field(None, ge=1, le=10)
    area_sqft: Decimal = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)
    facing_direction: Optional[FacingDirection] = None
    furnishing_status: Optional[FurnishingStatus] = None
    floor_number: Optional[int] = Field(None, ge=0)
    total_floors: Optional[int] = Field(None, ge=1)
    age_years: Optional[int] = Field(None, ge=0, le=100)
    vastu_score: int = Field(default=50, ge=0, le=100)
    natural_light_score: int = Field(default=50, ge=0, le=100)


class PropertyCreate(PropertyBase):
    """Schema for creating a property"""
    pass


class PropertyUpdate(BaseModel):
    """Schema for updating a property"""
    title: Optional[str] = Field(None, min_length=5, max_length=500)
    description: Optional[str] = None
    locality: Optional[str] = Field(None, min_length=2, max_length=255)
    sector: Optional[str] = Field(None, min_length=1, max_length=100)
    latitude: Optional[Decimal] = Field(None, ge=-90, le=90)
    longitude: Optional[Decimal] = Field(None, ge=-180, le=180)
    property_type: Optional[PropertyType] = None
    listing_type: Optional[ListingType] = None
    bhk: Optional[int] = Field(None, ge=1, le=10)
    area_sqft: Optional[Decimal] = Field(None, gt=0)
    price: Optional[Decimal] = Field(None, gt=0)
    facing_direction: Optional[FacingDirection] = None
    furnishing_status: Optional[FurnishingStatus] = None
    floor_number: Optional[int] = Field(None, ge=0)
    total_floors: Optional[int] = Field(None, ge=1)
    age_years: Optional[int] = Field(None, ge=0, le=100)
    vastu_score: Optional[int] = Field(None, ge=0, le=100)
    natural_light_score: Optional[int] = Field(None, ge=0, le=100)


class ImageResponse(BaseModel):
    """Image response schema"""
    id: UUID4
    original_url: str
    enhanced_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_type: str
    is_primary: bool
    display_order: int
    enhancement_status: str
    
    model_config = {"from_attributes": True}


class KeyMetrics(BaseModel):
    """Key metrics for property"""
    vastu_score: int
    natural_light_score: int
    price_vs_market: Literal["below_average", "average", "above_average"]


class FacingWidgetData(BaseModel):
    """Facing direction widget data"""
    direction: str
    heat_exposure: int = Field(..., ge=0, le=100, description="Heat exposure score 0-100")
    vastu_compatibility: int = Field(..., ge=0, le=100, description="Vastu compatibility score 0-100")
    natural_light_intensity: int = Field(..., ge=0, le=100, description="Natural light intensity 0-100")


class PriceComparisonData(BaseModel):
    """Price comparison data"""
    property_price_per_sqft: Decimal
    similar_properties_avg_price: Decimal
    difference_percentage: Decimal
    category: Literal["below_average", "average", "above_average"]


class PropertySearchResult(BaseModel):
    """Property search result schema"""
    id: UUID4
    title: str
    price: Decimal
    area_sqft: Decimal
    price_per_sqft: Optional[Decimal]
    locality: str
    sector: str
    bhk: Optional[int]
    property_type: str
    listing_type: str
    primary_image: Optional[ImageResponse] = None
    key_metrics: KeyMetrics
    
    model_config = {"from_attributes": True}


class PropertyDetail(BaseModel):
    """Property detail schema"""
    id: UUID4
    title: str
    description: Optional[str]
    locality: str
    sector: str
    latitude: Decimal
    longitude: Decimal
    property_type: str
    listing_type: str
    bhk: Optional[int]
    area_sqft: Decimal
    price: Decimal
    price_per_sqft: Optional[Decimal]
    facing_direction: Optional[str]
    furnishing_status: Optional[str]
    floor_number: Optional[int]
    total_floors: Optional[int]
    age_years: Optional[int]
    vastu_score: int
    natural_light_score: int
    is_active: bool
    view_count: int
    inquiry_count: int
    created_at: datetime
    updated_at: datetime
    images: List[ImageResponse] = []
    facing_widget_data: Optional[FacingWidgetData] = None
    price_comparison: Optional[PriceComparisonData] = None
    
    model_config = {"from_attributes": True}


class PropertyListResponse(BaseModel):
    """Property list response with pagination"""
    items: List[PropertySearchResult]
    page: int
    per_page: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool
