"""
Error handling middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.exceptions import BaseAPIException
from app.core.logging import get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and return consistent error responses"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except BaseAPIException as e:
            # Handle custom API exceptions
            logger.warning(
                "api_exception",
                path=request.url.path,
                error=e.message,
                status_code=e.status_code
            )
            
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error": e.message,
                    "detail": None
                }
            )
        except Exception as e:
            # Handle unexpected exceptions
            logger.error(
                "unhandled_exception",
                path=request.url.path,
                error=str(e),
                error_type=type(e).__name__
            )
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": "Internal server error",
                    "detail": str(e) if logger._logger.level == 10 else None  # Show details only in DEBUG
                }
            )
