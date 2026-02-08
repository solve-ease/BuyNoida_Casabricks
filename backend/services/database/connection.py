import asyncpg
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os

logger = logging.getLogger(__name__)

dsn = os.getenv("PostgressDSN" , "postgresql://filedb_user:filedb_pass123@localhost:5432/filedb")

@asynccontextmanager
async def create_conn_pool() :
    logger.info("Creating a File DB Connection Pool")
    
    try:
        pool = await asyncpg.create_pool(
            dsn=dsn, 
        )
        yield pool
    
    finally:
        if pool is not None:
            logger.info("Releasing File DB connection pool")
            await pool.close()

@asynccontextmanager
async def get_conn(app: FastAPI) :
    logger.info("Acquiring a Connection from File DB Connection Pool")
    conn = None

    try:
        conn = await app.state.connection_pool.acquire()
        yield conn
        
    finally:
        if conn is not None:
            logger.info("Releasing File DB Connection to the pool")
            await app.state.connection_pool.release(conn)