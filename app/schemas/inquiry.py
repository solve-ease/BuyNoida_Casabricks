"""
Inquiry schemas for lead management
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, UUID4
from app.models.inquiry import InquiryType, InquiryStatus, InquirySource


class InquiryCreate(BaseModel):
    """Schema for creating an inquiry"""
    property_id: UUID4 = Field(..., description="Property ID")
    full_name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., pattern=r'^\+91[6-9]\d{9}$', description="Indian phone format: +91XXXXXXXXXX")
    message: Optional[str] = Field(None, max_length=2000)
    inquiry_type: InquiryType = Field(default=InquiryType.GENERAL)
    preferred_contact_time: Optional[str] = Field(None, max_length=255)


class InquiryResponse(BaseModel):
    """Inquiry response schema"""
    id: UUID4
    property_id: Optional[UUID4]
    full_name: str
    email: str
    phone: str
    message: Optional[str]
    inquiry_type: str
    preferred_contact_time: Optional[str]
    status: str
    source: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


class InquiryDetail(InquiryResponse):
    """Detailed inquiry response (for admin)"""
    assigned_to: Optional[UUID4]
    notes: Optional[str]
    user_agent: Optional[str]
    ip_address: Optional[str]
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class InquiryStatusUpdate(BaseModel):
    """Schema for updating inquiry status"""
    status: InquiryStatus


class InquiryNotesUpdate(BaseModel):
    """Schema for adding notes to inquiry"""
    notes: str = Field(..., min_length=1, max_length=5000)
