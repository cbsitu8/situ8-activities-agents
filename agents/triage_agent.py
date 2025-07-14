from crewai import Agent, Task, Crew, Process
from agents.tools.cv_analyzer import analyze_cv_threat, CVThreatAnalyzer
from agents.tools.access_analyzer import analyze_access_control, AccessControlAnalyzer
from agents.tools.sop_search import SOPContextualSearch, get_priority_override, merge_response_requirements
from models.event_models import TriageAnalysis, ThreatLevel
from typing import Dict, Any, List
import os
import json
import logging

logger = logging.getLogger(__name__)

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
        tools=[analyze_cv_threat, analyze_access_control, SOPContextualSearch()],
        verbose=True,
        memory=True,
        allow_delegation=False
    )
    
    return triage_agent

def create_sop_enhanced_triage_agent():
    """Create and configure the SOP-enhanced security triage agent."""
    
    # Define the SOP-enhanced security triage agent
    enhanced_agent = Agent(
        role='SOP-Enhanced Security Operations Triage Specialist',
        goal='Analyze and prioritize security events using both threat assessment and Standard Operating Procedures to determine appropriate priority, response timeline, and required actions.',
        backstory="""You are a senior security operations specialist with comprehensive knowledge 
        of organizational SOPs and procedures. You understand that security events must be evaluated 
        not just for immediate threat level, but also for operational impact, regulatory compliance, 
        and organizational priorities. You always consult relevant SOPs before making final 
        recommendations and can override security-based priorities when SOPs mandate different responses.
        
        You are expert at merging security protocols with operational procedures to create 
        comprehensive response plans that address both security threats and organizational requirements.
        
        CRITICAL ANALYSIS PROCESS:
        1. First perform standard security threat assessment
        2. Search SOP knowledge base for relevant procedures using event context
        3. Apply priority overrides from SOPs when present (e.g., medical emergencies)
        4. Merge security response actions with SOP-mandated procedures
        5. Generate comprehensive response plan with clear reasoning
        
        SOP PRIORITY RULES:
        - SOPs ALWAYS supersede security threat assessment for priority determination
        - Medical emergencies (fall detection, injuries) get HIGH priority regardless of security threat level
        - Regulatory compliance requirements from SOPs must be included in response plan
        - SOP timelines override security-based timelines when more urgent""",
        tools=[analyze_cv_threat, analyze_access_control, SOPContextualSearch()],
        verbose=True,
        memory=True,
        allow_delegation=False
    )
    
    return enhanced_agent

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

def create_sop_aware_triage_task(event_data: Dict[str, Any], event_type: str):
    """Create a task for SOP-enhanced analysis of a security event."""
    
    task_description = f"""
    Analyze the following security event using BOTH threat assessment AND SOP consultation:
    
    Event Type: {event_type}
    Event Data: {json.dumps(event_data, indent=2)}
    
    MANDATORY ANALYSIS PROCESS:
    1. Perform initial security threat assessment using appropriate analyzer tool
    2. Search SOP knowledge base for relevant procedures using event context with SOP Contextual Search tool
    3. Identify any priority overrides or special requirements from SOPs
    4. Determine final priority considering both security risk and SOP requirements
    5. Merge security response actions with SOP-mandated procedures
    6. Generate comprehensive response plan with clear reasoning
    
    CRITICAL REQUIREMENTS:
    - ALWAYS search SOPs before finalizing priority using the SOP Contextual Search tool
    - Apply SOP priority overrides when present (e.g., medical emergencies get HIGH priority)
    - Combine security actions with SOP requirements - do not replace, MERGE them
    - Explain reasoning for any priority adjustments due to SOPs
    - Include regulatory/compliance requirements from SOPs in the response plan
    - SOP requirements OVERRIDE security recommendations when they conflict
    
    EVENT CONTEXT FOR SOP SEARCH:
    Create a descriptive context from the event data that includes:
    - Type of incident (fall, weapon, access violation, etc.)
    - Location information if available
    - Any relevant conditions or circumstances
    
    EXPECTED OUTPUT FORMAT:
    - original_security_analysis: Results from security threat assessment
    - applicable_sops: List of relevant SOPs found with similarity scores
    - sop_priority_override: Priority level mandated by SOPs (if any)
    - final_priority: Final priority determination (security vs SOP priority)
    - merged_response_plan: Combined security + SOP response actions
    - sop_timeline_requirements: Timeline requirements from SOPs
    - regulatory_requirements: Compliance requirements from SOPs
    - escalation_requirements: Combined escalation needs
    - reasoning: Detailed explanation of how SOPs influenced the analysis
    """
    
    expected_output = """A comprehensive SOP-enhanced triage analysis in JSON format containing:
    - event_type: The type of security event analyzed
    - original_security_analysis: Original security threat assessment results
    - applicable_sops: List of relevant SOPs with titles and similarity scores
    - sop_priority_override: Priority override from SOPs (if any)
    - final_threat_level: Final threat level (may be overridden by SOPs)
    - final_priority_score: Final priority score (1-10 scale)
    - merged_response_actions: Combined security and SOP response actions
    - response_timeline: Final response timeline (most urgent from security or SOPs)
    - escalation_required: Boolean indicating if escalation is needed
    - regulatory_requirements: List of compliance requirements from SOPs
    - sop_influence_reasoning: Explanation of how SOPs affected the analysis
    - confidence_score: Confidence in the analysis (0-1)
    - false_positive_probability: Probability this is a false positive (0-1)
    - event_summary: Concise description of the event and response plan"""
    
    return Task(
        description=task_description,
        expected_output=expected_output,
        agent=None  # Will be set when creating the crew
    )

