"""
Search service for guided property search
"""
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property
from app.repositories.property_repo import PropertyRepository
from app.schemas.search import GuidedSearchRequest, GuidedSearchResponse
from app.schemas.property import PropertySearchResult, ImageResponse
from app.services.property_service import PropertyService
from app.core.logging import get_logger
from app.core.metrics import search_queries_total

logger = get_logger(__name__)


class SearchService:
    """Service for property search operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.property_repo = PropertyRepository(db)
        self.property_service = PropertyService(db)
    
    async def guided_search(
        self,
        search_request: GuidedSearchRequest
    ) -> GuidedSearchResponse:
        """
        Perform guided property search
        
        Args:
            search_request: Search parameters from user
            
        Returns:
            Search results with pagination
        """
        # Track metric
        search_queries_total.labels(
            property_type=search_request.property_type.value
        ).inc()
        
        # Calculate pagination
        skip = (search_request.page - 1) * search_request.per_page
        
        # Search properties
        properties, total_count = await self.property_repo.search_properties(
            budget_min=search_request.budget_min,
            budget_max=search_request.budget_max,
            property_type=search_request.property_type,
            bhk=search_request.bhk,
            locality=search_request.locality_preference,
            skip=skip,
            limit=search_request.per_page
        )
        
        # Convert to search results
        results = []
        for property_obj in properties:
            result = await self._property_to_search_result(property_obj)
            results.append(result)
        
        # Calculate pagination info
        total_pages = (total_count + search_request.per_page - 1) // search_request.per_page
        has_next = search_request.page < total_pages
        has_prev = search_request.page > 1
        
        # Build filters applied dict
        filters_applied = {
            "budget_range": f"₹{search_request.budget_min:,.0f} - ₹{search_request.budget_max:,.0f}",
            "property_type": search_request.property_type.value,
        }
        
        if search_request.bhk:
            filters_applied["bhk"] = search_request.bhk
        
        if search_request.locality_preference:
            filters_applied["locality"] = search_request.locality_preference
        
        logger.info(
            "search_performed",
            property_type=search_request.property_type.value,
            results_count=len(results),
            total_count=total_count
        )
        
        return GuidedSearchResponse(
            results=results,
            total_count=total_count,
            page=search_request.page,
            per_page=search_request.per_page,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev,
            filters_applied=filters_applied
        )
    
    async def _property_to_search_result(
        self,
        property_obj: Property
    ) -> PropertySearchResult:
        """Convert Property model to PropertySearchResult schema"""
        # Get primary image
        primary_image = None
        if property_obj.images:
            primary = next((img for img in property_obj.images if img.is_primary), None)
            if primary:
                primary_image = ImageResponse.model_validate(primary)
            elif property_obj.images:
                # Use first image if no primary set
                primary_image = ImageResponse.model_validate(property_obj.images[0])
        
        # Get key metrics
        key_metrics = await self.property_service.get_key_metrics(property_obj)
        
        return PropertySearchResult(
            id=property_obj.id,
            title=property_obj.title,
            price=property_obj.price,
            area_sqft=property_obj.area_sqft,
            price_per_sqft=property_obj.price_per_sqft,
            locality=property_obj.locality,
            sector=property_obj.sector,
            bhk=property_obj.bhk,
            property_type=property_obj.property_type.value,
            listing_type=property_obj.listing_type.value,
            primary_image=primary_image,
            key_metrics=key_metrics
        )
