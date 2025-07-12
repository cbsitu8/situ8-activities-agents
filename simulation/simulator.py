from fastapi import APIRouter, HTTPException
from simulation.data_loader import DataLoader
from agents.triage_agent import run_triage_analysis
from models.event_models import CVThreatEvent, AccessControlEvent
from typing import Dict, Any
import json

# Initialize router
router = APIRouter(prefix="/simulate", tags=["simulation"])

# Global data loader instance
data_loader: DataLoader = None

def initialize_data_loader(cv_csv_path: str, access_csv_path: str):
    """Initialize the global data loader."""
    global data_loader
    data_loader = DataLoader(cv_csv_path, access_csv_path)

@router.get("/cv")
async def simulate_cv_event():
    """Simulate a random computer vision threat event."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    # Get random CV event
    cv_event = data_loader.get_random_cv_event()
    if cv_event is None:
        raise HTTPException(status_code=404, detail="No CV events available")
    
    try:
        # Convert to the format expected by the analyzer
        event_data = cv_event.dict()
        
        # Run analysis
        analysis_result = run_triage_analysis(event_data, "CV_Threat_Detection")
        
        return {
            "status": "success",
            "event_type": "CV_Threat_Detection",
            "original_event": event_data,
            "analysis_result": analysis_result,
            "timestamp": cv_event.creation_time
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/access")
async def simulate_access_event():
    """Simulate a random access control event."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    # Get random access event
    access_event = data_loader.get_random_access_event()
    if access_event is None:
        raise HTTPException(status_code=404, detail="No access control events available")
    
    try:
        # Convert to the format expected by the analyzer
        event_data = access_event.dict()
        
        # Run analysis
        analysis_result = run_triage_analysis(event_data, "Access_Control_System")
        
        return {
            "status": "success",
            "event_type": "Access_Control_System",
            "original_event": event_data,
            "analysis_result": analysis_result,
            "timestamp": access_event.timestamp
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/stats")
async def get_simulation_stats():
    """Get simulation statistics."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    return {
        "status": "success",
        "stats": data_loader.get_stats()
    }

@router.get("/batch")
async def simulate_batch_events(cv_count: int = 2, access_count: int = 2):
    """Simulate multiple events in batch."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    if cv_count > 10 or access_count > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 events per type in batch")
    
    results = []
    
    try:
        # Process CV events
        for _ in range(cv_count):
            cv_event = data_loader.get_random_cv_event()
            if cv_event:
                event_data = cv_event.dict()
                analysis_result = run_triage_analysis(event_data, "CV_Threat_Detection")
                results.append({
                    "event_type": "CV_Threat_Detection",
                    "original_event": event_data,
                    "analysis_result": analysis_result,
                    "timestamp": cv_event.creation_time
                })
        
        # Process Access Control events
        for _ in range(access_count):
            access_event = data_loader.get_random_access_event()
            if access_event:
                event_data = access_event.dict()
                analysis_result = run_triage_analysis(event_data, "Access_Control_System")
                results.append({
                    "event_type": "Access_Control_System",
                    "original_event": event_data,
                    "analysis_result": analysis_result,
                    "timestamp": access_event.timestamp
                })
        
        return {
            "status": "success",
            "total_events": len(results),
            "cv_events_processed": cv_count,
            "access_events_processed": access_count,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.get("/health")
async def simulation_health():
    """Check simulation system health."""
    if data_loader is None:
        return {
            "status": "error",
            "message": "Data loader not initialized"
        }
    
    stats = data_loader.get_stats()
    
    return {
        "status": "healthy",
        "data_loader_initialized": True,
        "cv_events_available": stats["cv_events_loaded"],
        "access_events_available": stats["access_events_loaded"],
        "csv_files_found": stats["cv_csv_exists"] and stats["access_csv_exists"]
    }