# Middleware Documentation

This folder contains authentication and rate limiting middleware for the Buy Noida backend API.

## Overview

- **auth.py**: JWT-based authentication middleware
- **rateLimiting.py**: IP-based rate limiting middleware

## Authentication Middleware

### Features

- **JWT Token Verification**: Validates JWT tokens in the Authorization header
- **User Context Injection**: Adds user information to request state
- **Role-Based Access Control**: Support for role-based permissions
- **Configurable Excluded Paths**: Skip authentication for specific endpoints

### Setup

1. Set the JWT secret key (use environment variable in production):
```bash
export JWT_SECRET_KEY="your-secure-secret-key"
```

2. Add middleware to your FastAPI app:
```python
from middleware.auth import AuthMiddleware

app.add_middleware(
    AuthMiddleware,
    excluded_paths=["/", "/docs", "/redoc", "/openapi.json", "/auth/login"]
)
```

### Usage

#### Creating Tokens

```python
from middleware.auth import create_access_token
from datetime import timedelta

# Create a token with default expiration (30 minutes)
token = create_access_token(
    data={
        "user_id": 123,
        "email": "user@example.com",
        "role": "user"
    }
)

# Create a token with custom expiration
token = create_access_token(
    data={"user_id": 123, "email": "user@example.com"},
    expires_delta=timedelta(hours=24)
)
```

#### Protected Routes

```python
from fastapi import Request
from middleware.auth import get_current_user

@app.get("/profile")
async def get_profile(request: Request):
    user = get_current_user(request)
    return {
        "user_id": user["user_id"],
        "email": user["email"],
        "role": user["role"]
    }
```

#### Role-Based Access

```python
from middleware.auth import require_role

@app.get("/admin")
async def admin_only(request: Request):
    user = require_role(["admin"])(request)
    return {"message": "Admin access granted", "user": user}

@app.get("/moderator")
async def moderator_or_admin(request: Request):
    user = require_role(["admin", "moderator"])(request)
    return {"message": "Moderator access granted"}
```

#### Client-Side Usage

Send the JWT token in the Authorization header:

```javascript
fetch('http://api.example.com/protected', {
    headers: {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
    }
})
```

### Token Payload

The JWT token includes:
- `user_id`: User's unique identifier
- `email`: User's email address
- `role`: User's role (e.g., "user", "admin", "moderator")
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp

### Error Responses

- **401 Unauthorized**: Missing, invalid, or expired token
- **403 Forbidden**: Insufficient permissions (wrong role)
- **500 Internal Server Error**: Authentication system error

## Rate Limiting Middleware

### Features

- **IP-Based Rate Limiting**: Tracks requests per IP address
- **Dual Window Limits**: Per-minute and per-hour limits
- **Automatic Cleanup**: Removes old request history to prevent memory leaks
- **Rate Limit Headers**: Includes remaining requests in response headers
- **Proxy Support**: Handles X-Forwarded-For and X-Real-IP headers

### Setup

Add middleware to your FastAPI app:

```python
from middleware.rateLimiting import RateLimiter

app.add_middleware(
    RateLimiter,
    requests_per_minute=60,    # 60 requests per minute
    requests_per_hour=1000,     # 1000 requests per hour
    cleanup_interval=300,       # Cleanup every 5 minutes
    excluded_paths=["/", "/health", "/docs"]
)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `requests_per_minute` | 60 | Maximum requests per minute per IP |
| `requests_per_hour` | 1000 | Maximum requests per hour per IP |
| `cleanup_interval` | 300 | Cleanup interval in seconds |
| `excluded_paths` | ["/", "/docs", "/redoc", "/openapi.json"] | Paths to exclude from rate limiting |

### Response Headers

Every response includes rate limit information:

```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Remaining-Minute: 45
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 823
```

### Rate Limit Exceeded Response

When rate limit is exceeded, the API returns:

```json
{
    "detail": "Rate limit exceeded: 60 requests per minute"
}
```

Headers:
```
Status: 429 Too Many Requests
Retry-After: 42
X-RateLimit-Limit: 60
X-RateLimit-Window: minute
```

### Endpoint-Specific Rate Limiting

For different limits on specific endpoints:

```python
from middleware.rateLimiting import RateLimitByEndpoint

# Apply to specific route
@app.get("/api/expensive-operation")
@RateLimitByEndpoint(requests_per_minute=5, requests_per_hour=50)
async def expensive_operation():
    return {"status": "completed"}
```

### Testing Rate Limits

Test with curl:

```bash
# Send multiple requests to test rate limiting
for i in {1..100}; do
    curl -i http://localhost:8000/api/endpoint
done
```

Check headers to see remaining requests:

```bash
curl -i http://localhost:8000/api/endpoint | grep X-RateLimit
```

## Best Practices

### Authentication

1. **Use Environment Variables**: Never hardcode JWT secrets
   ```bash
   export JWT_SECRET_KEY="$(openssl rand -base64 32)"
   ```

2. **Secure Token Storage**: Store tokens securely on client-side (httpOnly cookies or secure storage)

3. **Token Expiration**: Use short-lived tokens and implement refresh tokens for better security

4. **HTTPS Only**: Always use HTTPS in production to prevent token interception

5. **Validate Input**: Validate all user input before creating tokens

### Rate Limiting

1. **Adjust Limits**: Set appropriate limits based on your API's capacity and expected usage

2. **Monitor Logs**: Watch for rate limit violations to identify abuse or adjust limits

3. **Behind Proxy**: Ensure `X-Forwarded-For` header is properly set by your reverse proxy

4. **Different Tiers**: Consider different rate limits for authenticated vs. unauthenticated users

5. **Graceful Degradation**: Handle rate limit errors gracefully on the client side

## Combining Both Middleware

Apply both middleware to your app (order matters):

```python
# Rate limiting first (applies to all requests)
app.add_middleware(
    RateLimiter,
    requests_per_minute=60,
    requests_per_hour=1000,
    excluded_paths=["/", "/health"]
)

# Authentication second (only for protected endpoints)
app.add_middleware(
    AuthMiddleware,
    excluded_paths=["/", "/health", "/auth/login", "/auth/register"]
)
```

## Production Considerations

1. **JWT Secret**: Use a strong, random secret key stored in environment variables
2. **Rate Limit Storage**: For distributed systems, consider using Redis instead of in-memory storage
3. **Token Refresh**: Implement refresh token mechanism for long-lived sessions
4. **Logging**: Add comprehensive logging for security audits
5. **Monitoring**: Track authentication failures and rate limit violations
6. **IP Whitelisting**: Consider whitelisting trusted IPs from rate limiting
7. **API Keys**: For service-to-service communication, consider API keys alongside JWT

## Examples

See [server.py](../server.py) for working examples of:
- Login endpoint that creates tokens
- Protected routes requiring authentication
- Rate-limited public endpoints

## Troubleshooting

### "Missing or invalid authorization header"
- Ensure the token is sent in the `Authorization: Bearer <token>` header
- Check that the endpoint is not in the excluded paths

### "Token has expired"
- Token has exceeded its expiration time
- Client needs to obtain a new token

### "Rate limit exceeded"
- Client has sent too many requests
- Check the `Retry-After` header for when to retry
- Verify the IP address is correct (check proxy configuration)

### Rate limits not working
- Ensure middleware is added before routes are defined
- Check that cleanup task is running
- Verify proxy headers are being passed correctly
