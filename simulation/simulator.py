from fastapi import APIRouter, HTTPException
from simulation.data_loader import DataLoader
from agents.triage_agent import run_triage_analysis, run_sop_enhanced_analysis
from models.event_models import CVThreatEvent, AccessControlEvent
from typing import Dict, Any, List
import json
import random
import logging

logger = logging.getLogger(__name__)

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
async def simulate_activities(count: int = 5, activity_type: str = None, fast_mode: bool = False):
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
                    
                    # Run both standard and SOP-enhanced analysis
                    analysis_result = run_triage_analysis(event_data, "CV_Threat_Detection")
                    
                    # Run SOP-enhanced analysis with caching
                    if fast_mode:
                        # Fast mode: use predefined SOP overrides
                        detection_name = event_data.get('detection_name', '').lower()
                        if 'fall' in detection_name or 'person down' in detection_name:
                            sop_analysis_result = {
                                "event_type": "CV_Threat_Detection",
                                "final_threat_level": "MEDICAL EMERGENCY",
                                "final_priority_score": 10,
                                "confidence_score": 0.95,
                                "merged_response_actions": ["IMMEDIATE: Dispatch first aid", "CONTACT emergency services"],
                                "escalation_required": True,
                                "response_timeline": "IMMEDIATE (within 30 seconds)",
                                "sop_influence_reasoning": "Medical Emergency SOP applied - HIGH priority override for fall detection",
                                "applicable_sops": [{"title": "Medical Emergency Response Protocol", "priority_override": "HIGH"}],
                                "sop_analysis_failed": False
                            }
                        elif 'firearm' in detection_name or 'weapon' in detection_name:
                            sop_analysis_result = {
                                "event_type": "CV_Threat_Detection", 
                                "final_threat_level": "HIGH",
                                "final_priority_score": 9,
                                "confidence_score": 0.9,
                                "merged_response_actions": ["IMMEDIATE: Contact law enforcement", "EVACUATE area"],
                                "escalation_required": True,
                                "response_timeline": "IMMEDIATE",
                                "sop_influence_reasoning": "Weapon Protocol applied - HIGH priority override",
                                "applicable_sops": [{"title": "Weapon Incident Protocol", "priority_override": "HIGH"}],
                                "sop_analysis_failed": False
                            }
                        else:
                            # Use standard analysis as SOP result
                            sop_analysis_result = analysis_result.copy()
                            sop_analysis_result.update({
                                "sop_influence_reasoning": "No applicable SOPs found - using standard analysis",
                                "applicable_sops": [],
                                "sop_analysis_failed": False
                            })
                        logger.info(f"Fast mode SOP analysis for CV event {event_data.get('alert_event_id')}")
                    else:
                        try:
                            # Create cache key based on detection type
                            cache_key = f"{event_data.get('detection_name', 'unknown')}_{event_data.get('severity', 'unknown')}"
                            
                            # Check if we have a cached result for this type of event
                            if hasattr(run_sop_enhanced_analysis, '_cache') and cache_key in run_sop_enhanced_analysis._cache:
                                sop_analysis_result = run_sop_enhanced_analysis._cache[cache_key].copy()
                                logger.info(f"Using cached SOP analysis for CV event {event_data.get('alert_event_id')}")
                            else:
                                sop_analysis_result = run_sop_enhanced_analysis(event_data, "CV_Threat_Detection")
                                
                                # Cache the result
                                if not hasattr(run_sop_enhanced_analysis, '_cache'):
                                    run_sop_enhanced_analysis._cache = {}
                                run_sop_enhanced_analysis._cache[cache_key] = sop_analysis_result.copy()
                                
                                logger.info(f"SOP analysis completed and cached for CV event {event_data.get('alert_event_id')}")
                        except Exception as e:
                            logger.warning(f"SOP analysis failed for CV event: {e}")
                            # Fallback to standard analysis structure with SOP failure indicators
                            sop_analysis_result = {
                                "event_type": "CV_Threat_Detection",
                                "final_threat_level": analysis_result.get('ai_threat_level', 'MEDIUM'),
                                "final_priority_score": analysis_result.get('priority_score', 5),
                                "confidence_score": analysis_result.get('confidence_score', 0.7),
                                "merged_response_actions": analysis_result.get('recommended_actions', []),
                                "escalation_required": analysis_result.get('escalation_required', False),
                                "response_timeline": analysis_result.get('response_timeline', '15 minutes'),
                                "sop_influence_reasoning": f"SOP analysis unavailable: {str(e)}",
                                "applicable_sops": [],
                                "sop_analysis_failed": True
                            }
                    
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
                        "analysis_result": analysis_result,
                        # SOP-enhanced fields
                        "sop_analysis_result": sop_analysis_result,
                        "sop_priority_score": sop_analysis_result.get('final_priority_score', analysis_result.get('priority_score', 5)),
                        "sop_threat_level": sop_analysis_result.get('final_threat_level', analysis_result.get('ai_threat_level', 'UNKNOWN')),
                        "sop_influence_reasoning": sop_analysis_result.get('sop_influence_reasoning', 'No SOP consultation performed'),
                        "applicable_sops": sop_analysis_result.get('applicable_sops', []),
                        "sop_analysis_failed": sop_analysis_result.get('sop_analysis_failed', False)
                    }
                    activities.append(activity)
            
            else:  # access event
                event = data_loader.get_random_access_event()
                if event:
                    event_data = event.dict()
                    
                    # Run both standard and SOP-enhanced analysis
                    analysis_result = run_triage_analysis(event_data, "Access_Control_System")
                    
                    # Run SOP-enhanced analysis
                    try:
                        sop_analysis_result = run_sop_enhanced_analysis(event_data, "Access_Control_System")
                        logger.info(f"SOP analysis completed for Access Control event {event_data.get('alarm_id')}")
                    except Exception as e:
                        logger.warning(f"SOP analysis failed for Access Control event: {e}")
                        # Fallback to standard analysis structure with SOP failure indicators
                        sop_analysis_result = {
                            "event_type": "Access_Control_System",
                            "final_threat_level": analysis_result.get('ai_threat_level', 'MEDIUM'),
                            "final_priority_score": analysis_result.get('priority_score', 5),
                            "confidence_score": analysis_result.get('confidence_score', 0.7),
                            "merged_response_actions": analysis_result.get('recommended_actions', []),
                            "escalation_required": analysis_result.get('escalation_required', False),
                            "response_timeline": analysis_result.get('response_timeline', '15 minutes'),
                            "sop_influence_reasoning": f"SOP analysis unavailable: {str(e)}",
                            "applicable_sops": [],
                            "sop_analysis_failed": True
                        }
                    
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
                        "analysis_result": analysis_result,
                        # SOP-enhanced fields
                        "sop_analysis_result": sop_analysis_result,
                        "sop_priority_score": sop_analysis_result.get('final_priority_score', analysis_result.get('priority_score', 5)),
                        "sop_threat_level": sop_analysis_result.get('final_threat_level', analysis_result.get('ai_threat_level', 'UNKNOWN')),
                        "sop_influence_reasoning": sop_analysis_result.get('sop_influence_reasoning', 'No SOP consultation performed'),
                        "applicable_sops": sop_analysis_result.get('applicable_sops', []),
                        "sop_analysis_failed": sop_analysis_result.get('sop_analysis_failed', False)
                    }
                    activities.append(activity)
        
        # Sort by SOP priority score first (if available), then standard priority score, then timestamp
        activities.sort(key=lambda x: (-x.get("sop_priority_score", x["priority_score"]), -x["priority_score"], x["timestamp"]), reverse=True)
        
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