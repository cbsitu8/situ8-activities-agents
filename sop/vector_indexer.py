import json
import logging
import os
from typing import List, Dict, Any, Optional
from sop.models import ProcessedSOP, SOPSearchResult

# Use simple in-memory storage instead of vector database for testing
import sqlite3
import hashlib

logger = logging.getLogger(__name__)

class VectorIndexer:
    """Simple SQLite-based storage for SOPs without vector embeddings for testing"""
    
    def __init__(self, db_path: str = "./sop_knowledge_base.db"):
        try:
            # Initialize SQLite database
            self.db_path = db_path
            os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
            
            # Create database and table
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS sops (
                    sop_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    title TEXT,
                    category TEXT,
                    priority_override TEXT,
                    document_source TEXT,
                    processed_date TEXT,
                    searchable_text TEXT
                )
            ''')
            self.conn.commit()
            
            logger.info(f"Vector indexer initialized with SQLite database at {db_path}")
            
        except Exception as e:
            logger.error(f"Error initializing vector indexer: {str(e)}")
            raise
    
    def index_sop(self, sop: ProcessedSOP) -> tuple[bool, Optional[str]]:
        """
        Store SOP in SQLite database
        
        Args:
            sop: ProcessedSOP object to index
            
        Returns:
            Tuple of (success, error_message)
        """
        try:
            logger.info(f"Indexing SOP: {sop.sop_id}")
            
            # Create searchable text combining key fields
            searchable_text = self._create_searchable_text(sop)
            
            # Store in SQLite
            self.conn.execute('''
                INSERT OR REPLACE INTO sops 
                (sop_id, data, title, category, priority_override, document_source, processed_date, searchable_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                sop.sop_id,
                sop.model_dump_json(),
                sop.title,
                sop.category,
                sop.priority_override,
                sop.document_source,
                sop.processed_date.isoformat(),
                searchable_text
            ))
            self.conn.commit()
            
            logger.info(f"Successfully indexed SOP {sop.sop_id} in database")
            return True, None
            
        except Exception as e:
            logger.error(f"Error indexing SOP {sop.sop_id}: {str(e)}")
            return False, f"Error indexing SOP: {str(e)}"
    
    def search_sops(self, query: str, n_results: int = 3, similarity_threshold: float = 0.7) -> List[SOPSearchResult]:
        """
        Search for relevant SOPs using text matching
        
        Args:
            query: Search query (event description, keywords, etc.)
            n_results: Maximum number of results to return
            similarity_threshold: Minimum similarity score to include result
            
        Returns:
            List of SOPSearchResult objects
        """
        try:
            logger.info(f"Searching SOPs for query: '{query}'")
            
            # Simple text search in SQLite
            cursor = self.conn.execute('''
                SELECT sop_id, data, title, category, priority_override, searchable_text
                FROM sops 
                WHERE searchable_text LIKE ? 
                ORDER BY 
                    CASE 
                        WHEN title LIKE ? THEN 1
                        WHEN category LIKE ? THEN 2
                        ELSE 3
                    END
                LIMIT ?
            ''', (f'%{query}%', f'%{query}%', f'%{query}%', n_results))
            
            search_results = []
            
            for row in cursor.fetchall():
                try:
                    sop_id, data_json, title, category, priority_override, searchable_text = row
                    
                    # Parse stored SOP data
                    sop_data = json.loads(data_json)
                    
                    # Simple similarity score based on keyword matches
                    query_words = query.lower().split()
                    searchable_lower = searchable_text.lower()
                    matches = sum(1 for word in query_words if word in searchable_lower)
                    similarity_score = min(1.0, matches / max(1, len(query_words)))
                    
                    if similarity_score < 0.1:  # Lower threshold for text search
                        continue
                    
                    # Extract matched triggers
                    triggers = sop_data.get('triggers', [])
                    matched_triggers = self._find_matched_triggers(query.lower(), triggers)
                    
                    # Create search result
                    search_result = SOPSearchResult(
                        sop_id=sop_id,
                        title=title,
                        similarity_score=round(similarity_score, 3),
                        priority_override=priority_override,
                        response_requirements=sop_data['response_requirements'],
                        matched_triggers=matched_triggers
                    )
                    
                    search_results.append(search_result)
                    
                except (json.JSONDecodeError, KeyError) as e:
                    logger.error(f"Error parsing search result: {str(e)}")
                    continue
            
            logger.info(f"Found {len(search_results)} relevant SOPs for query")
            return search_results
            
        except Exception as e:
            logger.error(f"Error searching SOPs: {str(e)}")
            return []
    
    def get_all_sops(self) -> List[Dict[str, Any]]:
        """Get all stored SOPs with metadata"""
        try:
            cursor = self.conn.execute('SELECT data FROM sops')
            
            sops = []
            for row in cursor.fetchall():
                try:
                    sop_data = json.loads(row[0])
                    sops.append(sop_data)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing stored SOP: {str(e)}")
                    continue
            
            logger.info(f"Retrieved {len(sops)} SOPs from database")
            return sops
            
        except Exception as e:
            logger.error(f"Error retrieving all SOPs: {str(e)}")
            return []
    
    def delete_sop(self, sop_id: str) -> tuple[bool, Optional[str]]:
        """Delete SOP from database"""
        try:
            # Check if SOP exists
            cursor = self.conn.execute('SELECT sop_id FROM sops WHERE sop_id = ?', (sop_id,))
            if not cursor.fetchone():
                return False, f"SOP {sop_id} not found in database"
            
            # Delete from database
            self.conn.execute('DELETE FROM sops WHERE sop_id = ?', (sop_id,))
            self.conn.commit()
            
            logger.info(f"Successfully deleted SOP {sop_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error deleting SOP {sop_id}: {str(e)}")
            return False, f"Error deleting SOP: {str(e)}"
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the SOP database"""
        try:
            # Get count
            cursor = self.conn.execute('SELECT COUNT(*) FROM sops')
            count = cursor.fetchone()[0]
            
            # Get all SOPs for category breakdown
            all_sops = self.get_all_sops()
            
            # Calculate category breakdown
            categories = {}
            priorities = {}
            
            for sop in all_sops:
                category = sop.get('category', 'unknown')
                priority = sop.get('priority_override', 'not_specified')
                
                categories[category] = categories.get(category, 0) + 1
                priorities[priority] = priorities.get(priority, 0) + 1
            
            stats = {
                "total_sops": count,
                "database_path": self.db_path,
                "categories": categories,
                "priorities": priorities,
                "storage_type": "SQLite"
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {"error": str(e)}
    
    def _create_searchable_text(self, sop: ProcessedSOP) -> str:
        """Create combined text for embedding generation"""
        
        # Combine key searchable fields
        text_parts = [
            sop.title,
            sop.category,
            " ".join(sop.triggers),
            " ".join(sop.response_requirements.required_actions),
            " ".join(sop.response_requirements.notifications),
            " ".join(sop.regulatory_requirements)
        ]
        
        # Filter out empty parts and join
        searchable_text = " ".join([part for part in text_parts if part])
        
        return searchable_text
    
    def _find_matched_triggers(self, query: str, triggers: List[str]) -> List[str]:
        """Find triggers that match the query"""
        matched = []
        query_words = query.lower().split()
        
        for trigger in triggers:
            trigger_lower = trigger.lower()
            # Check for exact match or word overlap
            if trigger_lower in query or any(word in trigger_lower for word in query_words):
                matched.append(trigger)
        
        return matched