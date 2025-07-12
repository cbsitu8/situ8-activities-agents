from crewai.tools import tool
from typing import Dict, Any, List, Tuple
from models.event_models import ThreatLevel, TriageAnalysis
from datetime import datetime, timedelta
import re

@tool("Access Control Analyzer")
def analyze_access_control(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes access control system events to assess security threats, differentiate between system issues and security concerns, and generate appropriate responses."""
    
    analyzer = AccessControlAnalyzer()
    return analyzer._run(event_data)

class AccessControlAnalyzer:
    def _run(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze an access control event and return triage analysis."""
        
        # Extract key information
        alarm_name = event_data.get('alarm_name', 'Unknown Alarm')
        device_id = event_data.get('device_id', 'Unknown Device')
        source = event_data.get('source', 'Unknown Source')
        controller_id = event_data.get('controller_id', 'Unknown Controller')
        timestamp = event_data.get('timestamp', '')
        
        # Determine threat level and analysis
        threat_level, confidence, false_positive_prob = self._assess_access_threat_level(
            alarm_name, source, device_id
        )
        
        # Generate recommendations
        recommendations = self._generate_access_recommendations(
            threat_level, alarm_name, source, device_id
        )
        
        # Determine escalation requirements
        escalation_required = threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        
        # Set response timeline
        response_timeline = self._get_response_timeline(threat_level)
        
        # Generate analysis reasoning
        reasoning = self._generate_access_reasoning(
            alarm_name, threat_level, source, device_id, confidence, false_positive_prob
        )
        
        # Calculate priority score (1-10)
        priority_score = self._calculate_access_priority_score(threat_level, confidence, source)
        
        # Generate event summary
        event_summary = f"{alarm_name} - {device_id} ({source})"
        
        return {
            "event_type": "ACCESS_CONTROL",
            "ai_threat_level": threat_level.value,
            "false_positive_probability": false_positive_prob,
            "confidence_score": confidence,
            "recommended_actions": recommendations,
            "escalation_required": escalation_required,
            "response_timeline": response_timeline,
            "analysis_reasoning": reasoning,
            "event_summary": event_summary,
            "priority_score": priority_score
        }
    
    def _assess_access_threat_level(self, alarm_name: str, source: str, device_id: str) -> Tuple[ThreatLevel, float, float]:
        """Assess threat level based on access control alarm characteristics."""
        
        alarm_lower = alarm_name.lower()
        source_lower = source.lower()
        
        # Critical threats - forced entry, duress, security breaches
        critical_indicators = [
            'forced entry', 'duress', 'panic', 'emergency', 'break in', 'tamper',
            'anti-passback violation', 'tailgating', 'unauthorized access attempt'
        ]
        if any(indicator in alarm_lower for indicator in critical_indicators):
            return ThreatLevel.CRITICAL, 0.90, 0.05
        
        # High threats - unauthorized access, invalid credentials
        high_indicators = [
            'door held open', 'invalid card', 'access denied', 'unauthorized',
            'door left open', 'propped open', 'multiple failed attempts'
        ]
        if any(indicator in alarm_lower for indicator in high_indicators):
            return ThreatLevel.HIGH, 0.80, 0.10
        
        # Medium threats - system issues with security implications
        medium_indicators = [
            'door ajar', 'communication lost', 'sensor fault', 'lock failure',
            'battery low', 'time zone violation', 'after hours access'
        ]
        if any(indicator in alarm_lower for indicator in medium_indicators):
            return ThreatLevel.MEDIUM, 0.70, 0.20
        
        # Low threats - routine maintenance, system notifications
        low_indicators = [
            'scheduled maintenance', 'system reboot', 'status update',
            'normal operation', 'periodic check', 'heartbeat'
        ]
        if any(indicator in alarm_lower for indicator in low_indicators):
            return ThreatLevel.LOW, 0.60, 0.35
        
        # Source-based assessment
        if 'sensor' in source_lower or 'contact' in source_lower:
            if 'door' in alarm_lower:
                return ThreatLevel.MEDIUM, 0.75, 0.25
        
        # Default assessment for unknown alarms
        return ThreatLevel.MEDIUM, 0.65, 0.30
    
    def _generate_access_recommendations(self, threat_level: ThreatLevel, alarm_name: str, 
                                       source: str, device_id: str) -> List[str]:
        """Generate specific recommendations based on access control threat assessment."""
        
        recommendations = []
        alarm_lower = alarm_name.lower()
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.extend([
                "IMMEDIATE: Dispatch security to location",
                "IMMEDIATE: Verify building security status",
                "IMMEDIATE: Check for additional security breaches",
                "IMMEDIATE: Consider lockdown if necessary"
            ])
        
        elif threat_level == ThreatLevel.HIGH:
            recommendations.extend([
                "URGENT: Send security to investigate",
                "URGENT: Review access logs for pattern",
                "URGENT: Verify door/lock status",
                "URGENT: Check camera footage if available"
            ])
        
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.extend([
                "PROMPT: Assign maintenance to check system",
                "PROMPT: Monitor for recurring issues",
                "PROMPT: Schedule system diagnostic"
            ])
        
        else:  # LOW
            recommendations.extend([
                "ROUTINE: Log for maintenance review",
                "ROUTINE: Update system status"
            ])
        
        # Add alarm-specific recommendations
        if 'door held open' in alarm_lower:
            recommendations.append("PRIORITY: Check if door is propped open intentionally")
        
        if 'invalid card' in alarm_lower:
            recommendations.append("PRIORITY: Verify user credentials and access rights")
        
        if 'forced entry' in alarm_lower:
            recommendations.append("CRITICAL: Immediate physical security response required")
        
        if 'communication lost' in alarm_lower:
            recommendations.append("TECHNICAL: Check network connectivity to device")
        
        if 'battery low' in alarm_lower:
            recommendations.append("MAINTENANCE: Schedule battery replacement")
        
        if 'sensor fault' in alarm_lower:
            recommendations.append("MAINTENANCE: Inspect and test sensor functionality")
        
        return recommendations
    
    def _get_response_timeline(self, threat_level: ThreatLevel) -> str:
        """Get response timeline based on threat level."""
        timelines = {
            ThreatLevel.CRITICAL: "IMMEDIATE (within 2 minutes)",
            ThreatLevel.HIGH: "URGENT (within 5 minutes)",
            ThreatLevel.MEDIUM: "PROMPT (within 15 minutes)",
            ThreatLevel.LOW: "ROUTINE (within 60 minutes)"
        }
        return timelines.get(threat_level, "ROUTINE (within 60 minutes)")
    
    def _generate_access_reasoning(self, alarm_name: str, threat_level: ThreatLevel, 
                                 source: str, device_id: str, confidence: float, 
                                 false_positive_prob: float) -> str:
        """Generate analysis reasoning for access control event."""
        
        reasoning_parts = [
            f"Access control alarm '{alarm_name}' classified as {threat_level.value} priority",
            f"Device: {device_id}",
            f"Source: {source}",
            f"Confidence: {confidence:.0%}",
            f"False positive probability: {false_positive_prob:.0%}"
        ]
        
        if threat_level == ThreatLevel.CRITICAL:
            reasoning_parts.append("Critical security breach requires immediate response")
        elif threat_level == ThreatLevel.HIGH:
            reasoning_parts.append("High-priority access violation requires urgent investigation")
        elif threat_level == ThreatLevel.MEDIUM:
            reasoning_parts.append("Medium-priority system issue requires prompt attention")
        else:
            reasoning_parts.append("Low-priority system event for routine monitoring")
        
        # Add context about alarm type
        if 'door' in alarm_name.lower():
            reasoning_parts.append("Physical access point security event")
        elif 'card' in alarm_name.lower():
            reasoning_parts.append("Credential-based access event")
        elif 'sensor' in source.lower():
            reasoning_parts.append("Hardware sensor-based event")
        
        return ". ".join(reasoning_parts)
    
    def _calculate_access_priority_score(self, threat_level: ThreatLevel, confidence: float, source: str) -> int:
        """Calculate priority score from 1-10 for access control events."""
        
        base_scores = {
            ThreatLevel.CRITICAL: 9,
            ThreatLevel.HIGH: 7,
            ThreatLevel.MEDIUM: 5,
            ThreatLevel.LOW: 3
        }
        
        score = base_scores.get(threat_level, 3)
        
        # Adjust based on confidence
        if confidence > 0.85:
            score += 1
        elif confidence < 0.65:
            score -= 1
        
        # Adjust based on source criticality
        if any(critical in source.lower() for critical in ['door', 'lock', 'entry', 'exit']):
            score += 1
        elif any(maintenance in source.lower() for maintenance in ['sensor', 'battery', 'communication']):
            score -= 1
        
        return min(max(score, 1), 10)  # Clamp between 1-10