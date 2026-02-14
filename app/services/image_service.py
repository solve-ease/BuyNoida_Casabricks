"""
Image service for image upload and enhancement
"""
from typing import Optional
from uuid import UUID
from datetime import datetime
import hashlib
import hmac
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import PropertyImage, EnhancementStatus, ImageType
from app.repositories.image_repo import ImageRepository
from app.repositories.property_repo import PropertyRepository
from app.infrastructure.storage.supabase_storage import SupabaseStorage, get_storage
from app.infrastructure.ai.ai_client import AIServiceClient, get_ai_client
from app.schemas.image import WebhookAIEnhancementRequest
from app.core.exceptions import (
    ImageNotFoundException,
    PropertyNotFoundException,
    ValidationException,
    ImageEnhancementException
)
from app.core.logging import get_logger
from app.core.metrics import image_enhancement_status_total, image_enhancement_duration_seconds
from app.config.settings import settings

logger = get_logger(__name__)


# Allowed image extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024  # Convert to bytes


class ImageService:
    """Service for image operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.image_repo = ImageRepository(db)
        self.property_repo = PropertyRepository(db)
        self.storage = get_storage()
        self.ai_client = get_ai_client()
    
    def validate_image(self, filename: str, file_size: int) -> None:
        """Validate image file"""
        # Check extension
        ext = filename.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationException(
                f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check size
        if file_size > MAX_FILE_SIZE:
            raise ValidationException(
                f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
            )
    
    async def upload_image(
        self,
        property_id: UUID,
        file_content: bytes,
        filename: str,
        content_type: str,
        image_type: ImageType = ImageType.OTHER,
        is_primary: bool = False
    ) -> PropertyImage:
        """Upload image to storage and create database record"""
        # Verify property exists
        property_obj = await self.property_repo.get_by_id(property_id)
        if not property_obj:
            raise PropertyNotFoundException(str(property_id))
        
        # Validate file
        self.validate_image(filename, len(file_content))
        
        # Upload to storage
        original_url = await self.storage.upload_file(
            file_content=file_content,
            file_name=filename,
            content_type=content_type
        )
        
        # Create database record
        image = await self.image_repo.create(
            property_id=property_id,
            original_url=original_url,
            image_type=image_type,
            is_primary=is_primary,
            enhancement_status=EnhancementStatus.PENDING
        )
        
        await self.db.commit()
        
        logger.info(
            "image_uploaded",
            image_id=str(image.id),
            property_id=str(property_id),
            filename=filename
        )
        
        return image
    
    async def delete_image(self, image_id: UUID) -> bool:
        """Delete image"""
        image = await self.image_repo.get_by_id(image_id)
        
        if not image:
            raise ImageNotFoundException(str(image_id))
        
        # Delete from storage
        await self.storage.delete_file(image.original_url)
        if image.enhanced_url:
            await self.storage.delete_file(image.enhanced_url)
        
        # Delete from database
        await self.image_repo.delete(image_id)
        await self.db.commit()
        
        logger.info("image_deleted", image_id=str(image_id))
        
        return True
    
    async def request_enhancement(self, image_id: UUID, webhook_base_url: str) -> dict:
        """Request AI enhancement for image"""
        image = await self.image_repo.get_by_id(image_id)
        
        if not image:
            raise ImageNotFoundException(str(image_id))
        
        # Check if image can be enhanced
        if image.enhancement_status not in [EnhancementStatus.PENDING, EnhancementStatus.FAILED]:
            raise ValidationException(
                f"Image cannot be enhanced. Current status: {image.enhancement_status.value}"
            )
        
        # Build webhook URL
        webhook_url = f"{webhook_base_url}/api/v1/webhooks/ai-enhancement"
        
        # Request enhancement from AI service
        try:
            result = await self.ai_client.request_enhancement(
                image_url=image.original_url,
                job_id=str(image.id),
                webhook_url=webhook_url
            )
            
            # Update image record
            await self.image_repo.update(
                image_id,
                enhancement_status=EnhancementStatus.PROCESSING,
                ai_job_id=result.get("ai_job_id", str(image.id)),
                enhancement_requested_at=datetime.utcnow()
            )
            await self.db.commit()
            
            # Track metric
            image_enhancement_status_total.labels(status="processing").inc()
            
            logger.info(
                "enhancement_requested",
                image_id=str(image_id),
                ai_job_id=result.get("ai_job_id")
            )
            
            return {
                "id": image.id,
                "ai_job_id": result.get("ai_job_id"),
                "status": "processing",
                "message": "Enhancement request submitted successfully"
            }
            
        except Exception as e:
            logger.error("enhancement_request_failed", image_id=str(image_id), error=str(e))
            raise ImageEnhancementException(str(e))
    
    async def process_webhook(
        self,
        webhook_data: WebhookAIEnhancementRequest,
        signature: str
    ) -> bool:
        """Process webhook from AI service"""
        # Verify signature
        if not self._verify_signature(webhook_data.model_dump_json(), signature):
            logger.warning("webhook_signature_invalid")
            raise ValidationException("Invalid webhook signature")
        
        # Get image by job_id (which is our image ID)
        try:
            image_id = UUID(webhook_data.job_id)
        except ValueError:
            logger.error("webhook_invalid_job_id", job_id=webhook_data.job_id)
            return False
        
        image = await self.image_repo.get_by_id(image_id)
        
        if not image:
            logger.error("webhook_image_not_found", job_id=webhook_data.job_id)
            return False
        
        # Check for duplicate webhook (idempotency)
        if image.enhancement_status in [EnhancementStatus.COMPLETED, EnhancementStatus.FAILED]:
            logger.info("webhook_duplicate_ignored", image_id=str(image_id))
            return True
        
        # Process based on status
        if webhook_data.status == "success" and webhook_data.enhanced_image_url:
            await self._process_success(image, webhook_data)
        elif webhook_data.status == "failed":
            await self._process_failure(image, webhook_data)
        
        await self.db.commit()
        
        return True
    
    async def _process_success(
        self,
        image: PropertyImage,
        webhook_data: WebhookAIEnhancementRequest
    ) -> None:
        """Process successful enhancement"""
        try:
            # Download enhanced image
            enhanced_content = await self.storage.download_file(
                webhook_data.enhanced_image_url
            )
            
            # Upload to our storage
            enhanced_url = await self.storage.upload_file(
                file_content=enhanced_content,
                file_name=f"enhanced_{image.id}.jpg",
                content_type="image/jpeg"
            )
            
            # Update image record
            await self.image_repo.update_enhancement_status(
                image.id,
                status=EnhancementStatus.COMPLETED,
                enhanced_url=enhanced_url
            )
            
            # Track metrics
            image_enhancement_status_total.labels(status="completed").inc()
            if webhook_data.processing_time_seconds:
                image_enhancement_duration_seconds.observe(
                    webhook_data.processing_time_seconds
                )
            
            logger.info(
                "enhancement_completed",
                image_id=str(image.id),
                processing_time=webhook_data.processing_time_seconds
            )
            
        except Exception as e:
            logger.error("enhancement_processing_failed", image_id=str(image.id), error=str(e))
            await self.image_repo.update_enhancement_status(
                image.id,
                status=EnhancementStatus.FAILED,
                error_message=f"Failed to process enhanced image: {str(e)}"
            )
            image_enhancement_status_total.labels(status="failed").inc()
    
    async def _process_failure(
        self,
        image: PropertyImage,
        webhook_data: WebhookAIEnhancementRequest
    ) -> None:
        """Process failed enhancement"""
        await self.image_repo.update_enhancement_status(
            image.id,
            status=EnhancementStatus.FAILED,
            error_message=webhook_data.error_message or "Enhancement failed"
        )
        
        image_enhancement_status_total.labels(status="failed").inc()
        
        logger.warning(
            "enhancement_failed",
            image_id=str(image.id),
            error=webhook_data.error_message
        )
    
    def _verify_signature(self, payload: str, signature: str) -> bool:
        """Verify HMAC SHA256 signature"""
        try:
            expected_signature = hmac.new(
                settings.AI_SERVICE_WEBHOOK_SECRET.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error("signature_verification_failed", error=str(e))
            return False
