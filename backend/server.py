from fastapi import FastAPI, Request
from services.logger import ServiceLogger
from fastapi.middleware.cors import CORSMiddleware
from services.database.connection import create_conn_pool
from contextlib import asynccontextmanager
from middleware.auth import AuthMiddleware, create_access_token, get_current_user
from middleware.rateLimiting import RateLimiter
from middleware.logging import LoggingMiddleware
import os

ENVIRONMENT = os.getenv("ENVIRONMENT","DEV")

logger = ServiceLogger(service="backend", component="server")

# Server lifespan to gracefully handle server shutdown and prevent leaks
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing server lifecycle management)", operation_id="startup")

    async with create_conn_pool() as connection_pool:
        app.state.connection_pool = connection_pool
        yield
        
        logger.info("Ending the server lifecycle", operation_id="shutdown")


app = FastAPI(
    title="Buy Noida By Casabrick Backend",
    lifespan=lifespan
)


# Add Logging Middleware (tracks all requests with unique IDs)
app.add_middleware(LoggingMiddleware, service="backend")


if ENVIRONMENT == "PROD":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["buynoida.com","www.buynoida.com"],
        allow_headers=["*"],
        allow_methods=["GET", "POST"]
    )
    
    app.add_middleware(
        RateLimiter,
        requests_per_minute=60,
        requests_per_hour=1000,
        excluded_paths=["/", "/docs", "/redoc", "/openapi.json", "/health"]
    )
    
    app.add_middleware(
        AuthMiddleware,
        excluded_paths=["/", "/docs", "/redoc", "/openapi.json", "/health", "/auth/login", "/auth/register"]
    )


else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
        allow_methods=["*"]
    )


@app.get("/")
async def health():
    return {"status": "ok"}

# Example authentication endpoints
@app.post("/auth/login")
async def login(email: str, password: str):
    """
    Example login endpoint. Replace with actual authentication logic.
    """
    # TODO: Verify credentials against database
    # For now, this is just an example
    
    # Create JWT token
    token = create_access_token(
        data={
            "user_id": 1,
            "email": email,
            "role": "user"
        }
    )
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Example protected endpoint
@app.get("/protected")
async def protected_route(request: Request):
    """
    Example protected endpoint that requires authentication.
    Uncomment the AuthMiddleware above to enable protection.
    """
    user = get_current_user(request)
    return {
        "message": "This is a protected route",
        "user": user
    }