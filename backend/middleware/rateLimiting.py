from fastapi import Request, HTTPException, status
from typing import Callable, Optional
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    IP-based rate limiting middleware for FastAPI.
    Tracks requests per IP address and enforces configurable rate limits.
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        cleanup_interval: int = 300,  # Cleanup old entries every 5 minutes
        excluded_paths: list[str] = None
    ):
        """
        Initialize rate limiter.
        
        Args:
            app: FastAPI application instance
            requests_per_minute: Maximum requests allowed per minute per IP
            requests_per_hour: Maximum requests allowed per hour per IP
            cleanup_interval: How often to clean old entries (seconds)
            excluded_paths: Paths to exclude from rate limiting
        """
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.excluded_paths = excluded_paths or ["/", "/docs", "/redoc", "/openapi.json"]
        
        # Storage for request timestamps
        # Format: {ip: {"minute": [timestamps], "hour": [timestamps]}}
        self.request_history: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: {"minute": [], "hour": []}
        )
        
        # Start cleanup task
        self.cleanup_interval = cleanup_interval
        self._cleanup_task = None
    
    async def __call__(self, request: Request, call_next: Callable):
        # Skip rate limiting for excluded paths
        if request.url.path in self.excluded_paths:
            return await call_next(request)
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check rate limits
        current_time = time.time()
        
        try:
            self._check_rate_limit(client_ip, current_time)
        except HTTPException as e:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise e
        
        # Record this request
        self.request_history[client_ip]["minute"].append(current_time)
        self.request_history[client_ip]["hour"].append(current_time)
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        minute_count = len(self.request_history[client_ip]["minute"])
        hour_count = len(self.request_history[client_ip]["hour"])
        
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            max(0, self.requests_per_minute - minute_count)
        )
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            max(0, self.requests_per_hour - hour_count)
        )
        
        return response
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request.
        Handles X-Forwarded-For and X-Real-IP headers for proxy situations.
        """
        # Check for forwarded IP (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        return request.client.host if request.client else "unknown"
    
    def _check_rate_limit(self, client_ip: str, current_time: float):
        """
        Check if client has exceeded rate limits.
        
        Args:
            client_ip: Client IP address
            current_time: Current timestamp
        
        Raises:
            HTTPException: If rate limit is exceeded
        """
        history = self.request_history[client_ip]
        
        # Clean old entries for this IP
        one_minute_ago = current_time - 60
        one_hour_ago = current_time - 3600
        
        history["minute"] = [
            ts for ts in history["minute"] if ts > one_minute_ago
        ]
        history["hour"] = [
            ts for ts in history["hour"] if ts > one_hour_ago
        ]
        
        # Check minute limit
        if len(history["minute"]) >= self.requests_per_minute:
            oldest_request = min(history["minute"])
            retry_after = int(60 - (current_time - oldest_request))
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.requests_per_minute} requests per minute",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Window": "minute"
                }
            )
        
        # Check hour limit
        if len(history["hour"]) >= self.requests_per_hour:
            oldest_request = min(history["hour"])
            retry_after = int(3600 - (current_time - oldest_request))
            
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.requests_per_hour} requests per hour",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(self.requests_per_hour),
                    "X-RateLimit-Window": "hour"
                }
            )
    
    async def cleanup_old_entries(self):
        """
        Periodically clean up old request history entries to prevent memory leaks.
        This should be run as a background task.
        """
        while True:
            await asyncio.sleep(self.cleanup_interval)
            
            current_time = time.time()
            one_hour_ago = current_time - 3600
            
            # Remove IPs with no recent requests
            ips_to_remove = []
            for ip, history in self.request_history.items():
                if not history["hour"] or max(history["hour"]) < one_hour_ago:
                    ips_to_remove.append(ip)
            
            for ip in ips_to_remove:
                del self.request_history[ip]
            
            if ips_to_remove:
                logger.info(f"Cleaned up rate limit history for {len(ips_to_remove)} IPs")


class RateLimitByEndpoint:
    """
    Endpoint-specific rate limiting.
    Allows different rate limits for different endpoints.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.request_history: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: {"minute": [], "hour": []}
        )
    
    async def __call__(self, request: Request, call_next: Callable):
        # Get unique identifier (IP + endpoint)
        client_ip = self._get_client_ip(request)
        endpoint = request.url.path
        identifier = f"{client_ip}:{endpoint}"
        
        current_time = time.time()
        
        # Check and record
        self._check_and_record(identifier, current_time)
        
        return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
    
    def _check_and_record(self, identifier: str, current_time: float):
        history = self.request_history[identifier]
        
        one_minute_ago = current_time - 60
        one_hour_ago = current_time - 3600
        
        history["minute"] = [ts for ts in history["minute"] if ts > one_minute_ago]
        history["hour"] = [ts for ts in history["hour"] if ts > one_hour_ago]
        
        if len(history["minute"]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Endpoint rate limit exceeded: {self.requests_per_minute} requests per minute"
            )
        
        if len(history["hour"]) >= self.requests_per_hour:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Endpoint rate limit exceeded: {self.requests_per_hour} requests per hour"
            )
        
        history["minute"].append(current_time)
        history["hour"].append(current_time)
