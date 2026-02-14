"""
Property repository for database operations
"""
from typing import List, Optional, Dict, Any
from decimal import Decimal
from uuid import UUID
from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.property import Property, PropertyType
from app.models.image import PropertyImage
from app.repositories.base import BaseRepository


class PropertyRepository(BaseRepository[Property]):
    """Repository for Property model"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Property, db)
    
    async def get_with_images(self, property_id: UUID) -> Optional[Property]:
        """Get property with all images loaded"""
        result = await self.db.execute(
            select(Property)
            .options(selectinload(Property.images))
            .where(Property.id == property_id)
        )
        return result.scalar_one_or_none()
    
    async def search_properties(
        self,
        budget_min: float,
        budget_max: float,
        property_type: PropertyType,
        bhk: Optional[int] = None,
        locality: Optional[str] = None,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Property], int]:
        """
        Search properties with filters
        
        Returns:
            Tuple of (properties, total_count)
        """
        # Build base query
        query = select(Property).where(
            and_(
                Property.is_active == True,
                Property.price >= budget_min,
                Property.price <= budget_max,
                Property.property_type == property_type
            )
        )
        
        # Add optional filters
        if bhk is not None:
            query = query.where(Property.bhk == bhk)
        
        if locality:
            query = query.where(
                Property.locality.ilike(f"%{locality}%")
            )
        
        # Load images relationship
        query = query.options(selectinload(Property.images))
        
        # Order by relevance (exact locality match first, then by price)
        if locality:
            query = query.order_by(
                Property.locality.ilike(f"%{locality}%").desc(),
                Property.price.asc()
            )
        else:
            query = query.order_by(Property.price.asc())
        
        # Get total count
        count_query = select(func.count()).select_from(Property).where(
            and_(
                Property.is_active == True,
                Property.price >= budget_min,
                Property.price <= budget_max,
                Property.property_type == property_type
            )
        )
        
        if bhk is not None:
            count_query = count_query.where(Property.bhk == bhk)
        
        if locality:
            count_query = count_query.where(
                Property.locality.ilike(f"%{locality}%")
            )
        
        total_result = await self.db.execute(count_query)
        total_count = total_result.scalar_one()
        
        # Get paginated results
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        properties = result.scalars().all()
        
        return properties, total_count
    
    async def get_similar_properties(
        self,
        property_type: PropertyType,
        area_sqft: Decimal,
        exclude_id: Optional[UUID] = None,
        limit: int = 20
    ) -> List[Property]:
        """
        Get similar properties for price comparison
        
        Similar = same type, area within ±20%
        """
        area_min = area_sqft * Decimal("0.8")
        area_max = area_sqft * Decimal("1.2")
        
        query = select(Property).where(
            and_(
                Property.is_active == True,
                Property.property_type == property_type,
                Property.area_sqft >= area_min,
                Property.area_sqft <= area_max
            )
        )
        
        if exclude_id:
            query = query.where(Property.id != exclude_id)
        
        query = query.limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def increment_view_count(self, property_id: UUID) -> None:
        """Increment property view count"""
        property_obj = await self.get_by_id(property_id)
        if property_obj:
            property_obj.view_count += 1
            await self.db.flush()
    
    async def increment_inquiry_count(self, property_id: UUID) -> None:
        """Increment property inquiry count"""
        property_obj = await self.get_by_id(property_id)
        if property_obj:
            property_obj.inquiry_count += 1
            await self.db.flush()
