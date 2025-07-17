"""
SOP Processing Service - Unified Entry Point
Combines functionality from main.py, main_enhanced.py, and main_simple.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Import configuration
from config.settings import settings
from config.database import create_tables
from models.database import init_sample_data

# Import route modules
from api.routes.health import router as health_router
from api.routes.sop import router as sop_router
from api.routes.events import router as events_router
from api.routes.threats import router as threats_router

# Import utilities
from utils.logging import setup_logging

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting SOP Processing Service...")
    
    try:
        # Create database tables
        create_tables()
        logger.info("Database tables created successfully")
        
        # Initialize sample employee data
        init_sample_data()
        logger.info("Sample employee data initialized")
        
        logger.info("Service started successfully")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down SOP Processing Service...")

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(sop_router, prefix="/api/v1", tags=["sop"])
app.include_router(events_router, prefix="/api/v1", tags=["events"])
app.include_router(threats_router, prefix="/api/v1", tags=["threats"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "SOP Processing Service",
        "version": settings.API_VERSION,
        "status": "running",
        "features": {
            "sop_processing": True,
            "event_processing": True,
            "threat_correlation": settings.ENABLE_THREAT_CORRELATION,
            "semantic_matching": settings.ENABLE_SEMANTIC_MATCHING,
            "crewai_agents": settings.ENABLE_CREWAI
        },
        "endpoints": {
            "health": "/api/v1/health",
            "sops": "/api/v1/sops",
            "events": "/api/v1/events",
            "threats": "/api/v1/threats"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL.lower()
    )