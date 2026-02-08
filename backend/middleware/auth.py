from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Callable
import jwt
import os
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class AuthMiddleware:
    """
    JWT-based authentication middleware for FastAPI.
    Verifies JWT tokens and injects user information into request state.
    """
    
    def __init__(self, app, excluded_paths: list[str] = None):
        self.app = app
        self.excluded_paths = excluded_paths or ["/", "/docs", "/redoc", "/openapi.json"]
    
    async def __call__(self, request: Request, call_next: Callable):
        # Skip authentication for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = auth_header.split(" ")[1]
        
        try:
            # Verify and decode JWT token
            payload = verify_token(token)
            
            # Inject user information into request state
            request.state.user_id = payload.get("user_id")
            request.state.email = payload.get("email")
            request.state.role = payload.get("role", "user")
            
            logger.info(f"Authenticated user: {request.state.email}")
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed"
            )
        
        response = await call_next(request)
        return response


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    Args:
        data: Dictionary containing user information (user_id, email, role, etc.)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload


def get_current_user(request: Request) -> dict:
    """
    Get current authenticated user from request state.
    Use this as a dependency in route handlers.
    
    Args:
        request: FastAPI request object
    
    Returns:
        Dictionary with user information
    
    Example:
        @app.get("/protected")
        async def protected_route(request: Request):
            user = get_current_user(request)
            return {"user_id": user["user_id"]}
    """
    if not hasattr(request.state, "user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    
    return {
        "user_id": request.state.user_id,
        "email": request.state.email,
        "role": request.state.role
    }


def require_role(allowed_roles: list[str]):
    """
    Dependency to check if user has required role.
    
    Args:
        allowed_roles: List of roles that are allowed to access the endpoint
    
    Example:
        @app.get("/admin")
        async def admin_route(request: Request, 
                             user: dict = Depends(lambda r: require_role(["admin"])(r))):
            return {"message": "Admin access granted"}
    """
    def check_role(request: Request) -> dict:
        user = get_current_user(request)
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {allowed_roles}"
            )
        return user
    return check_role
