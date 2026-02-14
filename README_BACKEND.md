# CasaBricks Backend API

A production-ready FastAPI backend for CasaBricks - an interactive property discovery platform for Noida properties with AI-enhanced images and guided search.

## Features

- **Guided Search**: Simple 3-question flow replaces traditional filter-heavy search
- **AI-Enhanced Images**: Automatic image enhancement via external AI service with webhook integration
- **Visual Data Widgets**: Property data presented through compass, price charts, and metrics
- **Lead Management**: Complete inquiry and lead generation system
- **Admin Panel**: Full property and inquiry management with authentication
- **Async Operations**: Built on FastAPI with SQLAlchemy async for high performance
- **Caching**: Redis-based caching for optimized performance
- **Background Tasks**: Celery for image monitoring and analytics
- **Monitoring**: Prometheus metrics and structured logging
- **Security**: JWT authentication, rate limiting, webhook signature verification

## Technology Stack

- **Framework**: FastAPI 0.109+
- **Python**: 3.11+
- **Database**: PostgreSQL 15+ (via Supabase)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Cache & Queue**: Redis 7+
- **Background Tasks**: Celery 5.3+
- **Package Manager**: uv (NOT Poetry)
- **Authentication**: JWT (python-jose)
- **Storage**: Supabase Storage
- **Logging**: structlog
- **Metrics**: Prometheus

## Project Structure

```
app/
├── api/                    # API routes and endpoints
│   ├── dependencies.py     # Shared dependencies (auth, db session)
│   └── v1/
│       ├── router.py       # Main router aggregator
│       └── endpoints/      # API endpoint modules
├── models/                 # SQLAlchemy ORM models
├── schemas/                # Pydantic validation models
├── services/               # Business logic layer
├── repositories/           # Data access layer
├── infrastructure/         # External integrations
│   ├── ai/                # AI service client
│   ├── storage/           # Supabase storage
│   └── cache/             # Redis client
├── core/                   # Core utilities
│   ├── security.py        # JWT & password hashing
│   ├── logging.py         # Structured logging
│   ├── metrics.py         # Prometheus metrics
│   └── exceptions.py      # Custom exceptions
├── middleware/             # FastAPI middleware
├── tasks/                  # Celery background tasks
├── config/                 # Configuration
└── main.py                # FastAPI app entry point
```

## Installation

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15+ (or Supabase account)
- Redis 7+
- uv package manager

### Setup

1. **Install uv package manager:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone the repository:**

```bash
git clone <repository-url>
cd BuyNoida_Casabricks
```

3. **Create environment file:**

```bash
cp .env.backend.example .env
```

4. **Edit `.env` with your configuration:**

```bash
# Application
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here-min-32-chars

# Database (Supabase)
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/casabricks
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Service
AI_SERVICE_API_URL=https://your-ai-service.com/api/v1/enhance
AI_SERVICE_API_KEY=your-ai-api-key
AI_SERVICE_WEBHOOK_SECRET=shared-secret-min-32-chars

# Security
JWT_SECRET_KEY=your-jwt-secret-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

5. **Install dependencies:**

```bash
uv sync
```

6. **Run database migrations:**

```bash
# Generate initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

7. **Create admin user (via Python shell):**

```python
import asyncio
from app.config.database import async_session_maker
from app.models.user import User, UserRole
from app.core.security import get_password_hash

async def create_admin():
    async with async_session_maker() as db:
        admin = User(
            email="admin@casabricks.com",
            hashed_password=get_password_hash("your-secure-password"),
            full_name="Admin User",
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        db.add(admin)
        await db.commit()
        print(f"Admin user created: {admin.email}")

asyncio.run(create_admin())
```

## Running the Application

### Development Server

```bash
# Run with uvicorn (auto-reload enabled)
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
# Run with uvicorn (multiple workers)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Celery Worker

```bash
# Start Celery worker
uv run celery -A app.tasks.celery_app worker --loglevel=info

# Start Celery beat scheduler (for periodic tasks)
uv run celery -A app.tasks.celery_app beat --loglevel=info

