"""
AI service client for image enhancement
"""
import httpx
from typing import Dict, Any
from app.config.settings import settings
from app.core.logging import get_logger
from app.core.exceptions import ImageEnhancementException

logger = get_logger(__name__)


class AIServiceClient:
    """Client for external AI image enhancement service"""
    
    def __init__(self):
        self.api_url = settings.AI_SERVICE_API_URL
        self.api_key = settings.AI_SERVICE_API_KEY
        self.timeout = 30.0
    
    async def request_enhancement(
        self,
        image_url: str,
        job_id: str,
        webhook_url: str
    ) -> Dict[str, Any]:
        """
        Request image enhancement from AI service
        
        Args:
            image_url: URL of the original image
            job_id: Unique job ID for tracking
            webhook_url: Webhook URL for completion callback
            
        Returns:
            Response from AI service
        """
        try:
            payload = {
                "image_url": image_url,
                "job_id": job_id,
                "webhook_url": webhook_url,
                "webhook_secret": settings.AI_SERVICE_WEBHOOK_SECRET
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                
                result = response.json()
                logger.info(
                    "ai_enhancement_requested",
                    job_id=job_id,
                    ai_job_id=result.get("ai_job_id")
                )
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(
                "ai_enhancement_request_failed",
                job_id=job_id,
                status_code=e.response.status_code,
                error=str(e)
            )
            raise ImageEnhancementException(
                f"AI service returned error: {e.response.status_code}"
            )
        except Exception as e:
            logger.error("ai_enhancement_request_failed", job_id=job_id, error=str(e))
            raise ImageEnhancementException(f"Failed to request enhancement: {str(e)}")


# Global AI service client
ai_service_client = AIServiceClient()


def get_ai_client() -> AIServiceClient:
    """Dependency to get AI service client"""
    return ai_service_client
