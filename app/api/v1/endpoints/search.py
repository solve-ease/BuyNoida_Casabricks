"""
Search endpoints for guided property search
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.search import GuidedSearchRequest, GuidedSearchResponse
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/guided", response_model=GuidedSearchResponse)
async def guided_search(
    search_request: GuidedSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Guided property search endpoint
    
    This endpoint replaces traditional filter-heavy search with a simple 3-question guided flow:
    
    - **budget_min**: Minimum budget in INR
    - **budget_max**: Maximum budget in INR  
    - **property_type**: Type of property (flat, villa, plot, commercial)
    - **bhk**: Optional - Number of bedrooms (1-10)
    - **locality_preference**: Optional - Preferred locality/area name
    
    Returns matching properties with pagination and key metrics
    """
    # Validate budget
    search_request.validate_budget()
    
    search_service = SearchService(db)
    results = await search_service.guided_search(search_request)
    
    return results
