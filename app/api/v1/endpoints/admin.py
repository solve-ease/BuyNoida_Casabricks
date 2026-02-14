"""
Admin endpoints for property and inquiry management
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.property import PropertyCreate, PropertyUpdate, PropertyDetail, PropertyListResponse, PropertySearchResult
from app.schemas.inquiry import InquiryDetail, InquiryStatusUpdate, InquiryNotesUpdate
from app.schemas.image import ImageUploadResponse
from app.schemas.common import SuccessResponse
from app.services.property_service import PropertyService
from app.services.inquiry_service import InquiryService
from app.services.image_service import ImageService
from app.api.dependencies import get_current_admin_user
from app.models.user import User
from app.models.inquiry import InquiryStatus
from app.models.image import ImageType
from app.core.exceptions import PropertyNotFoundException, InquiryNotFoundException, ImageNotFoundException

router = APIRouter(prefix="/admin", tags=["Admin"])


# ============= Property Management =============

@router.post("/properties", response_model=PropertyDetail, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Create a new property listing (Admin only)
    
    Requires admin authentication
    """
    property_service = PropertyService(db)
    property_obj = await property_service.create_property(
        property_data=property_data,
        created_by=current_user.id
    )
    
    await db.commit()
    
    return await property_service.get_property_detail(property_obj.id)


@router.put("/properties/{property_id}", response_model=PropertyDetail)
async def update_property(
    property_id: UUID,
    property_data: PropertyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update a property listing (Admin only)
    
    Requires admin authentication
    """
    property_service = PropertyService(db)
    
    try:
        await property_service.update_property(property_id, property_data)
        return await property_service.get_property_detail(property_id)
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/properties/{property_id}", response_model=SuccessResponse)
async def delete_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Soft delete a property (sets is_active=False) (Admin only)
    
    Requires admin authentication
    """
    property_service = PropertyService(db)
    
    try:
        await property_service.delete_property(property_id)
        return SuccessResponse(message="Property deleted successfully")
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.patch("/properties/{property_id}/status", response_model=PropertyDetail)
async def toggle_property_status(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Toggle property active status (Admin only)
    
    Requires admin authentication
    """
    property_service = PropertyService(db)
    
    try:
        await property_service.toggle_property_status(property_id)
        return await property_service.get_property_detail(property_id)
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# ============= Image Management =============

@router.post("/properties/{property_id}/images", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_property_image(
    property_id: UUID,
    file: UploadFile = File(...),
    image_type: ImageType = Form(ImageType.OTHER),
    is_primary: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Upload an image for a property (Admin only)
    
    - Validates file type (jpg, jpeg, png, webp)
    - Validates file size (max 10MB)
    - Uploads to Supabase Storage
    - Creates database record with status 'pending'
    
    Requires admin authentication
    """
    image_service = ImageService(db)
    
    # Read file content
    file_content = await file.read()
    
    try:
        image = await image_service.upload_image(
            property_id=property_id,
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
            image_type=image_type,
            is_primary=is_primary
        )
        
        return ImageUploadResponse.model_validate(image)
        
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/images/{image_id}", response_model=SuccessResponse)
async def delete_image(
    image_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Delete an image (Admin only)
    
    Deletes from storage and database
    
    Requires admin authentication
    """
    image_service = ImageService(db)
    
    try:
        await image_service.delete_image(image_id)
        return SuccessResponse(message="Image deleted successfully")
    except ImageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/images/{image_id}/enhance")
async def enhance_image(
    image_id: UUID,
    request_url: str = Query(..., description="Base URL for webhook callback"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Trigger AI enhancement for an image (Admin only)
    
    - Checks image status (must be 'pending' or 'failed')
    - Sends request to external AI service
    - Updates status to 'processing'
    - AI service will call webhook when complete
    
    Requires admin authentication
    """
    image_service = ImageService(db)
    
    try:
        result = await image_service.request_enhancement(image_id, request_url)
        return result
    except ImageNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============= Inquiry Management =============

@router.get("/inquiries", response_model=List[InquiryDetail])
async def list_inquiries(
    status: Optional[InquiryStatus] = None,
    property_id: Optional[UUID] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    List inquiries with filters (Admin only)
    
    Optional filters:
    - **status**: Filter by inquiry status
    - **property_id**: Filter by property
    - **date_from**: Filter by date range (start)
    - **date_to**: Filter by date range (end)
    
    Requires admin authentication
    """
    inquiry_service = InquiryService(db)
    
    inquiries = await inquiry_service.list_inquiries(
        status=status,
        property_id=property_id,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit
    )
    
    return [InquiryDetail.model_validate(inq) for inq in inquiries]


@router.get("/inquiries/{inquiry_id}", response_model=InquiryDetail)
async def get_inquiry_detail(
    inquiry_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get inquiry details (Admin only)
    
    Requires admin authentication
    """
    inquiry_service = InquiryService(db)
    
    inquiry = await inquiry_service.get_inquiry(inquiry_id)
    
    if not inquiry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inquiry not found"
        )
    
    return InquiryDetail.model_validate(inquiry)


@router.patch("/inquiries/{inquiry_id}/status", response_model=InquiryDetail)
async def update_inquiry_status(
    inquiry_id: UUID,
    status_update: InquiryStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Update inquiry status (Admin only)
    
    Requires admin authentication
    """
    inquiry_service = InquiryService(db)
    
    try:
        inquiry = await inquiry_service.update_inquiry_status(
            inquiry_id,
            status_update.status
        )
        return InquiryDetail.model_validate(inquiry)
    except InquiryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/inquiries/{inquiry_id}/notes", response_model=InquiryDetail)
async def add_inquiry_notes(
    inquiry_id: UUID,
    notes_data: InquiryNotesUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Add notes to inquiry (Admin only)
    
    Requires admin authentication
    """
    inquiry_service = InquiryService(db)
    
    try:
        inquiry = await inquiry_service.add_notes(inquiry_id, notes_data.notes)
        return InquiryDetail.model_validate(inquiry)
    except InquiryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
