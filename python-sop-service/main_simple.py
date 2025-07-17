"""
Simple SOP Processing Service - Basic FastAPI Application
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for uploaded SOPs (for demo purposes)
uploaded_sops = []

app = FastAPI(
    title="SOP Processing Service",
    description="Simple SOP processing service for testing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting Simple SOP Processing Service...")
    logger.info("Service started successfully")

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "python-sop-service",
        "version": "1.0.0",
        "message": "Simple mode - ready for development"
    }

@app.get("/api/v1/sops")
async def list_sops():
    """List all stored SOPs"""
    # Include both uploaded SOPs and the sample SOP (if not deleted)
    all_sops = []
    
    if not sample_sop_deleted:
        sample_sop = {
            "id": "sample-001",
            "name": "Medical Emergency Response",
            "file_name": "medical_emergency.md",
            "file_type": "md",
            "upload_status": "completed",
            "rule_count": 3,
            "created_at": "2025-01-15T10:00:00Z"
        }
        all_sops.append(sample_sop)
    
    all_sops.extend(uploaded_sops)
    
    return {
        "sops": all_sops
    }

@app.post("/api/v1/sop/process")
async def process_sop(file: UploadFile = File(...), name: str = Form(...)):
    """Process uploaded SOP document (mock)"""
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in ['docx', 'md', 'txt']:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: .{file_extension}")
        
        # Read file content (for validation)
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Mock processing - simulate successful upload
        sop_id = str(uuid.uuid4())
        
        logger.info(f"Processing SOP: {file.filename} ({len(content)} bytes)")
        
        # Create SOP record
        sop_record = {
            "id": sop_id,
            "name": name or file.filename,
            "file_name": file.filename,
            "file_type": file_extension,
            "upload_status": "completed",
            "rule_count": 3,  # Mock number
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Store in memory
        uploaded_sops.append(sop_record)
        
        return {
            "sop_id": sop_id,
            "name": name or file.filename,
            "file_name": file.filename,
            "file_type": file_extension,
            "status": "completed",
            "rules_extracted": 3,  # Mock number
            "message": "SOP processed successfully",
            "created_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing SOP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sop/process-bulk")
async def process_bulk_sops(files: List[UploadFile] = File(...)):
    """Process multiple SOP documents at once"""
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(files) > 10:  # Limit to 10 files at once
        raise HTTPException(status_code=400, detail="Maximum 10 files allowed per upload")
    
    results = []
    errors = []
    
    for file in files:
        try:
            # Validate file type
            if not file.filename:
                errors.append({"file": "Unknown", "error": "No filename provided"})
                continue
            
            file_extension = file.filename.split('.')[-1].lower()
            if file_extension not in ['docx', 'md', 'txt']:
                errors.append({"file": file.filename, "error": f"Unsupported file type: .{file_extension}"})
                continue
            
            # Read file content (for validation)
            content = await file.read()
            if len(content) == 0:
                errors.append({"file": file.filename, "error": "Empty file"})
                continue
            
            # Validate file size (max 10MB)
            if len(content) > 10 * 1024 * 1024:
                errors.append({"file": file.filename, "error": "File too large. Maximum size is 10MB"})
                continue
            
            # Mock processing - simulate successful upload
            sop_id = str(uuid.uuid4())
            
            logger.info(f"Processing SOP: {file.filename} ({len(content)} bytes)")
            
            # Create SOP record
            sop_record = {
                "id": sop_id,
                "name": file.filename,
                "file_name": file.filename,
                "file_type": file_extension,
                "upload_status": "completed",
                "rule_count": 3,  # Mock number
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Store in memory
            uploaded_sops.append(sop_record)
            
            results.append({
                "sop_id": sop_id,
                "name": file.filename,
                "file_name": file.filename,
                "file_type": file_extension,
                "status": "completed",
                "rules_extracted": 3,  # Mock number
                "created_at": datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error processing SOP {file.filename}: {e}")
            errors.append({"file": file.filename, "error": str(e)})
    
    return {
        "total_files": len(files),
        "successful": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors,
        "message": f"Processed {len(results)} files successfully, {len(errors)} failed"
    }

@app.get("/api/v1/sops/{sop_id}/rules")
async def get_sop_rules(sop_id: str):
    """Get rules for a specific SOP"""
    # Check if it's the sample SOP
    if sop_id == "sample-001":
        if sample_sop_deleted:
            raise HTTPException(status_code=404, detail="SOP not found")
        return {
            "rules": [
                {
                    "id": "rule-001",
                    "rule_type": "exact",
                    "rule_value": ["Person Falling Down", "Person Brandishing Firearm"],
                    "priority": "CRITICAL",
                    "agent_assignments": ["EnvironmentAgent", "EscalationAgent"],
                    "created_at": "2025-01-15T10:00:00Z"
                },
                {
                    "id": "rule-002", 
                    "rule_type": "keyword",
                    "rule_value": ["fall", "medical", "emergency"],
                    "priority": "HIGH",
                    "agent_assignments": ["EnvironmentAgent"],
                    "created_at": "2025-01-15T10:00:00Z"
                },
                {
                    "id": "rule-003",
                    "rule_type": "semantic",
                    "rule_value": ["medical emergency", "health crisis", "injury incident"],
                    "priority": "HIGH", 
                    "agent_assignments": ["MedicalAgent", "EscalationAgent"],
                    "created_at": "2025-01-15T10:00:00Z"
                }
            ]
        }
    
    # Find the uploaded SOP
    uploaded_sop = None
    for sop in uploaded_sops:
        if sop["id"] == sop_id:
            uploaded_sop = sop
            break
    
    if not uploaded_sop:
        raise HTTPException(status_code=404, detail="SOP not found")
    
    # Generate dynamic rules based on the uploaded SOP
    file_type = uploaded_sop["file_type"]
    sop_name = uploaded_sop["name"]
    
    # Create different rules based on file type and name
    rules = []
    
    if "fire" in sop_name.lower() or "smoke" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Smoke or Fire", "Fire Detection", "Smoke Detection"],
                "priority": "CRITICAL",
                "agent_assignments": ["FireSafetyAgent", "EmergencyAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["fire", "smoke", "burning", "flames"],
                "priority": "CRITICAL",
                "agent_assignments": ["FireSafetyAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "shooter" in sop_name.lower() or "active" in sop_name.lower() or "weapon" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Person Brandishing Firearm", "Active Shooter", "Weapon Detected"],
                "priority": "CRITICAL",
                "agent_assignments": ["SecurityAgent", "EmergencyAgent", "LawEnforcementAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["firearm", "gun", "weapon", "shooter", "brandishing"],
                "priority": "CRITICAL",
                "agent_assignments": ["SecurityAgent", "LawEnforcementAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "perimeter" in sop_name.lower() or "intrusion" in sop_name.lower() or "fence" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Person Jumping Fence", "Perimeter Breach", "Tailgating"],
                "priority": "HIGH",
                "agent_assignments": ["SecurityAgent", "PerimeterAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["fence", "perimeter", "intrusion", "breach", "tailgating"],
                "priority": "HIGH",
                "agent_assignments": ["SecurityAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "security" in sop_name.lower() or "access" in sop_name.lower() or "unauthorized" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Unauthorized Access", "Badge Tailgating", "Door Forced Open"],
                "priority": "CRITICAL",
                "agent_assignments": ["SecurityAgent", "AccessControlAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword", 
                "rule_value": ["access", "badge", "door", "security", "unauthorized"],
                "priority": "HIGH",
                "agent_assignments": ["SecurityAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "emergency" in sop_name.lower() or "medical" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Smoke or Fire", "Fire Detection", "Smoke Detection"],
                "priority": "CRITICAL",
                "agent_assignments": ["FireSafetyAgent", "EmergencyAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["fire", "smoke", "burning", "flames"],
                "priority": "CRITICAL",
                "agent_assignments": ["FireSafetyAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "shooter" in sop_name.lower() or "active" in sop_name.lower() or "weapon" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Person Brandishing Firearm", "Active Shooter", "Weapon Detected"],
                "priority": "CRITICAL",
                "agent_assignments": ["SecurityAgent", "EmergencyAgent", "LawEnforcementAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["firearm", "gun", "weapon", "shooter", "brandishing"],
                "priority": "CRITICAL",
                "agent_assignments": ["SecurityAgent", "LawEnforcementAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    elif "perimeter" in sop_name.lower() or "intrusion" in sop_name.lower() or "fence" in sop_name.lower():
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "exact",
                "rule_value": ["Person Jumping Fence", "Perimeter Breach", "Tailgating"],
                "priority": "HIGH",
                "agent_assignments": ["SecurityAgent", "PerimeterAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "keyword",
                "rule_value": ["fence", "perimeter", "intrusion", "breach", "tailgating"],
                "priority": "HIGH",
                "agent_assignments": ["SecurityAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    else:
        # Default rules for generic SOPs
        rules = [
            {
                "id": f"rule-{sop_id}-001",
                "rule_type": "keyword",
                "rule_value": ["incident", "alert", "violation"],
                "priority": "MEDIUM",
                "agent_assignments": ["GeneralAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-002",
                "rule_type": "pattern",
                "rule_value": [".*suspicious.*", ".*anomaly.*"],
                "priority": "MEDIUM",
                "agent_assignments": ["PatternAgent"],
                "created_at": uploaded_sop["created_at"]
            },
            {
                "id": f"rule-{sop_id}-003",
                "rule_type": "exact",
                "rule_value": ["File Content Based Rule", f"Processed from {file_type.upper()} file"],
                "priority": "LOW",
                "agent_assignments": ["DocumentAgent"],
                "created_at": uploaded_sop["created_at"]
            }
        ]
    
    return {"rules": rules}

@app.get("/api/v1/sops/{sop_id}")
async def get_sop_details(sop_id: str):
    """Get details for a specific SOP"""
    # Check sample SOP
    if sop_id == "sample-001":
        if sample_sop_deleted:
            raise HTTPException(status_code=404, detail="SOP not found")
        return {
            "id": "sample-001",
            "name": "Medical Emergency Response",
            "file_name": "medical_emergency.md",
            "file_type": "md",
            "upload_status": "completed",
            "rule_count": 3,
            "created_at": "2025-01-15T10:00:00Z",
            "content": "# Medical Emergency Response SOP\n\nThis SOP covers procedures for medical emergencies including falls, injuries, and health crises.",
            "description": "Standard operating procedure for handling medical emergencies in the facility"
        }
    
    # Find uploaded SOP
    for sop in uploaded_sops:
        if sop["id"] == sop_id:
            return sop
    
    raise HTTPException(status_code=404, detail="SOP not found")

@app.put("/api/v1/sops/{sop_id}")
async def update_sop(sop_id: str, update_data: dict):
    """Update an existing SOP"""
    # Cannot update sample SOP
    if sop_id == "sample-001":
        raise HTTPException(status_code=403, detail="Cannot modify sample SOP")
    
    # Find and update uploaded SOP
    for i, sop in enumerate(uploaded_sops):
        if sop["id"] == sop_id:
            # Update allowed fields
            if "name" in update_data:
                uploaded_sops[i]["name"] = update_data["name"]
            if "description" in update_data:
                uploaded_sops[i]["description"] = update_data["description"]
            
            uploaded_sops[i]["updated_at"] = datetime.utcnow().isoformat()
            
            logger.info(f"Updated SOP {sop_id}: {update_data}")
            return uploaded_sops[i]
    
    raise HTTPException(status_code=404, detail="SOP not found")

# Global flag to track if sample SOP is deleted
sample_sop_deleted = False

@app.delete("/api/v1/sops/{sop_id}")
async def delete_sop(sop_id: str):
    """Delete a SOP"""
    global sample_sop_deleted
    
    # Handle sample SOP deletion
    if sop_id == "sample-001":
        if sample_sop_deleted:
            raise HTTPException(status_code=404, detail="SOP not found")
        sample_sop_deleted = True
        logger.info(f"Deleted SOP {sop_id}: Medical Emergency Response")
        return {
            "message": "SOP 'Medical Emergency Response' deleted successfully",
            "deleted_sop": {
                "id": "sample-001",
                "name": "Medical Emergency Response"
            }
        }
    
    # Find and remove uploaded SOP
    for i, sop in enumerate(uploaded_sops):
        if sop["id"] == sop_id:
            deleted_sop = uploaded_sops.pop(i)
            logger.info(f"Deleted SOP {sop_id}: {deleted_sop['name']}")
            return {
                "message": f"SOP '{deleted_sop['name']}' deleted successfully",
                "deleted_sop": deleted_sop
            }
    
    raise HTTPException(status_code=404, detail="SOP not found")

async def match_event_to_sops(event_type: str):
    """Match an event to actual SOPs and their rules"""
    # Get all SOPs (including sample and uploaded)
    all_sops = []
    
    if not sample_sop_deleted:
        sample_sop = {
            "id": "sample-001",
            "name": "Medical Emergency Response",
            "file_name": "medical_emergency.md",
            "file_type": "md",
            "upload_status": "completed",
            "rule_count": 3,
            "created_at": "2025-01-15T10:00:00Z"
        }
        all_sops.append(sample_sop)
    
    all_sops.extend(uploaded_sops)
    
    best_match = None
    best_confidence = 0.0
    matched_rules = []
    
    for sop in all_sops:
        # Get rules for this SOP (reuse the logic from get_sop_rules)
        if sop["id"] == "sample-001":
            rules = [
                {
                    "rule_type": "exact",
                    "rule_value": ["Person Falling Down", "Person Brandishing Firearm"],
                    "priority": "CRITICAL",
                    "agent_assignments": ["EnvironmentAgent", "EscalationAgent"]
                },
                {
                    "rule_type": "keyword",
                    "rule_value": ["fall", "medical", "emergency"],
                    "priority": "HIGH", 
                    "agent_assignments": ["EnvironmentAgent"]
                },
                {
                    "rule_type": "semantic",
                    "rule_value": ["medical emergency", "health crisis", "injury incident"],
                    "priority": "HIGH",
                    "agent_assignments": ["MedicalAgent", "EscalationAgent"]
                }
            ]
        else:
            # Generate rules for uploaded SOPs based on their name
            sop_name = sop["name"].lower()
            if "fire" in sop_name or "smoke" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Smoke or Fire", "Fire Detection", "Smoke Detection"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["FireSafetyAgent", "EmergencyAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["fire", "smoke", "burning", "flames"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["FireSafetyAgent"]
                    }
                ]
            elif "shooter" in sop_name or "active" in sop_name or "weapon" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Person Brandishing Firearm", "Active Shooter", "Weapon Detected"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["SecurityAgent", "EmergencyAgent", "LawEnforcementAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["firearm", "gun", "weapon", "shooter", "brandishing"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["SecurityAgent", "LawEnforcementAgent"]
                    }
                ]
            elif "perimeter" in sop_name or "intrusion" in sop_name or "fence" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Person Jumping Fence", "Perimeter Breach", "Tailgating"],
                        "priority": "HIGH",
                        "agent_assignments": ["SecurityAgent", "PerimeterAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["fence", "perimeter", "intrusion", "breach", "tailgating"],
                        "priority": "HIGH",
                        "agent_assignments": ["SecurityAgent"]
                    }
                ]
            elif "security" in sop_name or "access" in sop_name or "unauthorized" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Unauthorized Access", "Badge Tailgating", "Door Forced Open"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["SecurityAgent", "AccessControlAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["access", "badge", "door", "security", "unauthorized"],
                        "priority": "HIGH",
                        "agent_assignments": ["SecurityAgent"]
                    }
                ]
            elif "emergency" in sop_name or "medical" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Person Falling Down", "Medical Emergency"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["MedicalAgent", "EmergencyAgent"]
                    },
                    {
                        "rule_type": "semantic",
                        "rule_value": ["health incident", "injury", "medical crisis"],
                        "priority": "HIGH",
                        "agent_assignments": ["MedicalAgent"]
                    }
                ]
            elif "shooter" in sop_name or "active" in sop_name or "weapon" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Person Brandishing Firearm", "Active Shooter", "Weapon Detected"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["SecurityAgent", "EmergencyAgent", "LawEnforcementAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["firearm", "gun", "weapon", "shooter", "brandishing"],
                        "priority": "CRITICAL",
                        "agent_assignments": ["SecurityAgent", "LawEnforcementAgent"]
                    }
                ]
            elif "perimeter" in sop_name or "intrusion" in sop_name or "fence" in sop_name:
                rules = [
                    {
                        "rule_type": "exact",
                        "rule_value": ["Person Jumping Fence", "Perimeter Breach", "Tailgating"],
                        "priority": "HIGH",
                        "agent_assignments": ["SecurityAgent", "PerimeterAgent"]
                    },
                    {
                        "rule_type": "keyword",
                        "rule_value": ["fence", "perimeter", "intrusion", "breach", "tailgating"],
                        "priority": "HIGH",
                        "agent_assignments": ["SecurityAgent"]
                    }
                ]
            else:
                rules = [
                    {
                        "rule_type": "keyword",
                        "rule_value": ["incident", "alert", "violation"],
                        "priority": "MEDIUM",
                        "agent_assignments": ["GeneralAgent"]
                    }
                ]
        
        # Check each rule for matches
        for rule in rules:
            confidence = 0.0
            match_type = None
            
            if rule["rule_type"] == "exact":
                # Exact string matching
                for value in rule["rule_value"]:
                    if value.lower() == event_type.lower():
                        confidence = 0.95
                        match_type = f"{value} - Exact Match"
                        break
            elif rule["rule_type"] == "keyword":
                # Keyword matching
                event_lower = event_type.lower()
                matches = []
                for keyword in rule["rule_value"]:
                    if keyword.lower() in event_lower:
                        matches.append(keyword)
                if matches:
                    confidence = 0.75 + (0.1 * len(matches))  # Higher confidence for more keyword matches
                    match_type = f"Keywords: {', '.join(matches)}"
            elif rule["rule_type"] == "semantic":
                # Simple semantic matching (contains similar terms)
                event_lower = event_type.lower()
                for phrase in rule["rule_value"]:
                    phrase_words = phrase.lower().split()
                    event_words = event_lower.split()
                    common_words = set(phrase_words) & set(event_words)
                    if common_words:
                        confidence = 0.60 + (0.1 * len(common_words))
                        match_type = f"Semantic: {phrase}"
                        break
            
            # Update best match if this rule has higher confidence
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = sop
                matched_rules = [match_type] if match_type else []
    
    return best_match, best_confidence, matched_rules

@app.post("/api/v1/events/process")
async def process_event(event_data: dict):
    """Process a security event using actual SOPs"""
    try:
        event_type = event_data.get("event_type", "Unknown")
        event_details = event_data.get("event_details", "")
        location = event_data.get("location", "Unknown")
        
        logger.info(f"Processing event: {event_type} at {location}")
        
        # Match event against actual SOPs
        matched_sop, confidence, matched_rules = await match_event_to_sops(event_type)
        
        if matched_sop:
            # Determine priority and agents based on the matched SOP and confidence
            if confidence >= 0.9:
                priority = "CRITICAL"
                response_time = f"{8 + int((1 - confidence) * 20)}ms"
            elif confidence >= 0.7:
                priority = "HIGH" 
                response_time = f"{15 + int((1 - confidence) * 30)}ms"
            elif confidence >= 0.5:
                priority = "MEDIUM"
                response_time = f"{25 + int((1 - confidence) * 40)}ms"
            else:
                priority = "LOW"
                response_time = f"{35 + int((1 - confidence) * 50)}ms"
            
            # Generate actions based on SOP type
            sop_name_lower = matched_sop["name"].lower()
            if "medical" in sop_name_lower or "emergency" in sop_name_lower:
                actions = [
                    "Immediate medical response",
                    "Secure the area",
                    "Notify emergency contacts",
                    "Document incident details"
                ]
                agents = ["MedicalAgent", "EmergencyAgent"]
            elif "security" in sop_name_lower or "access" in sop_name_lower:
                actions = [
                    "Immediate security response", 
                    "Verify access credentials",
                    "Check security logs",
                    "Escalate if necessary"
                ]
                agents = ["SecurityAgent", "AccessControlAgent"]
            else:
                actions = [
                    "Log incident",
                    "Assess severity", 
                    "Follow SOP guidelines",
                    "Monitor for escalation"
                ]
                agents = ["GeneralAgent"]
            
            result = {
                "event_id": f"evt_{uuid.uuid4().hex[:8]}",
                "priority": priority,
                "matched_sop": matched_sop["name"],
                "matched_sop_id": matched_sop["id"],
                "matched_rules": matched_rules,
                "confidence": confidence,
                "assigned_agents": agents,
                "response_time": response_time,
                "actions_required": actions
            }
        else:
            # No SOP match found
            result = {
                "event_id": f"evt_{uuid.uuid4().hex[:8]}",
                "priority": "LOW",
                "matched_sop": "No SOP Match Found",
                "matched_sop_id": None,
                "matched_rules": ["No matching rules"],
                "confidence": 0.0,
                "assigned_agents": ["DefaultAgent"],
                "response_time": "50ms",
                "actions_required": [
                    "Log unmatched event",
                    "Review and create appropriate SOP",
                    "Manual assessment required"
                ]
            }
        
        # Add processing metadata
        result.update({
            "processed_at": datetime.utcnow().isoformat(),
            "processing_node": "python-sop-service",
            "event_source": event_data.get("source", "simulator"),
            "raw_event": event_data
        })
        
        return result
        
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)