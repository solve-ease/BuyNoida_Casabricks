# Buy Noida Backend

FastAPI-based backend service for the Buy Noida real estate platform by Casabrick.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **PostgreSQL Database**: Async database operations with asyncpg
- **JWT Authentication**: Secure token-based authentication
- **Rate Limiting**: IP-based request rate limiting
- **Connection Pooling**: Efficient database connection management
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Project Structure

```
backend/
├── server.py              # Main FastAPI application
├── pyproject.toml         # Python dependencies
├── middleware/            # Authentication and rate limiting
│   ├── auth.py           # JWT authentication middleware
│   ├── rateLimiting.py   # Rate limiting middleware
│   ├── examples.py       # Usage examples
│   └── README.md         # Middleware documentation
├── services/             # Business logic services
│   └── database/         # Database services
│       ├── connection.py # Database connection management
│       └── queries/      # SQL queries
└── routers/              # API route handlers
```

## Getting Started

### Prerequisites

- Python 3.12 or higher
- PostgreSQL database

### Installation

1. Install dependencies:
```bash
cd backend
pip install -e .
```

Or using uv:
```bash
uv pip install -e .
```

2. Set up environment variables:
```bash
# PostgreSQL connection
export PostgressDSN="postgresql://user:password@localhost:5432/dbname"

# JWT secret key (generate a secure random key)
export JWT_SECRET_KEY="your-secure-secret-key-here"
```

Generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Running the Server

```bash
cd backend
fastapi dev server.py
```

The server will start on `http://localhost:8000`

- API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### Public Endpoints

- `GET /` - Health check
- `POST /auth/login` - User login (returns JWT token)
- `POST /auth/register` - User registration

### Protected Endpoints

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

- `GET /protected` - Example protected route
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile

### Admin Endpoints

Admin endpoints require authentication with admin role:

- `GET /admin/users` - List all users
- `DELETE /admin/users/{user_id}` - Delete user

## Authentication

The backend uses JWT (JSON Web Tokens) for authentication.

### Getting a Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

```bash
curl -X GET "http://localhost:8000/protected" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

See [middleware/README.md](./middleware/README.md) for detailed authentication documentation.

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Per Minute Limit**: 60 requests per minute per IP
- **Per Hour Limit**: 1000 requests per hour per IP

Rate limit information is included in response headers:
```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Remaining-Minute: 45
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 823
```

When rate limit is exceeded, the API returns HTTP 429 with a `Retry-After` header.

See [middleware/README.md](./middleware/README.md) for detailed rate limiting documentation.

## Database

### Connection

The application uses asyncpg for async PostgreSQL operations. Connection pooling is managed automatically.

Database configuration via environment variable:
```bash
export PostgressDSN="postgresql://user:password@host:port/database"
```

### Getting a Connection

```python
from services.database.connection import get_conn

async with get_conn(app) as conn:
    result = await conn.fetch("SELECT * FROM users")
```

## Development

### Project Dependencies

- **fastapi[standard]**: Web framework with all standard extras
- **asyncpg**: Async PostgreSQL driver
- **pyjwt**: JWT token handling

### Adding Dependencies

Edit `pyproject.toml` and run:
```bash
pip install -e .
```

### Code Structure

1. **server.py**: Main application setup, middleware configuration
2. **middleware/**: Authentication and rate limiting logic
3. **routers/**: API endpoint handlers (organized by resource)
4. **services/**: Business logic and data access
5. **services/database/**: Database connection and queries

## Middleware

### Enable Authentication

Uncomment in `server.py`:
```python
app.add_middleware(
    AuthMiddleware,
    excluded_paths=["/", "/docs", "/health", "/auth/login", "/auth/register"]
)
```

### Configure Rate Limits

Adjust in `server.py`:
```python
app.add_middleware(
    RateLimiter,
    requests_per_minute=100,  # Increase limit
    requests_per_hour=5000,   # Increase limit
)
```

## Security Best Practices

1. **Never commit secrets**: Use environment variables for sensitive data
2. **Use HTTPS**: Always use HTTPS in production
3. **Rotate keys**: Regularly rotate JWT secret keys
4. **Strong passwords**: Enforce strong password policies
5. **Rate limiting**: Keep rate limits reasonable for your use case
6. **Input validation**: Validate all user input
7. **SQL injection**: Use parameterized queries (asyncpg does this automatically)

## Production Deployment

### Environment Variables

```bash
# Required
export PostgressDSN="postgresql://..."
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"

# Optional
export ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Running with Uvicorn

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY . .

RUN pip install -e .

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### CORS Configuration

For production, update CORS settings in `server.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
psql $PostgressDSN -c "SELECT 1"
```

### Authentication Not Working

1. Check JWT_SECRET_KEY is set
2. Verify token in Authorization header: `Bearer <token>`
3. Check token hasn't expired (default: 30 minutes)

### Rate Limiting Too Strict

1. Check current limits in server.py
2. Adjust `requests_per_minute` and `requests_per_hour`
3. Add your endpoint to `excluded_paths` if needed

## Documentation

- [Middleware Documentation](./middleware/README.md) - Detailed auth and rate limiting docs
- [Usage Examples](./middleware/examples.py) - Code examples and patterns
- [FastAPI Docs](https://fastapi.tiangolo.com/) - FastAPI framework documentation

## License

[Add your license here]

## Support

[Add support contact information]
