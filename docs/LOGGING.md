# Logging System Documentation

## Overview

This logging system provides structured, context-aware logging throughout the BuyNoida backend. All logs are tagged with service, component, operation ID, file location, timestamp, and severity level.

## Features

- ✅ **Service & Component Tagging**: Every log is tagged with its service and component
- ✅ **Operation ID Tracking**: Track logs across the entire request lifecycle using request IDs
- ✅ **File Location**: Automatically captures file name and line number
- ✅ **Severity Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- ✅ **Timestamps**: All logs include ISO 8601 formatted timestamps with timezone
- ✅ **Structured JSON Output**: Easy to parse and analyze
- ✅ **Exception Tracking**: Full exception traces with context

## Log Format

Each log entry is a JSON object with the following structure:

```json
{
  "timestamp": "2026-02-10T14:30:45.123456+00:00",
  "level": "INFO",
  "service": "backend",
  "component": "auth",
  "operation_id": "req-a1b2c3d4e5f6",
  "file": "auth.py:42",
  "function": "login",
  "message": "User logged in successfully",
  "data": {
    "user_id": 123,
    "email": "user@example.com"
  }
}
```

## Usage

### 1. Basic Logger Usage

```python
from services.logger import ServiceLogger

# Create a logger for your component
logger = ServiceLogger(service="backend", component="auth")

# Log messages
logger.info("User logged in successfully", operation_id="req-123", user_id=42)
logger.warning("Password attempt failed", operation_id="req-124", attempts=3)
logger.error("Database connection failed", operation_id="req-125", exc_info=True)
```

### 2. Using in FastAPI Routes

The logging middleware automatically adds a logger to `request.state` for each incoming request:

```python
from fastapi import APIRouter, Request
from services.logger import ServiceLogger

router = APIRouter()

# Create base logger for the router component
logger = ServiceLogger(service="backend", component="properties")

@router.get("/properties/{property_id}")
async def get_property(property_id: int, request: Request):
    # Use the request logger (automatically has request_id)
    request.state.logger.info(
        "Fetching property details",
        property_id=property_id
    )
    
    try:
        # Your business logic here
        property_data = await fetch_property(property_id)
        
        request.state.logger.info(
            "Property fetched successfully",
            property_id=property_id
        )
        
        return property_data
        
    except Exception as e:
        request.state.logger.error(
            "Failed to fetch property",
            exc_info=True,
            property_id=property_id,
            error=str(e)
        )
        raise
```

### 3. Operation-Specific Logger

For operations that span multiple function calls, create an operation-bound logger:

```python
from services.logger import ServiceLogger

logger = ServiceLogger(service="backend", component="payment")

def process_payment(transaction_id: str):
    # Create logger bound to this operation
    op_logger = logger.with_operation(transaction_id)
    
    op_logger.info("Starting payment processing")
    
    # All subsequent logs will include the transaction_id
    op_logger.info("Validating payment details")
    op_logger.info("Charging payment method")
    op_logger.info("Payment processed successfully", amount=100.00)
```

### 4. Logger with Different Levels

```python
from services.logger import ServiceLogger, LogLevel

# Create logger with DEBUG level
logger = ServiceLogger(
    service="backend",
    component="cache",
    log_level=LogLevel.DEBUG
)

logger.debug("Cache key generated", key="user:123")
logger.info("Cache hit", key="user:123")
logger.warning("Cache miss", key="user:456")
logger.error("Cache connection failed", exc_info=True)
logger.critical("Cache system down", exc_info=True)
```

### 5. Logging in Database Services

```python
from services.logger import ServiceLogger

class PropertyService:
    def __init__(self):
        self.logger = ServiceLogger(service="backend", component="db:properties")
    
    async def create_property(self, data: dict, operation_id: str):
        op_logger = self.logger.with_operation(operation_id)
        
        op_logger.info("Creating new property", data_keys=list(data.keys()))
        
        try:
            # Database operation
            result = await self.db.insert(data)
            
            op_logger.info(
                "Property created successfully",
                property_id=result.id
            )
            
            return result
            
        except Exception as e:
            op_logger.error(
                "Failed to create property",
                exc_info=True,
                error=str(e)
            )
            raise
```

