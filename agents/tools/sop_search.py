"""
SOP Contextual Search Tool for CrewAI Integration

This tool provides semantic search capabilities over the SOP knowledge base,
allowing the enhanced triage agent to consult relevant Standard Operating
Procedures when analyzing security events.
"""

from crewai.tools import BaseTool
from typing import Any, Optional, Type
from pydantic import BaseModel, Field
import json
import sqlite3
import logging
import os

logger = logging.getLogger(__name__)
# Enable debug logging for this specific module
logger.setLevel(logging.DEBUG)


class SOPSearchInput(BaseModel):
    """Input schema for SOP contextual search."""
    event_context: str = Field(
        description="Description of the security event or context to search SOPs for"
    )
    category_filter: Optional[str] = Field(
        default=None,
        description="Optional category filter (e.g., 'medical_emergency', 'security_incident')"
    )
    max_results: int = Field(
        default=3,
        description="Maximum number of relevant SOPs to return"
    )


class SOPContextualSearch(BaseTool):
    """
    Search SOP knowledge base for relevant procedures based on event context.
    
    This tool uses semantic similarity to find SOPs that match the given
    security event context, helping the triage agent understand what
    organizational procedures should be followed.
    """
    
    name: str = "SOP Contextual Search"
    description: str = (
        "Search the Standard Operating Procedures (SOP) knowledge base for relevant "
        "procedures based on security event context. Returns SOPs with their "
        "priority overrides, response requirements, and applicable conditions."
    )
    args_schema: Type[BaseModel] = SOPSearchInput
    db_path: str = os.path.abspath(os.getenv('SOP_DATABASE_PATH', './sop_knowledge_base.db'))
    
    def validate_database_connection(self) -> tuple[bool, str]:
        """Validate database connection and content."""
        try:
            if not os.path.exists(self.db_path):
                return False, f"Database file does not exist: {self.db_path}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if sops table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sops'")
            if not cursor.fetchone():
                conn.close()
                return False, "SOPs table does not exist in database"
            
            # Check if there are any SOPs
            cursor.execute("SELECT COUNT(*) FROM sops")
            count = cursor.fetchone()[0]
            conn.close()
            
            if count == 0:
                return False, f"Database exists but contains no SOPs (count: {count})"
            
            logger.info(f"Database validation successful: {count} SOPs found at {self.db_path}")
            return True, f"Database valid with {count} SOPs"
            
        except Exception as e:
            logger.error(f"Database validation failed: {e}")
            return False, f"Database validation error: {str(e)}"
        
    def _run(self, event_context: str, category_filter: Optional[str] = None, max_results: int = 3) -> str:
        """
        Search for relevant SOPs using event context.
        
        Args:
            event_context: Description of the security event
            category_filter: Optional category to filter by
            max_results: Maximum number of SOPs to return
            
        Returns:
            JSON string with relevant SOPs and their requirements
        """
        try:
            logger.info(f"Searching SOPs for context: {event_context[:100]}...")
            
            # Validate database first
            db_valid, db_message = self.validate_database_connection()
            if not db_valid:
                logger.error(f"Database validation failed: {db_message}")
                return json.dumps({
                    "relevant_sops": [],
                    "error": db_message,
                    "database_path": self.db_path
                })
            
            # Connect to SOP database
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Build search query
            if category_filter:
                query = """
                SELECT data as sop_data, searchable_text as search_text 
                FROM sops 
                WHERE category = ? 
                ORDER BY sop_id DESC
                """
                cursor.execute(query, (category_filter,))
            else:
                query = """
                SELECT data as sop_data, searchable_text as search_text 
                FROM sops 
                ORDER BY sop_id DESC
                """
                cursor.execute(query)
            
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                logger.warning("No SOPs found in database")
                return json.dumps({
                    "relevant_sops": [],
                    "message": "No SOPs found in knowledge base"
                })
            
            logger.info(f"Found {len(rows)} SOPs in database for processing")
            
            # Simple text-based matching (in production, use vector embeddings)
            relevant_sops = []
            event_keywords = event_context.lower().split()
            logger.info(f"Searching for keywords: {event_keywords}")
            
            for row in rows:
                try:
                    sop_data = json.loads(row['sop_data'])
                    search_text = row['search_text'].lower()
                    
                    logger.debug(f"Processing SOP: {sop_data.get('title', 'Unknown')} with triggers: {sop_data.get('triggers', [])}")
                    
                    # Calculate relevance score based on keyword matches
                    score = 0
                    matched_triggers = []
                    
                    # Check triggers with more flexible matching
                    for trigger in sop_data.get('triggers', []):
                        trigger_lower = trigger.lower()
                        for keyword in event_keywords:
                            if keyword in trigger_lower:
                                score += 2
                                if trigger not in matched_triggers:
                                    matched_triggers.append(trigger)
                                logger.debug(f"Keyword '{keyword}' matched trigger '{trigger}' - score: {score}")
                    
                    # Check title and category
                    title_matches = sum(1 for keyword in event_keywords 
                                       if keyword in sop_data.get('title', '').lower())
                    score += title_matches
                    
                    # Check search text
                    search_matches = sum(1 for keyword in event_keywords 
                                        if keyword in search_text)
                    score += search_matches * 0.5
                    
                    logger.debug(f"SOP '{sop_data.get('title')}': title_matches={title_matches}, search_matches={search_matches}, total_score={score}")
                    
                    # Lower threshold to be more inclusive
                    if score > 0:
                        similarity_score = min(score / len(event_keywords), 1.0)
                        
                        relevant_sop = {
                            "sop_id": sop_data.get('sop_id'),
                            "title": sop_data.get('title'),
                            "category": sop_data.get('category'),
                            "priority_override": sop_data.get('priority_override'),
                            "response_requirements": sop_data.get('response_requirements'),
                            "special_conditions": sop_data.get('special_conditions'),
                            "regulatory_requirements": sop_data.get('regulatory_requirements', []),
                            "similarity_score": similarity_score,
                            "matched_triggers": matched_triggers,
                            "triggers": sop_data.get('triggers', [])
                        }
                        relevant_sops.append(relevant_sop)
                        logger.info(f"Added relevant SOP: {sop_data.get('title')} with score {similarity_score}")
                    else:
                        logger.debug(f"SOP '{sop_data.get('title')}' rejected with score {score}")
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing SOP data: {e}")
                    continue
            
            # Sort by similarity score and limit results
            relevant_sops.sort(key=lambda x: x['similarity_score'], reverse=True)
            relevant_sops = relevant_sops[:max_results]
            
            result = {
                "relevant_sops": relevant_sops,
                "search_context": event_context,
                "total_found": len(relevant_sops)
            }
            
            logger.info(f"Found {len(relevant_sops)} relevant SOPs")
            return json.dumps(result, indent=2)
            
        except sqlite3.Error as e:
            logger.error(f"Database error in SOP search: {e}")
            return json.dumps({
                "relevant_sops": [],
                "error": f"Database error: {str(e)}"
            })
        except Exception as e:
            logger.error(f"Error in SOP contextual search: {e}")
            return json.dumps({
                "relevant_sops": [],
                "error": f"Search error: {str(e)}"
            })


