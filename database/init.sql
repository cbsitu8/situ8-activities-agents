-- SOP-Enhanced Agentic Security Operations System
-- PostgreSQL Database Schema with pgvector extension

-- Enable pgvector extension for semantic embeddings
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- SOP storage table
CREATE TABLE sops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    file_name VARCHAR(255),
    content TEXT,
    file_type VARCHAR(10), -- 'docx', 'md', 'txt'
    upload_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'error'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Extracted rules from SOPs
CREATE TABLE rules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sop_id UUID REFERENCES sops(id) ON DELETE CASCADE,
    rule_type VARCHAR(50) NOT NULL, -- 'exact', 'keyword', 'pattern', 'semantic'
    rule_value JSONB NOT NULL,
    priority VARCHAR(20) NOT NULL, -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    agent_assignments TEXT[],
    confidence_threshold FLOAT DEFAULT 0.8,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Semantic embeddings for rule matching
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID REFERENCES rules(id) ON DELETE CASCADE,
    phrase TEXT NOT NULL,
    embedding VECTOR(384), -- sentence-transformers 'all-MiniLM-L6-v2' output dimension
    created_at TIMESTAMP DEFAULT NOW()
);

-- Event history for tracking processed events
CREATE TABLE event_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_data JSONB NOT NULL,
    routing_decision JSONB,
    matched_rule_id UUID REFERENCES rules(id),
    processing_time_ms INTEGER,
    processed_at TIMESTAMP DEFAULT NOW()
);

-- Agent configuration (for future use)
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'access', 'perimeter', 'environment', 'escalation', etc.
    endpoint VARCHAR(255),
    capabilities JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- CSV test data tables for development
CREATE TABLE csv_computer_vision_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_event_id VARCHAR(50),
    severity VARCHAR(20),
    site_name VARCHAR(100),
    detection_name VARCHAR(255),
    creation_time TIMESTAMP,
    camera_name VARCHAR(100),
    readers_name VARCHAR(100),
    loaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE csv_access_control_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    serial_number VARCHAR(50),
    device_id VARCHAR(100),
    controller_id VARCHAR(50),
    segment_id VARCHAR(50),
    alarm_name VARCHAR(255),
    timestamp BIGINT,
    alarm_id BIGINT,
    badge_id BIGINT,
    threat_level VARCHAR(20),
    loaded_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_rules_sop_id ON rules(sop_id);
CREATE INDEX idx_rules_type_priority ON rules(rule_type, priority);
CREATE INDEX idx_embeddings_rule_id ON embeddings(rule_id);
CREATE INDEX idx_event_history_processed_at ON event_history(processed_at);
CREATE INDEX idx_event_history_rule_id ON event_history(matched_rule_id);

-- Insert sample agents for future development
INSERT INTO agents (name, type, capabilities) VALUES
('AccessControlAgent', 'access', '{"handles": ["badge_validation", "door_timing", "tailgating"]}'),
('PerimeterAgent', 'perimeter', '{"handles": ["camera_analysis", "fence_monitoring", "intrusion_detection"]}'),
('EnvironmentAgent', 'environment', '{"handles": ["fire_systems", "hvac", "life_safety"]}'),
('EscalationAgent', 'escalation', '{"handles": ["notifications", "dispatch", "incident_management"]}'),
('DocumentationAgent', 'documentation', '{"handles": ["logging", "compliance", "reporting"]}');

-- Insert sample SOP for testing
INSERT INTO sops (name, file_name, content, file_type, upload_status) VALUES
('Medical Emergency Response', 'medical_emergency.md', 
'# Medical Emergency Response SOP

## Purpose
This procedure outlines the response protocol for medical emergencies on site.

## Triggers
- Person falling down
- Person collapsed
- Medical assistance needed
- Someone injured
- Unconscious person

## Response Actions
1. **Immediate Response (CRITICAL priority)**
   - Contact EMS immediately
   - Secure the area
   - Provide first aid if trained

2. **Environmental Safety**
   - Check life safety systems
   - Clear evacuation routes
   - Monitor for additional hazards

3. **Documentation**
   - Create incident report
   - Document timeline
   - Notify management
   - OSHA compliance reporting if required

## Agent Assignments
- EnvironmentAgent: Check life safety systems
- EscalationAgent: Contact EMS and medical team
- DocumentationAgent: Create OSHA-compliant incident report
', 'md', 'completed');

-- Get the SOP ID for sample rules
DO $$
DECLARE
    medical_sop_id UUID;
BEGIN
    SELECT id INTO medical_sop_id FROM sops WHERE name = 'Medical Emergency Response';
    
    -- Insert sample rules for medical emergency SOP
    INSERT INTO rules (sop_id, rule_type, rule_value, priority, agent_assignments) VALUES
    (medical_sop_id, 'exact', '["Person Falling Down", "Person Brandishing Firearm"]', 'CRITICAL', 
     ARRAY['EnvironmentAgent', 'EscalationAgent', 'DocumentationAgent']),
    (medical_sop_id, 'keyword', '["fall", "fallen", "collapsed", "injury", "medical", "unconscious"]', 'CRITICAL',
     ARRAY['EnvironmentAgent', 'EscalationAgent']),
    (medical_sop_id, 'semantic', '["person has fallen", "someone is injured", "medical assistance needed"]', 'CRITICAL',
     ARRAY['EnvironmentAgent', 'EscalationAgent', 'DocumentationAgent']);
END $$;