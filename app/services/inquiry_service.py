"""
Inquiry service for lead management
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inquiry import Inquiry, InquiryStatus, InquirySource
from app.repositories.inquiry_repo import InquiryRepository
from app.repositories.property_repo import PropertyRepository
from app.schemas.inquiry import InquiryCreate, InquiryResponse
from app.core.exceptions import InquiryNotFoundException, PropertyNotFoundException
from app.core.logging import get_logger
from app.core.metrics import inquiries_submitted_total

logger = get_logger(__name__)


class InquiryService:
    """Service for inquiry operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.inquiry_repo = InquiryRepository(db)
        self.property_repo = PropertyRepository(db)
    
    async def create_inquiry(
        self,
        inquiry_data: InquiryCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Inquiry:
        """Create a new inquiry"""
        # Verify property exists
        property_obj = await self.property_repo.get_by_id(inquiry_data.property_id)
        if not property_obj:
            raise PropertyNotFoundException(str(inquiry_data.property_id))
        
        # Create inquiry
        inquiry_dict = inquiry_data.model_dump()
        inquiry_dict["source"] = InquirySource.WEB
        inquiry_dict["ip_address"] = ip_address
        inquiry_dict["user_agent"] = user_agent
        
        inquiry = await self.inquiry_repo.create(**inquiry_dict)
        
        # Increment property inquiry count
        await self.property_repo.increment_inquiry_count(inquiry_data.property_id)
        
        await self.db.commit()
        
        # Track metric
        inquiries_submitted_total.labels(
            inquiry_type=inquiry_data.inquiry_type.value
        ).inc()
        
        logger.info(
            "inquiry_created",
            inquiry_id=str(inquiry.id),
            property_id=str(inquiry_data.property_id),
            inquiry_type=inquiry_data.inquiry_type.value
        )
        
        return inquiry
    
    async def get_inquiry(self, inquiry_id: UUID) -> Optional[Inquiry]:
        """Get inquiry by ID"""
        return await self.inquiry_repo.get_with_property(inquiry_id)
    
    async def list_inquiries(
        self,
        status: Optional[InquiryStatus] = None,
        property_id: Optional[UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inquiry]:
        """List inquiries with filters"""
        return await self.inquiry_repo.get_by_filters(
            status=status,
            property_id=property_id,
            date_from=date_from,
            date_to=date_to,
            skip=skip,
            limit=limit
        )
    
    async def update_inquiry_status(
        self,
        inquiry_id: UUID,
        status: InquiryStatus
    ) -> Inquiry:
        """Update inquiry status"""
        inquiry = await self.inquiry_repo.get_by_id(inquiry_id)
        
        if not inquiry:
            raise InquiryNotFoundException(str(inquiry_id))
        
        updated_inquiry = await self.inquiry_repo.update(inquiry_id, status=status)
        await self.db.commit()
        
        logger.info(
            "inquiry_status_updated",
            inquiry_id=str(inquiry_id),
            new_status=status.value
        )
        
        return updated_inquiry
    
    async def add_notes(self, inquiry_id: UUID, notes: str) -> Inquiry:
        """Add notes to inquiry"""
        inquiry = await self.inquiry_repo.add_notes(inquiry_id, notes)
        
        if not inquiry:
            raise InquiryNotFoundException(str(inquiry_id))
        
        await self.db.commit()
        
        logger.info("inquiry_notes_added", inquiry_id=str(inquiry_id))
        
        return inquiry
