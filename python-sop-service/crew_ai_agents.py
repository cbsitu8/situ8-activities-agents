"""
CrewAI Badge Correlator Agents for Tailgating Threat Analysis
"""

import os
import uuid
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
from database_new import SessionLocal, Event, BadgeHolder, ThreatCorrelation
import logging

logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not set. CrewAI agents will not function properly.")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7) if OPENAI_API_KEY else None

# Custom Tools for Database Operations

@tool
def query_badge_events(location: str, timestamp_str: str, time_window_seconds: int = 30) -> str:
    """
    Query badge access events within a time window around a tailgating incident.
    
    Args:
        location: Location where tailgating occurred
        timestamp_str: Timestamp of tailgating event (ISO format)
        time_window_seconds: Time window in seconds to search (default 30)
    
    Returns:
        JSON string of badge events found
    """
    try:
        db = SessionLocal()
        
        # Parse the timestamp
        incident_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # Create time window
        start_time = incident_time - timedelta(seconds=time_window_seconds)
        end_time = incident_time + timedelta(seconds=time_window_seconds)
        
        # Query badge events in the time window and location
        badge_events = db.query(Event).join(BadgeHolder).filter(
            Event.source == "access_control",
            Event.location == location,
            Event.timestamp >= start_time,
            Event.timestamp <= end_time,
            Event.badge_id.isnot(None)
        ).all()
        
        # Format results
        results = []
        for event in badge_events:
            time_diff = (incident_time - event.timestamp).total_seconds()
            results.append({
                "event_id": event.id,
                "badge_id": event.badge_id,
                "employee_name": event.badge_holder.employee_name if event.badge_holder else "Unknown",
                "department": event.badge_holder.department if event.badge_holder else "Unknown",
                "access_level": event.badge_holder.access_level if event.badge_holder else "Unknown",
                "event_type": event.event_type,
                "timestamp": event.timestamp.isoformat(),
                "time_difference_seconds": round(time_diff, 2),
                "location": event.location,
                "severity": event.severity
            })
        
        db.close()
        return json.dumps({
            "found_events": len(results),
            "search_window": f"{time_window_seconds} seconds",
            "incident_location": location,
            "incident_time": timestamp_str,
            "badge_events": results
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Error querying badge events: {e}")
        return json.dumps({"error": str(e), "found_events": 0, "badge_events": []})

@tool
def get_employee_details(badge_id: str) -> str:
    """
    Get detailed employee information for a badge ID.
    
    Args:
        badge_id: The badge ID to look up
    
    Returns:
        JSON string with employee details
    """
    try:
        db = SessionLocal()
        
        badge_holder = db.query(BadgeHolder).filter(BadgeHolder.badge_id == badge_id).first()
        
        if badge_holder:
            result = {
                "badge_id": badge_holder.badge_id,
                "employee_name": badge_holder.employee_name,
                "department": badge_holder.department,
                "access_level": badge_holder.access_level,
                "active": badge_holder.active,
                "hire_date": badge_holder.created_at.isoformat()
            }
        else:
            result = {
                "badge_id": badge_id,
                "employee_name": "Unknown",
                "department": "Unknown",
                "access_level": "Unknown",
                "active": False,
                "error": "Badge ID not found in directory"
            }
        
        db.close()
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error getting employee details: {e}")
        return json.dumps({"error": str(e), "badge_id": badge_id})

@tool
def store_correlation_analysis(correlation_data: str) -> str:
    """
    Store the correlation analysis results in the database.
    
    Args:
        correlation_data: JSON string containing correlation analysis
    
    Returns:
        Correlation ID if successful
    """
    try:
        db = SessionLocal()
        data = json.loads(correlation_data)
        
        correlation = ThreatCorrelation(
            correlation_id=str(uuid.uuid4()),
            tailgating_event_id=data["tailgating_event_id"],
            correlated_badge_events=data.get("correlated_badge_events", []),
            analysis_summary=data["analysis_summary"],
            confidence_score=data["confidence_score"],
            risk_level=data["risk_level"],
            agent_analysis=data.get("agent_analysis", {})
        )
        
        db.add(correlation)
        db.commit()
        
        correlation_id = correlation.correlation_id
        db.close()
        
        return correlation_id
        
    except Exception as e:
        logger.error(f"Error storing correlation analysis: {e}")
        return f"ERROR: {str(e)}"

# CrewAI Agents

def create_incident_coordinator():
    """Create the Incident Coordinator Agent"""
    return Agent(
        role="Security Incident Coordinator",
        goal="Parse tailgating alerts and extract critical correlation data including timestamp, location, and camera information",
        backstory="""You are an experienced security operations specialist who has spent years 
        managing incident response workflows. You excel at quickly parsing security alerts and 
        extracting the essential information needed for further analysis. Your role is crucial 
        as the first step in the correlation process.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_badge_query_agent():
    """Create the Badge Log Query Agent"""
    return Agent(
        role="Access Control Data Analyst",
        goal="Query badge access logs within time windows around security incidents to find potential correlations",
        backstory="""You are a data analyst specializing in access control systems. You have deep 
        expertise in correlating security events with badge access patterns. You understand the 
        importance of timing analysis and can quickly identify suspicious access patterns that 
        might be related to security incidents.""",
        verbose=True,
        allow_delegation=False,
        tools=[query_badge_events, get_employee_details],
        llm=llm
    )

def create_report_generator():
    """Create the Report Generator Agent"""
    return Agent(
        role="Security Intelligence Analyst",
        goal="Generate comprehensive incident correlation reports with clear conclusions and risk assessments",
        backstory="""You are a senior security analyst with expertise in threat intelligence and 
        incident analysis. You excel at synthesizing complex security data into clear, actionable 
        reports. Your analyses help security teams understand the full context of incidents and 
        make informed decisions about response actions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_notification_agent():
    """Create the Notification Agent"""
    return Agent(
        role="Security Operations Communicator",
        goal="Format and deliver actionable security intelligence to threat management systems",
        backstory="""You are a security operations specialist focused on effective communication 
        of threat intelligence. You understand how to present complex security analysis in a 
        format that enables rapid decision-making by security teams. Your communications are 
        precise, actionable, and properly prioritized.""",
        verbose=True,
        allow_delegation=False,
        tools=[store_correlation_analysis],
        llm=llm
    )

# CrewAI Tasks

def create_coordinator_task(tailgating_event_data: Dict[str, Any]):
    """Create task for Incident Coordinator"""
    return Task(
        description=f"""
        Parse the following tailgating security alert and extract key information:
        
        Event Data: {json.dumps(tailgating_event_data, indent=2)}
        
        Extract and clearly identify:
        1. Event timestamp (exact time)
        2. Location/door where tailgating occurred
        3. Camera or sensor ID
        4. Severity level
        5. Any additional metadata
        
        Format your output as a structured summary that the next agent can easily process.
        """,
        agent=create_incident_coordinator(),
        expected_output="Structured summary of tailgating event with timestamp, location, and key details"
    )

def create_query_task():
    """Create task for Badge Query Agent"""
    return Task(
        description="""
        Using the tailgating event information from the Incident Coordinator, search for badge 
        access events that occurred around the same time and location.
        
        1. Use the query_badge_events tool to search for access events within 30 seconds
        2. Focus on the same location as the tailgating incident
        3. For any badge IDs found, use get_employee_details to get complete employee information
        4. Analyze the timing relationships between badge access and tailgating
        
        Look for patterns such as:
        - Badge access immediately before tailgating (potential follower scenario)
        - Use of the same badge within a 60 mins time window (potential pass-back)
        - Multiple badge accesses around the same time
        - Unusual access patterns for the location/time
        
        Provide a detailed summary of all badge events found and their potential relevance.
        """,
        agent=create_badge_query_agent(),
        expected_output="Detailed list of badge access events with employee information and timing analysis"
    )

def create_analysis_task(tailgating_event_id: int):
    """Create task for Report Generator"""
    return Task(
        description=f"""
        Analyze the correlation between the tailgating event and any badge access events found.
        
        Tailgating Event ID: {tailgating_event_id}
        
        Based on the incident details and badge query results:
        
        1. Determine if there's a credible correlation between badge access and tailgating
        2. Assess the confidence level of the correlation (0.0 to 1.0)
        3. Determine risk level: Critical, High, Medium, or Low using these guidelines:
           
           **Critical Risk:**
           - Inactive/terminated employee badge used close to the tailgating event
           - Multiple unauthorized people detected
           - Tailgating at high-security areas
           
           **High Risk:**
           - No badge access found within 5 seconds before or after the tailgating event (unauthorized entry without credentials)
           - Active employee followed by unauthorized person (classic tailgating)
           
           **Medium Risk:**
           - Longer time gaps (5+ seconds before and after the tailgating event) between badge and tailgating
           - Badge access 5 seconds after tailgating (possible same person or event was delayed)
           - Same badge used within 60 mins time window (anti pass-back)
           
           **Low Risk:**
           - Badge access immediately after tailgating by same person
           - False positive scenarios
        
        4. Provide a clear analysis summary explaining:
           - What likely happened
           - Who was involved (if identified)
           - The timeline of events
           - Potential security implications
        
        Consider factors like:
        - Timing proximity (closer = higher confidence)
        - Location match (exact location = higher confidence)
        - Employee access level vs. area accessed
        - Employee active status (terminated employees = critical risk)
        - Pattern consistency with normal behavior
        
        Generate a comprehensive threat assessment.
        """,
        agent=create_report_generator(),
        expected_output="Threat assessment with confidence score, risk level, and detailed analysis summary"
    )

def create_notification_task():
    """Create task for Notification Agent"""
    return Task(
        description="""
        Format the correlation analysis for storage and operational use.
        
        Based on the complete analysis from previous agents:
        
        1. Create a structured correlation record
        2. Include all relevant event details and employee information
        3. Format the analysis for easy consumption by security operations
        4. Use the store_correlation_analysis tool to save the results
        5. Provide a final summary for immediate action
        
        The output should be ready for security team review and potential investigation.
        """,
        agent=create_notification_agent(),
        expected_output="Stored correlation analysis with confirmation ID and operational summary"
    )

# Main Correlation Workflow

class TailgatingCorrelationCrew:
    """Main CrewAI crew for tailgating badge correlation analysis"""
    
    def __init__(self):
        self.coordinator = create_incident_coordinator()
        self.badge_analyst = create_badge_query_agent()
        self.report_generator = create_report_generator()
        self.notifier = create_notification_agent()
    
    def analyze_tailgating_event(self, tailgating_event_data: Dict[str, Any], event_id: int) -> Dict[str, Any]:
        """
        Run the complete correlation analysis for a tailgating event
        
        Args:
            tailgating_event_data: Dictionary containing tailgating event details
            event_id: Database ID of the tailgating event
        
        Returns:
            Dictionary containing correlation analysis results
        """
        try:
            # Create tasks
            coordinator_task = create_coordinator_task(tailgating_event_data)
            query_task = create_query_task()
            analysis_task = create_analysis_task(event_id)
            notification_task = create_notification_task()
            
            # Create crew
            crew = Crew(
                agents=[self.coordinator, self.badge_analyst, self.report_generator, self.notifier],
                tasks=[coordinator_task, query_task, analysis_task, notification_task],
                process=Process.sequential,
                verbose=True
            )
            
            # Execute the workflow
            logger.info(f"Starting CrewAI analysis for tailgating event {event_id}")
            result = crew.kickoff()
            
            # Parse the result to extract correlation ID
            correlation_id = None
            if isinstance(result, str) and "correlation_id" in result.lower():
                # Extract correlation ID from the result
                lines = result.split('\n')
                for line in lines:
                    if 'correlation_id' in line.lower() or line.strip().startswith('CORR-'):
                        correlation_id = line.strip()
                        break
            
            return {
                "success": True,
                "correlation_id": correlation_id,
                "analysis_result": str(result),
                "event_id": event_id
            }
            
        except Exception as e:
            logger.error(f"Error in CrewAI analysis: {e}")
            return {
                "success": False,
                "error": str(e),
                "event_id": event_id
            }

# Utility function to initialize the correlation system
def initialize_correlation_system():
    """Initialize the correlation system and check dependencies"""
    try:
        if not OPENAI_API_KEY:
            logger.error("OPENAI_API_KEY not configured. CrewAI agents cannot function.")
            return False
        
        # Test database connection
        db = SessionLocal()
        db.close()
        
        logger.info("CrewAI correlation system initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize correlation system: {e}")
        return False