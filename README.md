# CasaBricks - Interactive Property Listing Platform

CasaBricks is a modern property discovery platform for Noida properties with AI-enhanced images and guided search functionality.

## Project Structure

This repository contains both frontend and backend:

```
├── frontend/           # React + Vite frontend application
├── app/               # FastAPI backend application
├── alembic/           # Database migrations
├── scripts/           # Utility scripts
├── docs/              # Project documentation
└── README_BACKEND.md  # Detailed backend documentation
```

## Features

### Frontend
- **React + Vite**: Modern, fast frontend with HMR
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first design approach
- **Interactive UI**: Guided search flow for property discovery

### Backend
- **Guided Search**: 3-question flow replaces traditional filter-heavy search
- **AI-Enhanced Images**: Automatic image enhancement via external AI service
- **Visual Data Widgets**: Property metrics, price comparison, and more
- **Lead Management**: Complete inquiry and lead generation system
- **Admin Panel**: Property and inquiry management with JWT authentication
- **Real-time Processing**: Async operations with SQLAlchemy and FastAPI
- **Caching**: Redis-based caching for optimal performance
- **Background Tasks**: Celery for image monitoring and analytics
- **Monitoring**: Prometheus metrics and structured logging

## Technology Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- ESLint

### Backend
- FastAPI 0.109+
- Python 3.11+
- PostgreSQL 15+ (via Supabase)
- SQLAlchemy 2.0+ (async)
- Redis 7+
- Celery 5.3+
- Prometheus

## Quick Start

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy environment file
cp .env.backend.example .env

# Edit .env with your configuration
nano .env

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Create admin user
uv run python scripts/create_admin.py

# Start the server
uv run uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

**API Documentation**: http://localhost:8000/docs

## Detailed Documentation

- **Backend Documentation**: See [README_BACKEND.md](README_BACKEND.md) for comprehensive backend setup, API endpoints, and development guide
- **SRS Document**: See [docs/srs.md](docs/srs.md) for software requirements specification

## Environment Variables

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT_MS=10000
```

### Backend (.env)
See `.env.backend.example` for complete configuration. Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`: Supabase configuration
- `REDIS_URL`: Redis connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `AI_SERVICE_API_URL`: External AI service endpoint

## API Endpoints

### Public Endpoints
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/search/guided` - Guided property search
- `GET /api/v1/properties/{id}` - Get property details
- `POST /api/v1/inquiries` - Submit property inquiry

### Admin Endpoints (Requires JWT)
- `POST /api/v1/admin/properties` - Create property
- `PUT /api/v1/admin/properties/{id}` - Update property
- `POST /api/v1/admin/properties/{id}/images` - Upload image
- `POST /api/v1/admin/images/{id}/enhance` - Trigger AI enhancement
- `GET /api/v1/admin/inquiries` - List inquiries

### Monitoring
- `GET /metrics` - Prometheus metrics

## Development

### Run Tests
```bash
# Backend tests
uv run pytest
uv run pytest --cov=app --cov-report=html
```

### Run Celery Worker
```bash
# Start Celery worker
uv run celery -A app.tasks.celery_app worker --loglevel=info

# Start Celery beat (scheduler)
uv run celery -A app.tasks.celery_app beat --loglevel=info

# Start Flower (monitoring UI)
uv run celery -A app.tasks.celery_app flower
```

## Architecture

The backend follows a clean layered architecture:

```
app/
├── api/          # API routes and endpoints
├── models/       # SQLAlchemy ORM models
├── schemas/      # Pydantic validation models
├── services/     # Business logic layer
├── repositories/ # Data access layer
├── infrastructure/ # External integrations (AI, Storage, Cache)
├── core/         # Core utilities (security, logging, metrics)
├── middleware/   # FastAPI middleware
└── tasks/        # Celery background tasks
```

## Security Features

- ✅ JWT authentication with 60-minute expiration
- ✅ Password hashing with bcrypt
- ✅ CORS configuration
- ✅ Rate limiting (5 inquiries/hour per IP)
- ✅ File upload validation
- ✅ Webhook HMAC signature verification
- ✅ SQL injection prevention (ORM)
- ✅ Input validation (Pydantic)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[Your License Here]

## Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Note**: This project is exclusively for Noida properties. All listings must be within Noida, India.
