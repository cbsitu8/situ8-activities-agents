from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from agents.triage_agent import run_triage_analysis, batch_analyze_events
from models.event_models import CVThreatEvent, AccessControlEvent, TriageAnalysis
from simulation.simulator import router as simulation_router, initialize_data_loader
from typing import List, Dict, Any
import json
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('server.log')
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Security Triage Agent API",
    description="CrewAI-powered security event analysis and triage system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include simulation router
app.include_router(simulation_router)

# Initialize data loader on startup
@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting application startup...")
        cv_csv_path = "/Users/celinebroomhead/Downloads/MockData_ComputerVision - Sheet2.csv"
        access_csv_path = "/Users/celinebroomhead/Downloads/MockData_AccessControl - Sheet4.csv"
        
        logger.info(f"Initializing data loader with CV path: {cv_csv_path}")
        logger.info(f"Initializing data loader with Access path: {access_csv_path}")
        
        initialize_data_loader(cv_csv_path, access_csv_path)
        logger.info("Data loader initialized successfully")
        
        # Verify static files exist
        import os
        static_files = ['static/index.html', 'static/activities.html']
        for file_path in static_files:
            if os.path.exists(file_path):
                logger.info(f"Static file found: {file_path}")
            else:
                logger.warning(f"Static file missing: {file_path}")
                
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Security Triage Agent"
    }

# CV Threat Analysis Endpoint
@app.post("/analyze/cv-threat", response_model=Dict[str, Any])
async def analyze_cv_threat(event: CVThreatEvent):
    """Analyze computer vision threat detection event."""
    try:
        logger.info(f"Analyzing CV threat event: {event.record_id}")
        
        # Convert event to dict for analysis
        event_dict = event.dict()
        
        # Run triage analysis
        result = run_triage_analysis(event_dict, "CV_Threat_Detection")
        
        logger.info(f"CV analysis completed for {event.record_id}: {result.get('ai_threat_level', 'UNKNOWN')}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing CV threat event {event.record_id}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

# Access Control Analysis Endpoint
@app.post("/analyze/access-control", response_model=Dict[str, Any])
async def analyze_access_control(event: AccessControlEvent):
    """Analyze access control system event."""
    try:
        logger.info(f"Analyzing access control event: {event.alarm_id}")
        
        # Convert event to dict for analysis
        event_dict = event.dict()
        
        # Run triage analysis
        result = run_triage_analysis(event_dict, "Access_Control_System")
        
        logger.info(f"Access control analysis completed for {event.alarm_id}: {result.get('ai_threat_level', 'UNKNOWN')}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing access control event {event.alarm_id}: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

# Batch Analysis Endpoint
@app.post("/analyze/batch")
async def analyze_batch(
    events: List[Dict[str, Any]], 
    event_types: List[str],
    background_tasks: BackgroundTasks
):
    """Analyze multiple events in batch."""
    try:
        if len(events) != len(event_types):
            raise HTTPException(
                status_code=400,
                detail="Number of events must match number of event types"
            )
        
        logger.info(f"Starting batch analysis of {len(events)} events")
        
        # Validate event types
        valid_types = ["CV_Threat_Detection", "Access_Control_System"]
        for event_type in event_types:
            if event_type not in valid_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid event type: {event_type}. Must be one of: {valid_types}"
                )
        
        # Run batch analysis
        results = batch_analyze_events(events, event_types)
        
        logger.info(f"Batch analysis completed for {len(events)} events")
        
        return {
            "total_events": len(events),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch analysis: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )

# Generic Analysis Endpoint
@app.post("/analyze")
async def analyze_event(
    event_data: Dict[str, Any],
    event_type: str
):
    """Generic event analysis endpoint."""
    try:
        valid_types = ["CV_Threat_Detection", "Access_Control_System"]
        if event_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid event type: {event_type}. Must be one of: {valid_types}"
            )
        
        logger.info(f"Analyzing {event_type} event")
        
        # Run analysis
        result = run_triage_analysis(event_data, event_type)
        
        logger.info(f"Analysis completed: {result.get('ai_threat_level', 'UNKNOWN')}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing event: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

# Statistics Endpoint
@app.get("/stats")
async def get_statistics():
    """Get API usage statistics."""
    try:
        logger.info("Stats endpoint accessed")
        # This would typically pull from a database or metrics system
        # For now, return a simple response
        stats = {
            "service": "Security Triage Agent",
            "version": "1.0.0",
            "uptime": datetime.now().isoformat(),
            "supported_event_types": [
                "CV_Threat_Detection",
                "Access_Control_System"
            ],
            "threat_levels": [
                "CRITICAL",
                "HIGH", 
                "MEDIUM",
                "LOW"
            ]
        }
        logger.info("Stats generated successfully")
        return stats
    except Exception as e:
        logger.error(f"Error generating stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

# Configuration Info Endpoint
@app.get("/config")
async def get_config():
    """Get current configuration information."""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "max_batch_size": 100,
        "supported_models": ["CrewAI with OpenAI GPT"],
        "memory_enabled": True
    }

# Dashboard endpoint
@app.get("/")
async def dashboard():
    """Serve the simulation dashboard."""
    try:
        logger.info("Dashboard route accessed")
        from fastapi.responses import FileResponse
        import os
        
        file_path = 'static/index.html'
        if not os.path.exists(file_path):
            logger.error(f"Dashboard file not found: {file_path}")
            raise HTTPException(status_code=404, detail="Dashboard file not found")
        
        logger.info(f"Serving dashboard file: {file_path}")
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

# Activities page endpoint
@app.get("/activities")
async def activities_page():
    """Serve the activities dashboard."""
    try:
        logger.info("Activities page route accessed")
        from fastapi.responses import FileResponse
        import os
        
        file_path = 'static/activities.html'
        if not os.path.exists(file_path):
            logger.error(f"Activities file not found: {file_path}")
            raise HTTPException(status_code=404, detail="Activities file not found")
        
        logger.info(f"Serving activities file: {file_path}")
        return FileResponse(file_path)
    except Exception as e:
        logger.error(f"Error serving activities page: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Activities page error: {str(e)}")

# API root endpoint
@app.get("/api")
async def api_root():
    """API information endpoint."""
    return {
        "service": "Security Triage Agent API",
        "version": "1.0.0",
        "description": "CrewAI-powered security event analysis and triage system",
        "endpoints": {
            "dashboard": "/",
            "health": "/health",
            "simulation": "/simulate",
            "cv_threat_analysis": "/analyze/cv-threat",
            "access_control_analysis": "/analyze/access-control",
            "batch_analysis": "/analyze/batch",
            "generic_analysis": "/analyze",
            "statistics": "/stats",
            "configuration": "/config"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    import signal
    import sys
    
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal, stopping server...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Get configuration from environment
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("PORT", "8001"))
        
        logger.info(f"Starting Security Triage Agent API on {host}:{port}")
        
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info",
            access_log=True,
            reload=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        sys.exit(1)