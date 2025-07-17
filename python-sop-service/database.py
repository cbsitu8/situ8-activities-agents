"""
Database configuration and models for the SOP Processing Service with Threat Correlation
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import json
import logging

logger = logging.getLogger(__name__)

async def get_db_connection():
    """Get database connection"""
    postgres_url = os.getenv('POSTGRES_URL', 'postgresql://postgres:password@localhost:5432/security_ops')
    return await asyncpg.connect(postgres_url)

class DatabaseManager:
    """
    Manages database operations for SOPs, rules, and embeddings
    """
    
    def __init__(self):
        self.postgres_url = os.getenv('POSTGRES_URL', 'postgresql://postgres:password@localhost:5432/security_ops')
    
    async def initialize(self):
        """Initialize database connection and verify tables"""
        try:
            conn = await get_db_connection()
            try:
                # Test connection
                await conn.fetchval("SELECT 1")
                logger.info("Database connection established")
            finally:
                await conn.close()
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    async def store_sop(self, sop_data: Dict[str, Any]) -> str:
        """
        Store SOP document in database
        """
        try:
            conn = await get_db_connection()
            try:
                sop_id = str(uuid.uuid4())
                
                await conn.execute("""
                    INSERT INTO sops (id, name, file_name, content, file_type, upload_status, created_at, updated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """, 
                sop_id,
                sop_data['name'],
                sop_data['name'],  # Use name as filename if not provided
                sop_data['content'],
                sop_data['file_type'],
                'completed',
                datetime.utcnow(),
                datetime.utcnow()
                )
                
                logger.info(f"Stored SOP with ID: {sop_id}")
                return sop_id
                
        except Exception as e:
            logger.error(f"Error storing SOP: {e}")
            raise
    
    async def store_rules(self, sop_id: str, rules: List[Dict[str, Any]]) -> int:
        """
        Store extracted rules for a SOP
        """
        try:
            async with get_db_connection() as conn:
                rules_stored = 0
                
                for rule in rules:
                    rule_id = str(uuid.uuid4())
                    
                    await conn.execute("""
                        INSERT INTO rules (id, sop_id, rule_type, rule_value, priority, agent_assignments, created_at)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    rule_id,
                    sop_id,
                    rule['rule_type'],
                    json.dumps(rule['rule_value']),
                    rule['priority'],
                    rule['agent_assignments'],
                    datetime.utcnow()
                    )
                    
                    rules_stored += 1
                
                logger.info(f"Stored {rules_stored} rules for SOP {sop_id}")
                return rules_stored
                
        except Exception as e:
            logger.error(f"Error storing rules: {e}")
            raise
    
    async def store_embedding(self, rule_id: str, phrase: str, embedding: np.ndarray):
        """
        Store semantic embedding for a rule phrase
        """
        try:
            async with get_db_connection() as conn:
                embedding_id = str(uuid.uuid4())
                
                # Convert numpy array to list for JSON storage
                embedding_list = embedding.tolist()
                
                await conn.execute("""
                    INSERT INTO embeddings (id, rule_id, phrase, embedding, created_at)
                    VALUES ($1, $2, $3, $4, $5)
                """,
                embedding_id,
                rule_id,
                phrase,
                embedding_list,  # PostgreSQL will handle the vector conversion
                datetime.utcnow()
                )
                
        except Exception as e:
            logger.error(f"Error storing embedding: {e}")
            raise
    
    async def get_all_sops(self) -> List[Dict[str, Any]]:
        """
        Get all stored SOPs
        """
        try:
            async with get_db_connection() as conn:
                rows = await conn.fetch("""
                    SELECT id, name, file_name, file_type, upload_status, created_at,
                           (SELECT COUNT(*) FROM rules WHERE sop_id = sops.id) as rule_count
                    FROM sops
                    ORDER BY created_at DESC
                """)
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting SOPs: {e}")
            raise
    
    async def get_sop_rules(self, sop_id: str) -> List[Dict[str, Any]]:
        """
        Get all rules for a specific SOP
        """
        try:
            async with get_db_connection() as conn:
                rows = await conn.fetch("""
                    SELECT id, rule_type, rule_value, priority, agent_assignments, created_at
                    FROM rules
                    WHERE sop_id = $1
                    ORDER BY priority DESC, created_at
                """, sop_id)
                
                rules = []
                for row in rows:
                    rule = dict(row)
                    # Parse JSON rule_value
                    rule['rule_value'] = json.loads(rule['rule_value'])
                    rules.append(rule)
                
                return rules
                
        except Exception as e:
            logger.error(f"Error getting SOP rules: {e}")
            raise
    
    async def get_semantic_rules_for_sop(self, sop_id: str) -> List[Dict[str, Any]]:
        """
        Get semantic rules for a specific SOP
        """
        try:
            async with get_db_connection() as conn:
                rows = await conn.fetch("""
                    SELECT id, rule_value
                    FROM rules
                    WHERE sop_id = $1 AND rule_type = 'semantic'
                """, sop_id)
                
                rules = []
                for row in rows:
                    rule = dict(row)
                    rule['rule_value'] = json.loads(rule['rule_value'])
                    rules.append(rule)
                
                return rules
                
        except Exception as e:
            logger.error(f"Error getting semantic rules: {e}")
            raise
    
    async def get_all_embeddings(self) -> List[Dict[str, Any]]:
        """
        Get all stored embeddings
        """
        try:
            async with get_db_connection() as conn:
                rows = await conn.fetch("""
                    SELECT id, rule_id, phrase, embedding
                    FROM embeddings
                """)
                
                embeddings = []
                for row in rows:
                    embedding_record = dict(row)
                    # Convert embedding back to numpy array
                    embedding_record['embedding'] = row['embedding']
                    embeddings.append(embedding_record)
                
                return embeddings
                
        except Exception as e:
            logger.error(f"Error getting embeddings: {e}")
            raise
    
    async def delete_sop(self, sop_id: str):
        """
        Delete a SOP and all its rules (cascading delete)
        """
        try:
            async with get_db_connection() as conn:
                await conn.execute("DELETE FROM sops WHERE id = $1", sop_id)
                logger.info(f"Deleted SOP {sop_id}")
                
        except Exception as e:
            logger.error(f"Error deleting SOP: {e}")
            raise
    
    async def load_computer_vision_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        """
        Load Computer Vision events from CSV content
        """
        try:
            events = []
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            async with get_db_connection() as conn:
                for row in csv_reader:
                    # Parse timestamp
                    creation_time = datetime.strptime(row['creation_time'], '%Y-%m-%d %H:%M:%S')
                    
                    await conn.execute("""
                        INSERT INTO csv_computer_vision_events 
                        (alert_event_id, severity, site_name, detection_name, creation_time, camera_name, readers_name)
                        VALUES ($1, $2, $3, $4, $5, $6, $7)
                    """,
                    row['alert_event_id'],
                    row['severity'],
                    row['site_name'],
                    row['detection_name'],
                    creation_time,
                    row['camera_name'],
                    row.get('readers_name', '')
                    )
                    
                    events.append(row)
            
            logger.info(f"Loaded {len(events)} Computer Vision events")
            return events
            
        except Exception as e:
            logger.error(f"Error loading Computer Vision CSV: {e}")
            raise
    
    async def load_access_control_csv(self, csv_content: str) -> List[Dict[str, Any]]:
        """
        Load Access Control events from CSV content
        """
        try:
            events = []
            csv_reader = csv.DictReader(io.StringIO(csv_content))
            
            async with get_db_connection() as conn:
                for row in csv_reader:
                    await conn.execute("""
                        INSERT INTO csv_access_control_events 
                        (serial_number, device_id, controller_id, segment_id, alarm_name, 
                         timestamp, alarm_id, badge_id, threat_level)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    """,
                    row['serial_number'],
                    row['device_id'],
                    row['controller_id'],
                    row['segment_id'],
                    row['alarm_name'],
                    int(row['timestamp']),
                    int(row['alarm_id']),
                    int(row.get('badge_id', 0)) if row.get('badge_id') else None,
                    row['threat_level']
                    )
                    
                    events.append(row)
            
            logger.info(f"Loaded {len(events)} Access Control events")
            return events
            
        except Exception as e:
            logger.error(f"Error loading Access Control CSV: {e}")
            raise