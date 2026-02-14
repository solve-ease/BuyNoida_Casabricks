"""
Image schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from app.models.image import ImageType, EnhancementStatus


class ImageUploadResponse(BaseModel):
    """Image upload response"""
    id: UUID4
    property_id: UUID4
    original_url: str
    image_type: str
    enhancement_status: str
    
    model_config = {"from_attributes": True}


class ImageEnhanceRequest(BaseModel):
    """Request to enhance an image"""
    pass  # No body needed, just the image ID in the URL


class ImageEnhanceResponse(BaseModel):
    """Response after triggering enhancement"""
    id: UUID4
    ai_job_id: str
    status: str
    message: str


class WebhookAIEnhancementRequest(BaseModel):
    """Webhook request from AI service"""
    job_id: str = Field(..., description="Job ID from our database")
    status: str = Field(..., description="success or failed")
    enhanced_image_url: Optional[str] = Field(None, description="URL of enhanced image if success")
    processing_time_seconds: Optional[int] = Field(None, description="Processing time")
    error_message: Optional[str] = Field(None, description="Error message if failed")
