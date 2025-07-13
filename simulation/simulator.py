from fastapi import APIRouter, HTTPException
from simulation.data_loader import DataLoader
from agents.triage_agent import run_triage_analysis
from models.event_models import CVThreatEvent, AccessControlEvent
from typing import Dict, Any, List
import json
import random

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

@router.get("/activities")
async def simulate_activities(count: int = 5, activity_type: str = None):
    """Simulate activity events with proper categorization."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    if count > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 activities per request")
    
    # Event type mapping
    EVENT_TYPE_MAPPING = {
        # CV Events
        "Person Brandishing Firearm": {"category": "health & safety", "icon": "🏥"},
        "Smoke or Fire": {"category": "health & safety", "icon": "🏥"},
        "Person Falling Down": {"category": "health & safety", "icon": "🏥"},
        "Person Jumping Fence": {"category": "perimeter intrusion", "icon": "👣"},
        "Tailgating": {"category": "perimeter intrusion", "icon": "👣"},
        "Door Propped Open": {"category": "policy-violation", "icon": "⚠️"},
        
        # Access Control Events
        "Door Forced Open": {"category": "perimeter intrusion", "icon": "👣"},
        "Invalid Badge Read": {"category": "perimeter intrusion", "icon": "👣"},
        "Door Held Open": {"category": "perimeter intrusion", "icon": "👣"},
        "Granted Access": {"category": "access-control", "icon": "🚪"}
    }
    
    activities = []
    
    try:
        for _ in range(count):
            # Randomly choose between CV and Access events
            event_source = random.choice(["cv", "access"])
            
            if event_source == "cv":
                event = data_loader.get_random_cv_event()
                if event:
                    event_data = event.dict()
                    analysis_result = run_triage_analysis(event_data, "CV_Threat_Detection")
                    detection_name = event_data.get('detection_name', 'Unknown')
                    
                    # Get activity mapping
                    mapping = EVENT_TYPE_MAPPING.get(detection_name, {
                        "category": "unknown", 
                        "icon": "❓"
                    })
                    
                    # Filter by activity type if specified
                    if activity_type and mapping["category"] != activity_type:
                        continue
                    
                    activity = {
                        "id": f"ACT-CV-{event_data.get('alert_event_id', random.randint(1000, 9999))}",
                        "type": mapping["category"],
                        "icon": mapping["icon"],
                        "title": detection_name,
                        "description": f"Computer vision detection at {event_data.get('site_name', 'Unknown Site')}",
                        "location": {
                            "building": event_data.get('site_name', 'Unknown'),
                            "camera": event_data.get('camera_name', 'Unknown Camera'),
                            "zone": "Security Zone"
                        },
                        "timestamp": event_data.get('creation_time', ''),
                        "threat_level": analysis_result.get('ai_threat_level', 'UNKNOWN'),
                        "confidence": analysis_result.get('confidence_score', 0),
                        "priority_score": analysis_result.get('priority_score', 5),
                        "source": "CV System",
                        "original_event": event_data,
                        "analysis_result": analysis_result
                    }
                    activities.append(activity)
            
            else:  # access event
                event = data_loader.get_random_access_event()
                if event:
                    event_data = event.dict()
                    analysis_result = run_triage_analysis(event_data, "Access_Control_System")
                    alarm_name = event_data.get('alarm_name', 'Unknown')
                    
                    # Get activity mapping
                    mapping = EVENT_TYPE_MAPPING.get(alarm_name, {
                        "category": "unknown", 
                        "icon": "❓"
                    })
                    
                    # Filter by activity type if specified
                    if activity_type and mapping["category"] != activity_type:
                        continue
                    
                    activity = {
                        "id": f"ACT-AC-{event_data.get('alarm_id', random.randint(1000, 9999))}",
                        "type": mapping["category"],
                        "icon": mapping["icon"],
                        "title": alarm_name,
                        "description": f"Access control event at {event_data.get('device_id', 'Unknown Device')}",
                        "location": {
                            "building": "Building", 
                            "device": event_data.get('device_id', 'Unknown Device'),
                            "zone": "Access Point"
                        },
                        "timestamp": event_data.get('timestamp', ''),
                        "threat_level": analysis_result.get('ai_threat_level', 'UNKNOWN'),
                        "confidence": analysis_result.get('confidence_score', 0),
                        "priority_score": analysis_result.get('priority_score', 5),
                        "source": "Access Control",
                        "original_event": event_data,
                        "analysis_result": analysis_result
                    }
                    activities.append(activity)
        
        # Sort by priority score (descending) and timestamp
        activities.sort(key=lambda x: (-x["priority_score"], x["timestamp"]), reverse=True)
        
        return {
            "status": "success",
            "total_activities": len(activities),
            "activities": activities,
            "filter_applied": activity_type,
            "event_type_mapping": EVENT_TYPE_MAPPING
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Activities simulation failed: {str(e)}")

@router.get("/activities/stats")
async def get_activities_stats():
    """Get activity statistics by type."""
    if data_loader is None:
        raise HTTPException(status_code=500, detail="Data loader not initialized")
    
    try:
        # Generate sample activities to get stats
        activities_response = await simulate_activities(count=20)
        activities = activities_response["activities"]
        
        # Count by type
        type_counts = {}
        threat_level_counts = {}
        
        for activity in activities:
            activity_type = activity["type"]
            threat_level = activity["threat_level"]
            
            type_counts[activity_type] = type_counts.get(activity_type, 0) + 1
            threat_level_counts[threat_level] = threat_level_counts.get(threat_level, 0) + 1
        
        # Calculate averages
        total_activities = len(activities)
        avg_confidence = sum(a["confidence"] for a in activities) / total_activities if total_activities > 0 else 0
        avg_priority = sum(a["priority_score"] for a in activities) / total_activities if total_activities > 0 else 0
        
        return {
            "status": "success",
            "total_activities": total_activities,
            "type_breakdown": type_counts,
            "threat_level_distribution": threat_level_counts,
            "average_confidence": round(avg_confidence, 2),
            "average_priority_score": round(avg_priority, 1),
            "activity_types": [
                {"type": "health & safety", "icon": "🏥"},
                {"type": "perimeter intrusion", "icon": "👣"},
                {"type": "policy-violation", "icon": "⚠️"},
                {"type": "access-control", "icon": "🚪"}
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats generation failed: {str(e)}")

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