from crewai.tools import tool
from typing import Dict, Any, List, Tuple
from models.event_models import ThreatLevel, TriageAnalysis
import re

@tool("CV Threat Analyzer")
def analyze_cv_threat(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyzes computer vision threat detection events to assess threat levels, false positive probability, and generate actionable recommendations."""
    
    analyzer = CVThreatAnalyzer()
    return analyzer._run(event_data)

class CVThreatAnalyzer:
    def _run(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a CV threat detection event and return triage analysis."""
        
        # Extract key information from CSV-based model
        threat_name = event_data.get('detection_name', 'Unknown Threat')
        severity = event_data.get('severity', 'UNKNOWN')
        alert_name = event_data.get('detection_name', 'Unknown Alert')
        site_name = event_data.get('site_name', 'Unknown Site')
        camera_name = event_data.get('camera_name', 'Unknown Camera')
        location = f"{site_name} > {camera_name}"
        
        # No icon in CSV data, derive from threat name
        threat_icon = self._derive_threat_icon(threat_name)
        
        # Determine threat level and analysis
        threat_level, confidence, false_positive_prob = self._assess_threat_level(
            threat_name, threat_icon, severity, location
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            threat_level, threat_name, threat_icon, location, site_name
        )
        
        # Determine escalation requirements
        escalation_required = threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
        
        # Set response timeline
        response_timeline = self._get_response_timeline(threat_level)
        
        # Generate analysis reasoning
        reasoning = self._generate_reasoning(
            threat_name, threat_level, location, confidence, false_positive_prob
        )
        
        # Calculate priority score (1-10)
        priority_score = self._calculate_priority_score(threat_level, confidence, location)
        
        # Generate event summary
        event_summary = f"{threat_name} detected at {location} ({site_name})"
        
        return {
            "event_type": "CV_THREAT",
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
    
    def _derive_threat_icon(self, threat_name: str) -> str:
        """Derive threat icon from threat name."""
        threat_lower = threat_name.lower()
        
        if 'firearm' in threat_lower or 'gun' in threat_lower or 'brandishing' in threat_lower:
            return 'GUN'
        elif 'fire' in threat_lower or 'smoke' in threat_lower:
            return 'FIRE'
        elif 'falling' in threat_lower:
            return 'FALL'
        elif 'fence' in threat_lower or 'jumping' in threat_lower:
            return 'FENCE'
        elif 'door' in threat_lower or 'propped' in threat_lower:
            return 'DOOR'
        elif 'tailgating' in threat_lower:
            return 'PERSON'
        else:
            return 'UNKNOWN'
    
    def _assess_threat_level(self, threat_name: str, threat_icon: str, severity: str, location: str) -> Tuple[ThreatLevel, float, float]:
        """Assess threat level based on threat characteristics."""
        
        # Critical threats - weapons and violence
        critical_indicators = ['firearm', 'gun', 'weapon', 'knife', 'violence', 'assault', 'brandishing']
        if any(indicator in threat_name.lower() for indicator in critical_indicators) or threat_icon == 'GUN':
            return ThreatLevel.CRITICAL, 0.95, 0.05
        
        # High threats - unauthorized access, suspicious behavior
        high_indicators = ['unauthorized', 'intrusion', 'trespassing', 'suspicious', 'loitering']
        if any(indicator in threat_name.lower() for indicator in high_indicators):
            return ThreatLevel.HIGH, 0.85, 0.10
        
        # Medium threats - general security concerns
        medium_indicators = ['unattended', 'overcrowding', 'restricted', 'violation']
        if any(indicator in threat_name.lower() for indicator in medium_indicators):
            return ThreatLevel.MEDIUM, 0.75, 0.20
        
        # Severity-based assessment
        if severity == 'SEV0':
            return ThreatLevel.CRITICAL, 0.90, 0.05
        elif severity == 'SEV1':
            return ThreatLevel.HIGH, 0.80, 0.10
        elif severity == 'SEV2':
            return ThreatLevel.MEDIUM, 0.70, 0.20
        else:
            return ThreatLevel.LOW, 0.60, 0.30
    
    def _generate_recommendations(self, threat_level: ThreatLevel, threat_name: str, 
                                threat_icon: str, location: str, site_name: str) -> List[str]:
        """Generate specific recommendations based on threat assessment."""
        
        recommendations = []
        
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.extend([
                "IMMEDIATE: Dispatch security personnel to location",
                "IMMEDIATE: Notify law enforcement if weapon confirmed",
                "IMMEDIATE: Consider lockdown procedures if necessary",
                "IMMEDIATE: Evacuate area if public safety at risk"
            ])
        
        elif threat_level == ThreatLevel.HIGH:
            recommendations.extend([
                "URGENT: Send security to investigate location",
                "URGENT: Review additional camera angles",
                "URGENT: Notify facility management",
                "URGENT: Document incident for investigation"
            ])
        
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.extend([
                "PROMPT: Assign security patrol to area",
                "PROMPT: Monitor situation for escalation",
                "PROMPT: Review security protocols for location"
            ])
        
        else:  # LOW
            recommendations.extend([
                "ROUTINE: Log incident for review",
                "ROUTINE: Monitor for pattern analysis"
            ])
        
        # Add threat-specific recommendations
        if 'firearm' in threat_name.lower() or threat_icon == 'GUN':
            recommendations.append("CRITICAL: Implement active shooter protocols")
        
        if 'restricted' in location.lower() or 'secure' in location.lower():
            recommendations.append("PRIORITY: Verify access authorization")
        
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
    
    def _generate_reasoning(self, threat_name: str, threat_level: ThreatLevel, 
                          location: str, confidence: float, false_positive_prob: float) -> str:
        """Generate analysis reasoning."""
        
        reasoning_parts = [
            f"Threat '{threat_name}' classified as {threat_level.value} priority",
            f"Location: {location}",
            f"Confidence: {confidence:.0%}",
            f"False positive probability: {false_positive_prob:.0%}"
        ]
        
        if threat_level == ThreatLevel.CRITICAL:
            reasoning_parts.append("Critical threat requires immediate response and potential law enforcement notification")
        elif threat_level == ThreatLevel.HIGH:
            reasoning_parts.append("High-priority threat requires urgent security response")
        elif threat_level == ThreatLevel.MEDIUM:
            reasoning_parts.append("Medium-priority threat requires prompt investigation")
        else:
            reasoning_parts.append("Low-priority event for routine monitoring")
        
        return ". ".join(reasoning_parts)
    
    def _calculate_priority_score(self, threat_level: ThreatLevel, confidence: float, location: str) -> int:
        """Calculate priority score from 1-10."""
        
        base_scores = {
            ThreatLevel.CRITICAL: 9,
            ThreatLevel.HIGH: 7,
            ThreatLevel.MEDIUM: 5,
            ThreatLevel.LOW: 3
        }
        
        score = base_scores.get(threat_level, 3)
        
        # Adjust based on confidence
        if confidence > 0.9:
            score += 1
        elif confidence < 0.7:
            score -= 1
        
        # Adjust based on location criticality
        if any(critical in location.lower() for critical in ['entrance', 'exit', 'lobby', 'secure']):
            score += 1
        
        return min(max(score, 1), 10)  # Clamp between 1-10