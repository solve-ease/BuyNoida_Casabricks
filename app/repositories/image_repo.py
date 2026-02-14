"""
Image repository for database operations
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.image import PropertyImage, EnhancementStatus
from app.repositories.base import BaseRepository


class ImageRepository(BaseRepository[PropertyImage]):
    """Repository for PropertyImage model"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(PropertyImage, db)
    
    async def get_by_property(self, property_id: UUID) -> List[PropertyImage]:
        """Get all images for a property"""
        result = await self.db.execute(
            select(PropertyImage)
            .where(PropertyImage.property_id == property_id)
            .order_by(PropertyImage.display_order.asc())
        )
        return result.scalars().all()
    
    async def get_by_ai_job_id(self, ai_job_id: str) -> Optional[PropertyImage]:
        """Get image by AI job ID"""
        result = await self.db.execute(
            select(PropertyImage)
            .where(PropertyImage.ai_job_id == ai_job_id)
        )
        return result.scalar_one_or_none()
    
    async def get_primary_image(self, property_id: UUID) -> Optional[PropertyImage]:
        """Get primary image for a property"""
        result = await self.db.execute(
            select(PropertyImage)
            .where(
                and_(
                    PropertyImage.property_id == property_id,
                    PropertyImage.is_primary == True
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_stuck_images(self, hours: int = 48) -> List[PropertyImage]:
        """
        Get images that have been processing for too long
        
        Args:
            hours: Number of hours to consider as stuck
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        result = await self.db.execute(
            select(PropertyImage)
            .where(
                and_(
                    PropertyImage.enhancement_status == EnhancementStatus.PROCESSING,
                    PropertyImage.enhancement_requested_at < cutoff_time
                )
            )
        )
        return result.scalars().all()
    
    async def mark_as_timeout(self, image_ids: List[UUID]) -> int:
        """Mark images as timed out"""
        count = 0
        for image_id in image_ids:
            image = await self.get_by_id(image_id)
            if image:
                image.enhancement_status = EnhancementStatus.TIMEOUT
                count += 1
        
        await self.db.flush()
        return count
    
    async def update_enhancement_status(
        self,
        image_id: UUID,
        status: EnhancementStatus,
        enhanced_url: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> Optional[PropertyImage]:
        """Update enhancement status"""
        image = await self.get_by_id(image_id)
        if image:
            image.enhancement_status = status
            
            if enhanced_url:
                image.enhanced_url = enhanced_url
            
            if error_message:
                image.enhancement_error_message = error_message
            
            if status == EnhancementStatus.COMPLETED or status == EnhancementStatus.FAILED:
                image.enhancement_completed_at = datetime.utcnow()
            
            await self.db.flush()
            await self.db.refresh(image)
        
        return image
