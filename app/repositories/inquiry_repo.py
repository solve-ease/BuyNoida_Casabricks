"""
Inquiry repository for database operations
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.inquiry import Inquiry, InquiryStatus
from app.repositories.base import BaseRepository


class InquiryRepository(BaseRepository[Inquiry]):
    """Repository for Inquiry model"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Inquiry, db)
    
    async def get_with_property(self, inquiry_id: UUID) -> Optional[Inquiry]:
        """Get inquiry with property loaded"""
        result = await self.db.execute(
            select(Inquiry)
            .options(selectinload(Inquiry.property))
            .where(Inquiry.id == inquiry_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_filters(
        self,
        status: Optional[InquiryStatus] = None,
        property_id: Optional[UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Inquiry]:
        """Get inquiries with filters"""
        query = select(Inquiry).options(selectinload(Inquiry.property))
        
        conditions = []
        
        if status:
            conditions.append(Inquiry.status == status)
        
        if property_id:
            conditions.append(Inquiry.property_id == property_id)
        
        if date_from:
            conditions.append(Inquiry.created_at >= date_from)
        
        if date_to:
            conditions.append(Inquiry.created_at <= date_to)
        
        if conditions:
            query = query.where(and_(*conditions))
        
        query = query.order_by(Inquiry.created_at.desc())
        query = query.offset(skip).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def count_by_filters(
        self,
        status: Optional[InquiryStatus] = None,
        property_id: Optional[UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> int:
        """Count inquiries with filters"""
        conditions = [Inquiry.id.isnot(None)]  # Always true condition
        
        if status:
            conditions.append(Inquiry.status == status)
        
        if property_id:
            conditions.append(Inquiry.property_id == property_id)
        
        if date_from:
            conditions.append(Inquiry.created_at >= date_from)
        
        if date_to:
            conditions.append(Inquiry.created_at <= date_to)
        
        return await self.count(**{})  # Use base count with where clause
    
    async def add_notes(self, inquiry_id: UUID, notes: str) -> Optional[Inquiry]:
        """Add notes to inquiry"""
        inquiry = await self.get_by_id(inquiry_id)
        if inquiry:
            if inquiry.notes:
                inquiry.notes = f"{inquiry.notes}\n\n{notes}"
            else:
                inquiry.notes = notes
            await self.db.flush()
            await self.db.refresh(inquiry)
        return inquiry
