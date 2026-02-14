"""
Webhook endpoints for external service callbacks
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.image import WebhookAIEnhancementRequest
from app.schemas.common import SuccessResponse
from app.services.image_service import ImageService
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/ai-enhancement", response_model=SuccessResponse)
async def ai_enhancement_webhook(
    webhook_data: WebhookAIEnhancementRequest,
    x_webhook_signature: str = Header(..., description="HMAC signature for verification"),
    db: AsyncSession = Depends(get_db)
):
    """
    Webhook endpoint for AI image enhancement service
    
    Called by external AI service when image enhancement is complete.
    
    Request body:
    - **job_id**: Job ID (our image UUID)
    - **status**: success or failed
    - **enhanced_image_url**: URL of enhanced image (if success)
    - **processing_time_seconds**: Time taken to process
    - **error_message**: Error message (if failed)
    
    Headers:
    - **X-Webhook-Signature**: HMAC SHA256 signature for verification
    
    Security:
    - Verifies HMAC signature
    - Implements idempotent handling
    - Returns 200 OK quickly
    
    Processing:
    - If success: Downloads enhanced image, uploads to our storage, updates DB
    - If failed: Updates DB with error message
    """
    image_service = ImageService(db)
    
    try:
        # Process webhook (includes signature verification)
        success = await image_service.process_webhook(
            webhook_data=webhook_data,
            signature=x_webhook_signature
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to process webhook"
            )
        
        logger.info(
            "webhook_processed",
            job_id=webhook_data.job_id,
            status=webhook_data.status
        )
        
        return SuccessResponse(message="Webhook processed successfully")
        
    except Exception as e:
        logger.error("webhook_processing_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
