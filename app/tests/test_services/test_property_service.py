"""
Test property service
"""
import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.property_service import PropertyService
from app.models.property import PropertyType, ListingType
from app.schemas.property import PropertyCreate


@pytest.mark.asyncio
async def test_create_property(db_session: AsyncSession, test_user):
    """Test creating a property"""
    service = PropertyService(db_session)
    
    property_data = PropertyCreate(
        title="Test Property",
        description="A test property",
        locality="Sector 62",
        sector="62",
        latitude=Decimal("28.6139"),
        longitude=Decimal("77.2090"),
        property_type=PropertyType.FLAT,
        listing_type=ListingType.SALE,
        bhk=3,
        area_sqft=Decimal("1500"),
        price=Decimal("7500000"),
        vastu_score=75,
        natural_light_score=80
    )
    
    property_obj = await service.create_property(property_data, test_user.id)
    
    assert property_obj.id is not None
    assert property_obj.title == "Test Property"
    assert property_obj.bhk == 3
    assert property_obj.is_active is True


@pytest.mark.asyncio
async def test_get_property_detail(db_session: AsyncSession, test_user):
    """Test getting property detail"""
    service = PropertyService(db_session)
    
    # Create property
    property_data = PropertyCreate(
        title="Test Property",
        locality="Sector 62",
        sector="62",
        latitude=Decimal("28.6139"),
        longitude=Decimal("77.2090"),
        property_type=PropertyType.FLAT,
        listing_type=ListingType.SALE,
        bhk=2,
        area_sqft=Decimal("1200"),
        price=Decimal("6000000"),
        vastu_score=70,
        natural_light_score=75
    )
    
    property_obj = await service.create_property(property_data, test_user.id)
    await db_session.commit()
    
    # Get detail
    detail = await service.get_property_detail(property_obj.id)
    
    assert detail.id == property_obj.id
    assert detail.title == "Test Property"
    assert detail.view_count == 1  # Incremented on get
