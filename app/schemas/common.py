"""
Common schemas used across the application
"""
from typing import Optional
from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1, description="Page number")
    per_page: int = Field(default=20, ge=1, le=100, description="Results per page")


class PageInfo(BaseModel):
    """Pagination information"""
    page: int
    per_page: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None
