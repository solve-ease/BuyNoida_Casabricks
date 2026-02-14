"""
Inquiry endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.inquiry import InquiryCreate, InquiryResponse
from app.schemas.common import SuccessResponse
from app.services.inquiry_service import InquiryService
from app.api.dependencies import get_client_ip, get_user_agent, check_rate_limit
from app.core.exceptions import PropertyNotFoundException

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("", response_model=InquiryResponse, status_code=status.HTTP_201_CREATED)
async def create_inquiry(
    inquiry_data: InquiryCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(check_rate_limit)  # Check rate limit
):
    """
    Submit a property inquiry
    
    Creates a new inquiry/lead for the specified property.
    
    **Rate Limit**: 5 inquiries per hour per IP address
    
    Required fields:
    - **property_id**: UUID of the property
    - **full_name**: Full name (2-255 characters)
    - **email**: Valid email address
    - **phone**: Indian phone number format (+91XXXXXXXXXX)
    - **inquiry_type**: general, callback, or site_visit (default: general)
    
    Optional fields:
    - **message**: Additional message (max 2000 characters)
    - **preferred_contact_time**: Preferred time for contact
    
    This endpoint:
    - Validates all fields
    - Tracks source, user agent, and IP address
    - Increments property inquiry count
    - Returns 429 if rate limit exceeded
    """
    inquiry_service = InquiryService(db)
    
    # Get client info
    ip_address = await get_client_ip(request)
    user_agent = await get_user_agent(request)
    
    try:
        inquiry = await inquiry_service.create_inquiry(
            inquiry_data=inquiry_data,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return InquiryResponse.model_validate(inquiry)
        
    except PropertyNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
