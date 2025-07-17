"""
Analysis tools for agents
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class AnalysisTools:
    """
    Analysis utility tools for agents
    """
    
    @staticmethod
    def calculate_time_correlation(
        incident_time: datetime,
        badge_events: List[Dict[str, Any]],
        max_time_window: int = 60
    ) -> Dict[str, Any]:
        """
        Calculate time correlation between incident and badge events
        
        Args:
            incident_time: Time of the incident
            badge_events: List of badge events
            max_time_window: Maximum time window in seconds
        
        Returns:
            Time correlation analysis
        """
        try:
            correlations = []
            
            for event in badge_events:
                event_time = datetime.fromisoformat(event["timestamp"])
                time_diff = (incident_time - event_time).total_seconds()
                
                # Only consider events within the time window
                if abs(time_diff) <= max_time_window:
                    correlation_strength = 1.0 - (abs(time_diff) / max_time_window)
                    
                    correlations.append({
                        "event_id": event["event_id"],
                        "badge_id": event["badge_id"],
                        "employee_name": event["employee_name"],
                        "time_difference": time_diff,
                        "correlation_strength": correlation_strength,
                        "timing_category": AnalysisTools._categorize_timing(time_diff)
                    })
            
            # Sort by correlation strength
            correlations.sort(key=lambda x: x["correlation_strength"], reverse=True)
            
            return {
                "total_events": len(badge_events),
                "correlated_events": len(correlations),
                "strongest_correlation": correlations[0] if correlations else None,
                "all_correlations": correlations
            }
            
        except Exception as e:
            logger.error(f"Error calculating time correlation: {e}")
            return {
                "total_events": 0,
                "correlated_events": 0,
                "strongest_correlation": None,
                "all_correlations": []
            }
    
    @staticmethod
    def _categorize_timing(time_diff: float) -> str:
        """
        Categorize timing relationship
        
        Args:
            time_diff: Time difference in seconds (negative = before incident)
        
        Returns:
            Timing category
        """
        if time_diff < -10:
            return "well_before"
        elif -10 <= time_diff < -2:
            return "shortly_before"
        elif -2 <= time_diff <= 2:
            return "simultaneous"
        elif 2 < time_diff <= 10:
            return "shortly_after"
        else:
            return "well_after"
    
    @staticmethod
    def assess_risk_level(
        correlation_data: Dict[str, Any],
        employee_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Assess risk level based on correlation and employee data
        
        Args:
            correlation_data: Time correlation analysis
            employee_data: Employee information
        
        Returns:
            Risk assessment
        """
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check for inactive employees
            for emp in employee_data:
                if not emp.get("active", True):
                    risk_factors.append(f"Inactive employee {emp['employee_name']} involved")
                    risk_score += 0.8
            
            # Check timing patterns
            correlations = correlation_data.get("all_correlations", [])
            
            if not correlations:
                risk_factors.append("No badge access found around incident time")
                risk_score += 0.6
            else:
                # Analyze timing patterns
                for corr in correlations:
                    timing = corr["timing_category"]
                    
                    if timing == "simultaneous":
                        risk_factors.append(f"Simultaneous badge access by {corr['employee_name']}")
                        risk_score += 0.2
                    elif timing == "shortly_before":
                        risk_factors.append(f"Badge access shortly before incident by {corr['employee_name']}")
                        risk_score += 0.4
                    elif timing == "well_before":
                        risk_factors.append(f"Badge access well before incident by {corr['employee_name']}")
                        risk_score += 0.1
            
            # Determine risk level
            if risk_score >= 0.8:
                risk_level = "Critical"
            elif risk_score >= 0.6:
                risk_level = "High"
            elif risk_score >= 0.4:
                risk_level = "Medium"
            else:
                risk_level = "Low"
            
            return {
                "risk_level": risk_level,
                "risk_score": min(risk_score, 1.0),
                "risk_factors": risk_factors,
                "confidence": min(risk_score * 0.9, 0.95)
            }
            
        except Exception as e:
            logger.error(f"Error assessing risk level: {e}")
            return {
                "risk_level": "Unknown",
                "risk_score": 0.0,
                "risk_factors": ["Analysis error"],
                "confidence": 0.0
            }
    
    @staticmethod
    def generate_summary(
        incident_data: Dict[str, Any],
        correlation_analysis: Dict[str, Any],
        risk_assessment: Dict[str, Any]
    ) -> str:
        """
        Generate analysis summary
        
        Args:
            incident_data: Incident information
            correlation_analysis: Time correlation analysis
            risk_assessment: Risk assessment results
        
        Returns:
            Analysis summary text
        """
        try:
            summary_parts = []
            
            # Incident overview
            summary_parts.append(f"Tailgating incident detected at {incident_data.get('location', 'Unknown location')}")
            summary_parts.append(f"Incident time: {incident_data.get('timestamp', 'Unknown time')}")
            
            # Correlation findings
            corr_count = correlation_analysis.get("correlated_events", 0)
            if corr_count > 0:
                summary_parts.append(f"Found {corr_count} badge access events in correlation window")
                
                strongest = correlation_analysis.get("strongest_correlation")
                if strongest:
                    summary_parts.append(f"Strongest correlation: {strongest['employee_name']} (strength: {strongest['correlation_strength']:.2f})")
            else:
                summary_parts.append("No badge access events found in correlation window")
            
            # Risk assessment
            risk_level = risk_assessment.get("risk_level", "Unknown")
            risk_score = risk_assessment.get("risk_score", 0.0)
            summary_parts.append(f"Risk Level: {risk_level} (score: {risk_score:.2f})")
            
            # Risk factors
            risk_factors = risk_assessment.get("risk_factors", [])
            if risk_factors:
                summary_parts.append("Risk factors identified:")
                for factor in risk_factors:
                    summary_parts.append(f"- {factor}")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Error generating analysis summary"
    
    @staticmethod
    def format_for_storage(
        event_id: int,
        correlation_id: str,
        analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format analysis data for database storage
        
        Args:
            event_id: Event ID
            correlation_id: Correlation ID
            analysis_data: Analysis results
        
        Returns:
            Formatted data for storage
        """
        try:
            return {
                "tailgating_event_id": event_id,
                "correlation_id": correlation_id,
                "correlated_badge_events": analysis_data.get("correlation_analysis", {}).get("all_correlations", []),
                "analysis_summary": analysis_data.get("summary", ""),
                "confidence_score": analysis_data.get("risk_assessment", {}).get("confidence", 0.0),
                "risk_level": analysis_data.get("risk_assessment", {}).get("risk_level", "Unknown"),
                "agent_analysis": {
                    "time_correlation": analysis_data.get("correlation_analysis", {}),
                    "risk_assessment": analysis_data.get("risk_assessment", {}),
                    "processed_at": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error formatting data for storage: {e}")
            return {
                "tailgating_event_id": event_id,
                "correlation_id": correlation_id,
                "correlated_badge_events": [],
                "analysis_summary": "Error processing analysis",
                "confidence_score": 0.0,
                "risk_level": "Unknown",
                "agent_analysis": {}
            }