## Log Levels

Choose the appropriate log level based on severity:

- **DEBUG**: Detailed diagnostic information (e.g., cache keys, intermediate values)
- **INFO**: General informational messages (e.g., "Request processed", "User logged in")
- **WARNING**: Warning messages indicating potential issues (e.g., "Retry attempt 3/5", "Deprecated API used")
- **ERROR**: Error messages for recoverable errors (e.g., "Database query failed", "External API timeout")
- **CRITICAL**: Critical errors requiring immediate attention (e.g., "Database connection pool exhausted", "System out of memory")

## Best Practices

1. **Always Include Operation ID**: Use `request.state.request_id` or generate a unique ID for batch operations
2. **Add Context Data**: Include relevant data as keyword arguments (e.g., `user_id`, `property_id`)
3. **Use Descriptive Messages**: Write clear, actionable log messages
4. **Log Exceptions**: Always use `exc_info=True` when logging exceptions
5. **Component Naming**: Use descriptive component names:
   - `db:users`, `db:properties` for database services
   - `auth`, `payment` for business logic
   - `middleware`, `router` for infrastructure

## Middleware Configuration

The `LoggingMiddleware` is automatically applied to all requests and:
- Generates unique request IDs
- Logs incoming requests with method, path, and client IP
- Logs responses with status code and duration
- Adds `X-Request-ID` header to all responses
- Makes logger available in `request.state.logger`

## Example Log Output

```json
{
  "timestamp": "2026-02-10T14:30:45.123456+00:00",
  "level": "INFO",
  "service": "backend",
  "component": "middleware",
  "operation_id": "req-a1b2c3d4e5f6",
  "file": "logging.py:56",
  "function": "dispatch",
  "message": "Incoming request: GET /api/properties/123",
  "data": {
    "method": "GET",
    "path": "/api/properties/123",
    "query_params": "limit=10",
    "client_ip": "192.168.1.100"
  }
}
```

```json
{
  "timestamp": "2026-02-10T14:30:45.234567+00:00",
  "level": "INFO",
  "service": "backend",
  "component": "properties",
  "operation_id": "req-a1b2c3d4e5f6",
  "file": "properties.py:28",
  "function": "get_property",
  "message": "Fetching property details",
  "data": {
    "property_id": 123
  }
}
```

```json
{
  "timestamp": "2026-02-10T14:30:45.345678+00:00",
  "level": "INFO",
  "service": "backend",
  "component": "middleware",
  "operation_id": "req-a1b2c3d4e5f6",
  "file": "logging.py:72",
  "function": "dispatch",
  "message": "Request completed: GET /api/properties/123",
  "data": {
    "status_code": 200,
    "duration_ms": 112.34
  }
}
```

## Request ID Generation

Request IDs are automatically generated in the format: `req-{12-char-uuid}`

Example: `req-a1b2c3d4e5f6`

You can also generate custom operation IDs:

```python
from services.logger import generate_request_id

batch_id = generate_request_id()  # e.g., "req-x7y8z9a0b1c2"
```

## Troubleshooting

### Logs not appearing?

Check that your logger's log level is set appropriately:

```python
logger = ServiceLogger(
    service="backend",
    component="mycomponent",
    log_level=LogLevel.DEBUG  # Shows all logs including DEBUG
)
```

### Want to filter logs?

Since logs are JSON, you can easily filter them:

```bash
# Filter by service
cat logs.json | grep '"service": "backend"'

# Filter by operation ID
cat logs.json | grep '"operation_id": "req-123"'

# Filter by error level
cat logs.json | grep '"level": "ERROR"'
```

## Advanced: Log Aggregation

For production, consider piping logs to a log aggregation service:

- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Grafana Loki**
- **CloudWatch Logs**
- **Datadog**

The structured JSON format makes it easy to ingest into any log management system.
