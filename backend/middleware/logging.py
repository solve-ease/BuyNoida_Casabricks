"""
Logging Middleware for Request Tracking

Automatically adds request IDs and logging context to all incoming requests.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from services.logger import ServiceLogger, generate_request_id
from typing import Callable
import time


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    - Generates unique request IDs
    - Logs incoming requests
    - Logs response status and duration
    - Makes logger available in request.state
    """
    
    def __init__(self, app, service: str = "backend"):
        super().__init__(app)
        self.service = service
        self.logger = ServiceLogger(service=service, component="middleware")
    
    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        # Generate request ID
        request_id = generate_request_id()
        
        # Create operation-specific logger
        operation_logger = self.logger.with_operation(request_id)
        
        # Make logger available in request state for other components
        request.state.logger = operation_logger
        request.state.request_id = request_id
        
        # Log incoming request
        operation_logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_ip=request.client.host if request.client else "unknown"
        )
        
        # Record start time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log response
            operation_logger.info(
                f"Request completed: {request.method} {request.url.path}",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2)
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log error
            operation_logger.error(
                f"Request failed: {request.method} {request.url.path}",
                exc_info=True,
                error=str(e),
                duration_ms=round(duration_ms, 2)
            )
            
            # Re-raise the exception
            raise
