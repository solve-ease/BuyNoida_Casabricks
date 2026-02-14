"""
Property service for business logic
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property, PropertyType
from app.repositories.property_repo import PropertyRepository
from app.repositories.image_repo import ImageRepository
from app.schemas.property import (
    PropertyCreate,
    PropertyUpdate,
    PropertyDetail,
    FacingWidgetData,
    PriceComparisonData,
    ImageResponse,
    KeyMetrics
)
from app.core.exceptions import PropertyNotFoundException
from app.core.utils import calculate_price_category, calculate_facing_metrics
from app.core.logging import get_logger

logger = get_logger(__name__)


class PropertyService:
    """Service for property operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.property_repo = PropertyRepository(db)
        self.image_repo = ImageRepository(db)
    
    async def create_property(
        self,
        property_data: PropertyCreate,
        created_by: UUID
    ) -> Property:
        """Create a new property"""
        property_dict = property_data.model_dump()
        property_dict["created_by"] = created_by
        
        property_obj = await self.property_repo.create(**property_dict)
        
        logger.info(
            "property_created",
            property_id=str(property_obj.id),
            property_type=property_obj.property_type.value
        )
        
        return property_obj
    
    async def get_property(self, property_id: UUID) -> Optional[Property]:
        """Get property by ID"""
        property_obj = await self.property_repo.get_with_images(property_id)
        
        if property_obj:
            # Increment view count
            await self.property_repo.increment_view_count(property_id)
            await self.db.commit()
        
        return property_obj
    
    async def get_property_detail(self, property_id: UUID) -> PropertyDetail:
        """Get property detail with enriched data"""
        property_obj = await self.get_property(property_id)
        
        if not property_obj:
            raise PropertyNotFoundException(str(property_id))
        
        # Convert property to detail schema
        property_dict = {
            "id": property_obj.id,
            "title": property_obj.title,
            "description": property_obj.description,
            "locality": property_obj.locality,
            "sector": property_obj.sector,
            "latitude": property_obj.latitude,
            "longitude": property_obj.longitude,
            "property_type": property_obj.property_type.value,
            "listing_type": property_obj.listing_type.value,
            "bhk": property_obj.bhk,
            "area_sqft": property_obj.area_sqft,
            "price": property_obj.price,
            "price_per_sqft": property_obj.price_per_sqft,
            "facing_direction": property_obj.facing_direction.value if property_obj.facing_direction else None,
            "furnishing_status": property_obj.furnishing_status.value if property_obj.furnishing_status else None,
            "floor_number": property_obj.floor_number,
            "total_floors": property_obj.total_floors,
            "age_years": property_obj.age_years,
            "vastu_score": property_obj.vastu_score,
            "natural_light_score": property_obj.natural_light_score,
            "is_active": property_obj.is_active,
            "view_count": property_obj.view_count,
            "inquiry_count": property_obj.inquiry_count,
            "created_at": property_obj.created_at,
            "updated_at": property_obj.updated_at,
            "images": [ImageResponse.model_validate(img) for img in property_obj.images]
        }
        
        # Add facing widget data
        if property_obj.facing_direction:
            facing_metrics = calculate_facing_metrics(property_obj.facing_direction.value)
            property_dict["facing_widget_data"] = FacingWidgetData(
                direction=property_obj.facing_direction.value,
                **facing_metrics
            )
        
        # Add price comparison data
        price_comparison = await self._calculate_price_comparison(property_obj)
        if price_comparison:
            property_dict["price_comparison"] = price_comparison
        
        return PropertyDetail(**property_dict)
    
    async def update_property(
        self,
        property_id: UUID,
        property_data: PropertyUpdate
    ) -> Property:
        """Update a property"""
        property_obj = await self.property_repo.get_by_id(property_id)
        
        if not property_obj:
            raise PropertyNotFoundException(str(property_id))
        
        # Update only provided fields
        update_dict = property_data.model_dump(exclude_unset=True)
        updated_property = await self.property_repo.update(property_id, **update_dict)
        
        await self.db.commit()
        
        logger.info("property_updated", property_id=str(property_id))
        
        return updated_property
    
    async def delete_property(self, property_id: UUID) -> bool:
        """Soft delete a property (set is_active=False)"""
        property_obj = await self.property_repo.get_by_id(property_id)
        
        if not property_obj:
            raise PropertyNotFoundException(str(property_id))
        
        await self.property_repo.update(property_id, is_active=False)
        await self.db.commit()
        
        logger.info("property_deleted", property_id=str(property_id))
        
        return True
    
    async def toggle_property_status(self, property_id: UUID) -> Property:
        """Toggle property active status"""
        property_obj = await self.property_repo.get_by_id(property_id)
        
        if not property_obj:
            raise PropertyNotFoundException(str(property_id))
        
        new_status = not property_obj.is_active
        updated_property = await self.property_repo.update(
            property_id,
            is_active=new_status
        )
        await self.db.commit()
        
        logger.info(
            "property_status_toggled",
            property_id=str(property_id),
            new_status=new_status
        )
        
        return updated_property
    
    async def _calculate_price_comparison(
        self,
        property_obj: Property
    ) -> Optional[PriceComparisonData]:
        """Calculate price comparison with similar properties"""
        similar_properties = await self.property_repo.get_similar_properties(
            property_type=property_obj.property_type,
            area_sqft=property_obj.area_sqft,
            exclude_id=property_obj.id
        )
        
        if not similar_properties:
            return None
        
        # Calculate average price per sqft
        total_price_per_sqft = sum(
            float(p.price / p.area_sqft) for p in similar_properties
        )
        avg_price_per_sqft = Decimal(str(total_price_per_sqft / len(similar_properties)))
        
        property_price_per_sqft = property_obj.price / property_obj.area_sqft
        
        # Calculate difference percentage
        difference = property_price_per_sqft - avg_price_per_sqft
        difference_pct = (difference / avg_price_per_sqft * 100) if avg_price_per_sqft > 0 else Decimal(0)
        
        # Determine category
        category = calculate_price_category(property_price_per_sqft, avg_price_per_sqft)
        
        return PriceComparisonData(
            property_price_per_sqft=property_price_per_sqft,
            similar_properties_avg_price=avg_price_per_sqft,
            difference_percentage=difference_pct,
            category=category
        )
    
    async def get_key_metrics(self, property_obj: Property) -> KeyMetrics:
        """Get key metrics for property search results"""
        # Calculate price vs market
        price_per_sqft = property_obj.price / property_obj.area_sqft
        
        similar_properties = await self.property_repo.get_similar_properties(
            property_type=property_obj.property_type,
            area_sqft=property_obj.area_sqft,
            exclude_id=property_obj.id
        )
        
        if similar_properties:
            avg_price_per_sqft = Decimal(
                str(sum(float(p.price / p.area_sqft) for p in similar_properties) / len(similar_properties))
            )
            price_category = calculate_price_category(price_per_sqft, avg_price_per_sqft)
        else:
            price_category = "average"
        
        return KeyMetrics(
            vastu_score=property_obj.vastu_score,
            natural_light_score=property_obj.natural_light_score,
            price_vs_market=price_category
        )
