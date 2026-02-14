"""
Search schemas for guided property search
"""
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.property import PropertyType
from app.schemas.property import PropertySearchResult


class GuidedSearchRequest(BaseModel):
    """Guided search request schema"""
    budget_min: float = Field(..., gt=0, description="Minimum budget")
    budget_max: float = Field(..., gt=0, description="Maximum budget")
    property_type: PropertyType = Field(..., description="Type of property")
    bhk: Optional[int] = Field(None, ge=1, le=10, description="Number of BHK (optional)")
    locality_preference: Optional[str] = Field(None, max_length=255, description="Preferred locality (optional)")
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Results per page")
    
    def validate_budget(self) -> "GuidedSearchRequest":
        """Validate that max budget is greater than min budget"""
        if self.budget_max <= self.budget_min:
            raise ValueError("budget_max must be greater than budget_min")
        return self


class GuidedSearchResponse(BaseModel):
    """Guided search response schema"""
    results: List[PropertySearchResult]
    total_count: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_prev: bool
    filters_applied: dict
