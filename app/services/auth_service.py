"""
Authentication service
"""
from typing import Optional
from datetime import timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.exceptions import UnauthorizedException
from app.core.logging import get_logger
from app.config.settings import settings

logger = get_logger(__name__)


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        # Get user by email
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            logger.warning("auth_failed_user_not_found", email=email)
            return None
        
        # Check if user is active
        if not user.is_active:
            logger.warning("auth_failed_user_inactive", email=email)
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            logger.warning("auth_failed_invalid_password", email=email)
            return None
        
        logger.info("auth_success", user_id=str(user.id), email=email)
        return user
    
    async def login(self, email: str, password: str) -> dict:
        """
        Login user and generate access token
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Dict with access_token and token_type
            
        Raises:
            UnauthorizedException if authentication fails
        """
        user = await self.authenticate_user(email, password)
        
        if not user:
            raise UnauthorizedException("Invalid email or password")
        
        # Create access token
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value
            },
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # in seconds
        }
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