# Start Flower (Celery monitoring)
uv run celery -A app.tasks.celery_app flower
```

## API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Public Endpoints

- `GET /` - API health check
- `GET /health` - Detailed health status
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/search/guided` - Guided property search
- `GET /api/v1/properties/{id}` - Get property details
- `POST /api/v1/inquiries` - Submit property inquiry

### Admin Endpoints (Requires JWT)

- `POST /api/v1/admin/properties` - Create property
- `PUT /api/v1/admin/properties/{id}` - Update property
- `DELETE /api/v1/admin/properties/{id}` - Delete property
- `PATCH /api/v1/admin/properties/{id}/status` - Toggle property status
- `POST /api/v1/admin/properties/{id}/images` - Upload image
- `DELETE /api/v1/admin/images/{id}` - Delete image
- `POST /api/v1/admin/images/{id}/enhance` - Trigger AI enhancement
- `GET /api/v1/admin/inquiries` - List inquiries
- `PATCH /api/v1/admin/inquiries/{id}/status` - Update inquiry status
- `POST /api/v1/admin/inquiries/{id}/notes` - Add notes to inquiry

### Webhook Endpoints

- `POST /api/v1/webhooks/ai-enhancement` - AI service webhook callback

### Monitoring

- `GET /metrics` - Prometheus metrics endpoint

## Authentication

Admin endpoints require JWT authentication. To authenticate:

1. **Login to get token:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@casabricks.com", "password": "your-password"}'
```

2. **Use token in requests:**

```bash
curl -X GET "http://localhost:8000/api/v1/admin/properties" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest app/tests/test_services/test_property_service.py
```

## Rate Limiting

- **Inquiries**: Maximum 5 inquiries per hour per IP address
- Exceeded requests return `429 Too Many Requests`

## Image Enhancement Flow

1. Admin uploads image → Stored in Supabase, status: `pending`
2. Admin clicks "Enhance" → Request sent to AI service, status: `processing`
3. AI service processes (up to 24 hours)
4. AI service calls webhook with result
5. Backend downloads enhanced image, uploads to Supabase, status: `completed`
6. If processing takes >48 hours → Celery marks as `timeout`

## Background Tasks

Celery runs three periodic tasks:

1. **Check Stuck Images** (Every 15 minutes)
   - Finds images processing >48 hours
   - Marks as timeout

2. **Aggregate Analytics** (Every hour)
   - Updates property counts by type
   - Updates image enhancement queue length

3. **Warm Cache** (Daily at midnight)
   - Pre-populates cache for popular searches

## Monitoring & Logging

### Structured Logging

All logs are structured JSON (production) or pretty-printed (development):

```python
logger.info("property_created", property_id=property.id, property_type=property.property_type)
```

### Prometheus Metrics

Access metrics at `/metrics`:

- API request counts and duration
- Active properties by type
- Property views and inquiries
- Image enhancement queue length
- Image enhancement duration

## Security Features

- ✅ JWT authentication with 60-minute expiration
- ✅ Password hashing with bcrypt
- ✅ CORS configuration
- ✅ Rate limiting on inquiry endpoint
- ✅ File upload validation (type, size)
- ✅ Webhook HMAC signature verification
- ✅ SQL injection prevention (ORM)
- ✅ Input validation (Pydantic)

## Database Schema

Key tables:
- `users` - Admin users
- `properties` - Property listings
- `property_images` - Property images with enhancement status
- `inquiries` - Lead inquiries
- `analytics_events` - Event tracking

## Environment Variables

See `.env.backend.example` for complete list of configuration options.

## Troubleshooting

### Database Connection Issues

```bash
# Test database connection
uv run python -c "from app.config.database import engine; import asyncio; asyncio.run(engine.connect())"
```

### Redis Connection Issues

```bash
# Test Redis connection
redis-cli ping
```

### Migration Issues

```bash
# Reset migrations (WARNING: This will drop all data)
uv run alembic downgrade base
uv run alembic upgrade head
```

## Contributing

1. Follow the existing code structure and patterns
2. Write tests for new features
3. Update documentation
4. Run linters before committing

## License

[Your License Here]

## Support

For issues and questions, please contact [your-contact]