def search_sops_for_event(event_context: str, category_filter: Optional[str] = None) -> dict:
    """
    Convenience function to search SOPs for a given event context.
    
    Args:
        event_context: Description of the security event
        category_filter: Optional category filter
        
    Returns:
        Dictionary with relevant SOPs
    """
    search_tool = SOPContextualSearch()
    result_json = search_tool._run(event_context, category_filter)
    return json.loads(result_json)


def get_priority_override(relevant_sops: list) -> Optional[str]:
    """
    Extract the highest priority override from relevant SOPs.
    
    Args:
        relevant_sops: List of relevant SOP objects
        
    Returns:
        Highest priority override or None
    """
    priority_levels = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }
    
    highest_priority = None
    highest_value = 0
    
    for sop in relevant_sops:
        priority = sop.get('priority_override')
        if priority and priority in priority_levels:
            value = priority_levels[priority]
            if value > highest_value:
                highest_value = value
                highest_priority = priority
    
    return highest_priority


def merge_response_requirements(relevant_sops: list) -> dict:
    """
    Merge response requirements from multiple relevant SOPs.
    
    Args:
        relevant_sops: List of relevant SOP objects
        
    Returns:
        Combined response requirements
    """
    merged_requirements = {
        "timeline": None,
        "notifications": set(),
        "required_actions": [],
        "escalation_required": False
    }
    
    # Find the most urgent timeline
    timeline_urgency = {
        "IMMEDIATE": 5,
        "URGENT (within 1 minute)": 4,
        "URGENT (within 2 minutes)": 4,
        "URGENT (within 5 minutes)": 3,
        "15 minutes": 2,
        "30 minutes": 1
    }
    
    most_urgent_score = 0
    
    for sop in relevant_sops:
        requirements = sop.get('response_requirements', {})
        
        # Handle timeline
        timeline = requirements.get('timeline')
        if timeline:
            score = 0
            for key, value in timeline_urgency.items():
                if key.lower() in timeline.lower():
                    score = value
                    break
            
            if score > most_urgent_score:
                most_urgent_score = score
                merged_requirements['timeline'] = timeline
        
        # Collect notifications
        notifications = requirements.get('notifications', [])
        merged_requirements['notifications'].update(notifications)
        
        # Collect required actions
        actions = requirements.get('required_actions', [])
        merged_requirements['required_actions'].extend(actions)
        
        # Set escalation if any SOP requires it
        if requirements.get('escalation_required'):
            merged_requirements['escalation_required'] = True
    
    # Convert set back to list for JSON serialization
    merged_requirements['notifications'] = list(merged_requirements['notifications'])
    
    return merged_requirements