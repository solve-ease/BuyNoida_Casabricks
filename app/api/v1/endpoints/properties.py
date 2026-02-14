"""
Property endpoints
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.property import PropertyDetail
from app.services.property_service import PropertyService
from app.core.exceptions import PropertyNotFoundException

router = APIRouter(prefix="/properties", tags=["Properties"])


@router.get("/{property_id}", response_model=PropertyDetail)
async def get_property_detail(
    property_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get property detail by ID
    
    Returns complete property information including:
    - All property fields
    - Images (with enhanced URLs if available)
    - Facing direction widget data
    - Price comparison data
    
    This endpoint also increments the property view count
    """
    property_service = PropertyService(db)
    
    try:
        property_detail = await property_service.get_property_detail(property_id)
        return property_detail
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
