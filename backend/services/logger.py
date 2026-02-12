"""
Structured Logging System for BuyNoida Backend

This module provides a comprehensive logging system that tags logs with:
- Service name
- Component name
- Operation ID (e.g., request ID)
- File location
- Severity level
- Timestamp
"""

import logging
import json
import inspect
from datetime import datetime, timezone
from typing import Optional, Any, Dict
from enum import Enum
from pathlib import Path


class LogLevel(Enum):
    """Log severity levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": getattr(record, 'service', 'unknown'),
            "component": getattr(record, 'component', 'unknown'),
            "operation_id": getattr(record, 'operation_id', None),
            "file": f"{record.filename}:{record.lineno}",
            "function": record.funcName,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_data['data'] = record.extra_data
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, indent=2)


class ServiceLogger:
    """
    Service-aware logger that adds context to all log messages.
    
    Usage:
        logger = ServiceLogger(service="backend", component="auth")
        logger.info("User logged in", operation_id="req-123", user_id=42)
        logger.error("Database connection failed", operation_id="req-124", error="timeout")
    """
    
    def __init__(
        self,
        service: str,
        component: str,
        log_level: LogLevel = LogLevel.INFO
    ):
        """
        Initialize a service logger.
        
        Args:
            service: Name of the service (e.g., "backend", "api")
            component: Name of the component (e.g., "auth", "database", "router")
            log_level: Minimum log level to capture (default: INFO)
        """
        self.service = service
        self.component = component
        self.logger = logging.getLogger(f"{service}.{component}")
        self.logger.setLevel(getattr(logging, log_level.value))
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Add console handler with structured formatter
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(console_handler)
        
        # Prevent propagation to root logger
        self.logger.propagate = False
    
    def _get_caller_info(self) -> tuple[str, int]:
        """Get the file and line number of the caller"""
        frame = inspect.currentframe()
        if frame is None:
            return "unknown", 0
        
        # Go up the stack to find the actual caller (skip logger methods)
        caller_frame = frame.f_back.f_back if frame.f_back else None
        if caller_frame:
            filename = Path(caller_frame.f_code.co_filename).name
            lineno = caller_frame.f_lineno
            return filename, lineno
        return "unknown", 0
    
    def _log(
        self,
        level: LogLevel,
        message: str,
        operation_id: Optional[str] = None,
        **kwargs
    ):
        """Internal logging method"""
        extra = {
            'service': self.service,
            'component': self.component,
            'operation_id': operation_id,
        }
        
        if kwargs:
            extra['extra_data'] = kwargs
        
        log_func = getattr(self.logger, level.value.lower())
        log_func(message, extra=extra)
    
    def debug(
        self,
        message: str,
        operation_id: Optional[str] = None,
        **kwargs
    ):
        """Log a DEBUG level message"""
        self._log(LogLevel.DEBUG, message, operation_id, **kwargs)
    
    def info(
        self,
        message: str,
        operation_id: Optional[str] = None,
        **kwargs
    ):
        """Log an INFO level message"""
        self._log(LogLevel.INFO, message, operation_id, **kwargs)
    
    def warning(
        self,
        message: str,
        operation_id: Optional[str] = None,
        **kwargs
    ):
        """Log a WARNING level message"""
        self._log(LogLevel.WARNING, message, operation_id, **kwargs)
    
    def error(
        self,
        message: str,
        operation_id: Optional[str] = None,
        exc_info: bool = False,
        **kwargs
    ):
        """
        Log an ERROR level message
        
        Args:
            message: Error message
            operation_id: Operation/request ID
            exc_info: Include exception traceback if True
            **kwargs: Additional context data
        """
        extra = {
            'service': self.service,
            'component': self.component,
            'operation_id': operation_id,
        }
        
        if kwargs:
            extra['extra_data'] = kwargs
        
        self.logger.error(message, extra=extra, exc_info=exc_info)
    
    def critical(
        self,
        message: str,
        operation_id: Optional[str] = None,
        exc_info: bool = False,
        **kwargs
    ):
        """
        Log a CRITICAL level message
        
        Args:
            message: Critical error message
            operation_id: Operation/request ID
            exc_info: Include exception traceback if True
            **kwargs: Additional context data
        """
        extra = {
            'service': self.service,
            'component': self.component,
            'operation_id': operation_id,
        }
        
        if kwargs:
            extra['extra_data'] = kwargs
        
        self.logger.critical(message, extra=extra, exc_info=exc_info)
    
    def with_operation(self, operation_id: str) -> 'OperationLogger':
        """
        Create a logger bound to a specific operation ID.
        
        Usage:
            request_logger = logger.with_operation("req-123")
            request_logger.info("Processing request")
            request_logger.error("Request failed")
        """
        return OperationLogger(self, operation_id)


class OperationLogger:
    """Logger bound to a specific operation ID"""
    
    def __init__(self, service_logger: ServiceLogger, operation_id: str):
        self.service_logger = service_logger
        self.operation_id = operation_id
    
    def debug(self, message: str, **kwargs):
        """Log a DEBUG level message with operation ID"""
        self.service_logger.debug(message, operation_id=self.operation_id, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log an INFO level message with operation ID"""
        self.service_logger.info(message, operation_id=self.operation_id, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log a WARNING level message with operation ID"""
        self.service_logger.warning(message, operation_id=self.operation_id, **kwargs)
    
    def error(self, message: str, exc_info: bool = False, **kwargs):
        """Log an ERROR level message with operation ID"""
        self.service_logger.error(
            message,
            operation_id=self.operation_id,
            exc_info=exc_info,
            **kwargs
        )
    
    def critical(self, message: str, exc_info: bool = False, **kwargs):
        """Log a CRITICAL level message with operation ID"""
        self.service_logger.critical(
            message,
            operation_id=self.operation_id,
            exc_info=exc_info,
            **kwargs
        )


# Utility function to generate request IDs
def generate_request_id() -> str:
    """Generate a unique request ID"""
    import uuid
    return f"req-{uuid.uuid4().hex[:12]}"
