"""
API v1 router - aggregates all v1 endpoints
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, search, properties, inquiries, admin, webhooks

# Create main v1 router
router = APIRouter(prefix="/v1")

# Include all endpoint routers
router.include_router(auth.router)
router.include_router(search.router)
router.include_router(properties.router)
router.include_router(inquiries.router)
router.include_router(admin.router)
router.include_router(webhooks.router)
