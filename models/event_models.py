from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class ThreatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class CVThreatEvent(BaseModel):
    alert_event_id: str
    severity: str
    site_name: str
    detection_name: str
    creation_time: str
    camera_name: str
    readers_name: Optional[str] = None
    
    @property
    def threat_signature(self) -> Dict[str, Any]:
        return {
            "name": self.detection_name,
            "id": self.alert_event_id
        }
    
    @property
    def location(self) -> str:
        return f"{self.site_name} > {self.camera_name}"
    
    @property
    def alert_name(self) -> str:
        return self.detection_name

class AccessControlEvent(BaseModel):
    serial_number: str
    device_id: str
    controller_id: str
    segment_id: str
    alarm_name: str
    timestamp: str
    alarm_id: str
    badge_id: Optional[str] = None

class TriageAnalysis(BaseModel):
    event_type: str
    ai_threat_level: ThreatLevel
    false_positive_probability: float
    confidence_score: float
    recommended_actions: List[str]
    escalation_required: bool
    response_timeline: str
    analysis_reasoning: str
    event_summary: str
    priority_score: int  # 1-10 scale