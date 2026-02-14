"""
API dependencies for authentication and database session
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException
from app.models.user import User, UserRole
from app.services.auth_service import AuthService
from app.infrastructure.cache.redis_client import get_redis, RedisClient
from app.core.logging import get_logger

logger = get_logger(__name__)

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException if authentication fails
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_access_token(token)
    
    if not payload:
        logger.warning("invalid_token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        logger.warning("token_missing_sub")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Get user from database
    auth_service = AuthService(db)
    user = await auth_service.get_user_by_id(user_id)
    
    if not user:
        logger.warning("user_not_found", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        logger.warning("user_inactive", user_id=user_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is inactive"
        )
    
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is an admin
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user if admin
        
    Raises:
        HTTPException if user is not admin
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        logger.warning(
            "unauthorized_access_attempt",
            user_id=str(current_user.id),
            role=current_user.role.value
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


async def get_client_ip(request: Request) -> str:
    """
    Get client IP address from request
    
    Args:
        request: FastAPI request
        
    Returns:
        Client IP address
    """
    # Check for X-Forwarded-For header (proxy/load balancer)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For can contain multiple IPs, get the first one
        return forwarded_for.split(",")[0].strip()
    
    # Fall back to direct connection IP
    return request.client.host if request.client else "unknown"


async def get_user_agent(request: Request) -> str:
    """
    Get user agent from request
    
    Args:
        request: FastAPI request
        
    Returns:
        User agent string
    """
    return request.headers.get("User-Agent", "unknown")


async def check_rate_limit(
    request: Request,
    redis: RedisClient = Depends(get_redis)
) -> None:
    """
    Check rate limit for inquiries
    
    Args:
        request: FastAPI request
        redis: Redis client
        
    Raises:
        HTTPException if rate limit exceeded
    """
    from app.config.settings import settings
    
    # Get client IP
    client_ip = await get_client_ip(request)
    
    # Key for rate limiting
    key = f"rate_limit:inquiry:{client_ip}"
    
    # Get current count
    current_count = await redis.get(key)
    
    if current_count is None:
        # First request in this hour
        await redis.set(key, 1, expire=3600)  # 1 hour
    else:
        current_count = int(current_count)
        
        if current_count >= settings.RATE_LIMIT_INQUIRIES_PER_HOUR:
            logger.warning(
                "rate_limit_exceeded",
                client_ip=client_ip,
                count=current_count
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_INQUIRIES_PER_HOUR} inquiries per hour."
            )
        
        await redis.increment(key)
