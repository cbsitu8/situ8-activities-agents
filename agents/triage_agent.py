from crewai import Agent, Task, Crew, Process
from agents.tools.cv_analyzer import analyze_cv_threat, CVThreatAnalyzer
from agents.tools.access_analyzer import analyze_access_control, AccessControlAnalyzer
from models.event_models import TriageAnalysis, ThreatLevel
from typing import Dict, Any, List
import os

def create_triage_agent():
    """Create and configure the security triage agent."""
    
    # Define the security triage agent
    triage_agent = Agent(
        role='Security Operations Triage Specialist',
        goal='Analyze and prioritize security events from computer vision and access control systems to provide actionable intelligence for security operations teams.',
        backstory="""You are a seasoned security operations professional with 15+ years of experience in 
        threat assessment and incident response. You have deep expertise in:
        
        - Computer vision threat detection systems and their common false positive patterns
        - Access control system behaviors and failure modes
        - Security incident classification and escalation procedures
        - Risk assessment methodologies for physical security threats
        - Integration between multiple security systems and their data correlation
        
        Your analysis is trusted by security teams to make critical decisions about resource allocation,
        threat response, and escalation procedures. You excel at distinguishing between genuine security
        threats and system anomalies, while ensuring that no critical threats are missed.
        
        You provide clear, actionable recommendations with specific timelines and escalation paths.
        Your assessments include confidence levels and false positive probabilities to help security
        teams make informed decisions under pressure.""",
        tools=[analyze_cv_threat, analyze_access_control],
        verbose=True,
        memory=True,
        allow_delegation=False
    )
    
    return triage_agent

def create_analysis_task(event_data: Dict[str, Any], event_type: str):
    """Create a task for analyzing a security event."""
    
    if event_type == "CV_Threat_Detection":
        task_description = f"""
        Analyze the following computer vision threat detection event and provide a comprehensive triage analysis:
        
        Event Data: {event_data}
        
        Use the CV Threat Analyzer tool to evaluate this event and provide:
        1. Threat level assessment (CRITICAL, HIGH, MEDIUM, LOW)
        2. Confidence score and false positive probability
        3. Specific actionable recommendations with timelines
        4. Escalation requirements
        5. Detailed reasoning for the assessment
        
        Focus on the threat signature, location context, and severity level to make your determination.
        Consider the facility type and location criticality in your assessment.
        """
        
        expected_output = """A comprehensive triage analysis in JSON format containing:
        - event_type: "CV_THREAT"
        - ai_threat_level: threat level classification
        - false_positive_probability: decimal between 0-1
        - confidence_score: decimal between 0-1
        - recommended_actions: list of specific actions with priorities
        - escalation_required: boolean
        - response_timeline: expected response timeframe
        - analysis_reasoning: detailed explanation of assessment
        - event_summary: concise event description
        - priority_score: integer 1-10 scale"""
        
    elif event_type == "Access_Control_System":
        task_description = f"""
        Analyze the following access control system event and provide a comprehensive triage analysis:
        
        Event Data: {event_data}
        
        Use the Access Control Analyzer tool to evaluate this event and provide:
        1. Threat level assessment (CRITICAL, HIGH, MEDIUM, LOW)
        2. Confidence score and false positive probability
        3. Specific actionable recommendations with timelines
        4. Escalation requirements
        5. Detailed reasoning for the assessment
        
        Distinguish between genuine security threats and system maintenance issues.
        Consider the alarm type, device location, and source system in your assessment.
        """
        
        expected_output = """A comprehensive triage analysis in JSON format containing:
        - event_type: "ACCESS_CONTROL"
        - ai_threat_level: threat level classification
        - false_positive_probability: decimal between 0-1
        - confidence_score: decimal between 0-1
        - recommended_actions: list of specific actions with priorities
        - escalation_required: boolean
        - response_timeline: expected response timeframe
        - analysis_reasoning: detailed explanation of assessment
        - event_summary: concise event description
        - priority_score: integer 1-10 scale"""
    
    else:
        raise ValueError(f"Unknown event type: {event_type}")
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=None  # Will be set when creating the crew
    )

def run_triage_analysis(event_data: Dict[str, Any], event_type: str) -> Dict[str, Any]:
    """Run the triage analysis on a security event."""
    
    try:
        if event_type == "CV_Threat_Detection":
            analyzer = CVThreatAnalyzer()
            return analyzer._run(event_data)
        elif event_type == "Access_Control_System":
            analyzer = AccessControlAnalyzer()
            return analyzer._run(event_data)
        else:
            raise ValueError(f"Unknown event type: {event_type}")
            
    except Exception as e:
        # Return error response
        return {
            "event_type": event_type,
            "ai_threat_level": "MEDIUM",
            "false_positive_probability": 0.5,
            "confidence_score": 0.5,
            "recommended_actions": [f"Manual review required - Analysis error: {str(e)}"],
            "escalation_required": True,
            "response_timeline": "URGENT (within 5 minutes)",
            "analysis_reasoning": f"Analysis failed with error: {str(e)}",
            "event_summary": "Security event - analysis error",
            "priority_score": 7
        }

def batch_analyze_events(events: List[Dict[str, Any]], event_types: List[str]) -> List[Dict[str, Any]]:
    """Analyze multiple events in batch."""
    
    results = []
    
    for event_data, event_type in zip(events, event_types):
        try:
            result = run_triage_analysis(event_data, event_type)
            results.append(result)
        except Exception as e:
            # Add error result
            results.append({
                "event_type": event_type,
                "ai_threat_level": "MEDIUM",
                "false_positive_probability": 0.5,
                "confidence_score": 0.5,
                "recommended_actions": [f"Manual review required - Error: {str(e)}"],
                "escalation_required": True,
                "response_timeline": "URGENT (within 5 minutes)",
                "analysis_reasoning": f"Batch analysis failed: {str(e)}",
                "event_summary": "Security event - batch analysis error",
                "priority_score": 7
            })
    
    return results