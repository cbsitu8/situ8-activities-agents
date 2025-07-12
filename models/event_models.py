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
    stored_at: str
    record_id: str
    data: Dict[str, Any]
    
    @property
    def threat_signature(self) -> Dict[str, Any]:
        return self.data.get('threatSignature', {})
    
    @property
    def location(self) -> str:
        space = self.data.get('stream', {}).get('space', {})
        return space.get('fullPath', 'Unknown Location')
    
    @property
    def severity(self) -> str:
        return self.data.get('severity', 'UNKNOWN')
    
    @property
    def alert_name(self) -> str:
        return self.data.get('alertName', 'Unknown Alert')
    
    @property
    def site_name(self) -> str:
        return self.data.get('site', {}).get('name', 'Unknown Site')

class AccessControlEvent(BaseModel):
    serial_number: str
    device_id: str
    controller_id: str
    segment_id: str
    timestamp_processed: str
    alarm_name: str
    timestamp: str
    alarm_id: str
    source: str
    Subdevice_id: str

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