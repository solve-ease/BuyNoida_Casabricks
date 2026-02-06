from fastapi import FastAPI
import logging
from fastapi.middleware.cors import CORSMiddleware
from .services.database.connection import create_conn_pool
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server lifespan to gracefully handle server shutdown and prevent leaks
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing server lifecycle management)")

    async with create_conn_pool() as connection_pool:
        app.state.connection_pool = connection_pool
        yield
        
        logger.info("Ending the server lifecycle")


app = FastAPI(lifespan=lifespan)

# Temporary CORS For development 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
async def health():
    return {"status": "ok"}