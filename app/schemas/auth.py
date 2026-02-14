"""
Authentication schemas
"""
from pydantic import BaseModel, EmailStr, Field, UUID4


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response schema"""
    id: UUID4
    email: str
    full_name: str
    role: str
    is_active: bool
    
    model_config = {"from_attributes": True}