def run_sop_enhanced_analysis(event_data: Dict[str, Any], event_type: str) -> Dict[str, Any]:
    """Run the SOP-enhanced triage analysis on a security event."""
    
    try:
        logger.info(f"Running SOP-enhanced analysis for {event_type}")
        
        # Create the enhanced agent and task
        enhanced_agent = create_sop_enhanced_triage_agent()
        analysis_task = create_sop_aware_triage_task(event_data, event_type)
        analysis_task.agent = enhanced_agent
        
        # Create and run the crew
        crew = Crew(
            agents=[enhanced_agent],
            tasks=[analysis_task],
            verbose=True,
            process=Process.sequential
        )
        
        # Execute the analysis
        result = crew.kickoff()
        
        # Try to parse the result as JSON, fallback to structured format
        try:
            # Handle CrewAI CrewOutput object
            result_str = str(result)
            if "```json" in result_str:
                # Extract JSON from markdown code block
                start = result_str.find("```json") + 7
                end = result_str.find("```", start)
                json_text = result_str[start:end].strip()
                parsed_result = json.loads(json_text)
            elif isinstance(result, str):
                parsed_result = json.loads(result)
            else:
                # Try to extract JSON from the result object
                result_str = str(result)
                # Look for JSON pattern in the string
                import re
                json_match = re.search(r'\{[\s\S]*\}', result_str)
                if json_match:
                    parsed_result = json.loads(json_match.group())
                else:
                    raise json.JSONDecodeError("No JSON found", result_str, 0)
        except (json.JSONDecodeError, AttributeError, TypeError):
            # If JSON parsing fails, create a structured response
            parsed_result = {
                "event_type": event_type,
                "analysis_result": str(result),
                "final_threat_level": "MEDIUM",
                "final_priority_score": 6,
                "response_timeline": "15 minutes",
                "escalation_required": True,
                "merged_response_actions": ["Manual review of SOP-enhanced analysis required"],
                "confidence_score": 0.7,
                "false_positive_probability": 0.3,
                "event_summary": f"SOP-enhanced analysis completed for {event_type}",
                "sop_influence_reasoning": "Analysis completed with SOP consultation"
            }
        
        logger.info(f"SOP-enhanced analysis completed for {event_type}")
        return parsed_result
        
    except Exception as e:
        logger.error(f"Error in SOP-enhanced analysis for {event_type}: {e}")
        # Return error response in expected format
        return {
            "event_type": event_type,
            "final_threat_level": "MEDIUM",
            "final_priority_score": 7,
            "confidence_score": 0.5,
            "false_positive_probability": 0.5,
            "merged_response_actions": [f"Manual review required - SOP-enhanced analysis error: {str(e)}"],
            "escalation_required": True,
            "response_timeline": "URGENT (within 5 minutes)",
            "sop_influence_reasoning": f"SOP-enhanced analysis failed: {str(e)}",
            "event_summary": f"Security event - SOP-enhanced analysis error for {event_type}",
            "regulatory_requirements": [],
            "applicable_sops": []
        }