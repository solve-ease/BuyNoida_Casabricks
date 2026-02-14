"""
Main FastAPI application entry point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from app.config.settings import settings
from app.config.database import init_db, close_db
from app.core.logging import configure_logging, get_logger
from app.infrastructure.cache.redis_client import redis_client
from app.infrastructure.storage.supabase_storage import supabase_storage
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.api.v1.router import router as v1_router

# Configure logging
configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info("application_starting", env=settings.APP_ENV)
    
    # Initialize database
    try:
        await init_db()
        logger.info("database_initialized")
    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))
    
    # Connect to Redis
    try:
        await redis_client.connect()
        logger.info("redis_connected")
    except Exception as e:
        logger.error("redis_connection_failed", error=str(e))
    
    # Initialize Supabase storage
    try:
        supabase_storage.connect()
        logger.info("supabase_storage_initialized")
    except Exception as e:
        logger.error("supabase_storage_initialization_failed", error=str(e))
    
    logger.info("application_started")
    
    yield
    
    # Shutdown
    logger.info("application_shutting_down")
    
    # Close connections
    await redis_client.disconnect()
    await close_db()
    
    logger.info("application_stopped")


# Create FastAPI app
app = FastAPI(
    title="CasaBricks Backend API",
    description="""
    CasaBricks Property Listing API - An interactive property discovery platform for Noida properties
    
    ## Features
    
    * **Guided Search**: 3-question flow to find properties
    * **AI-Enhanced Images**: Automatic image enhancement via external AI service
    * **Visual Data Widgets**: Compass, price charts, and amenity maps
    * **Lead Management**: Property inquiry and lead generation
    * **Admin Panel**: Complete property and inquiry management
    
    ## Authentication
    
    Admin endpoints require JWT authentication. Use `/api/v1/auth/login` to get an access token.
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(LoggingMiddleware)

# Include API routers
app.include_router(v1_router, prefix="/api")

# Add Prometheus metrics endpoint
if settings.ENABLE_METRICS:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    
    # Instrument the app with Prometheus
    Instrumentator().instrument(app).expose(app, endpoint="/metrics/fastapi")


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "name": "CasaBricks Backend API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.APP_ENV
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected" if redis_client.redis else "disconnected"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
