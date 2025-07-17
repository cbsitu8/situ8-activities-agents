# Product Requirements Document
## SOP-Enhanced Agentic Security Operations System

**Version:** 2.0  
**Date:** January 2025  
**Status:** Implementation Ready

---

## 1. Executive Summary

### 1.1 Purpose
Build a microservices-based security event routing system that uses organizational Standard Operating Procedures (SOPs) to automatically route events to specialized security agents. The system replaces traditional AI triage with deterministic, SOP-based routing while maintaining an agentic architecture for future expansion.

### 1.2 System Overview
- **Go-based routing engine** for high-performance event processing
- **Python microservice** for SOP semantic processing
- **Svelte frontend** for SOP management and event simulation
- **PostgreSQL** for persistent storage with JSON import/export
- **Future-ready** architecture for specialist security agents

### 1.3 Key Innovation
Events are routed in <50ms using rule-based matching derived from organizational SOPs, ensuring compliance and eliminating LLM latency in the critical path while preserving intelligent agent capabilities for domain-specific processing.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐     ┌─────────────────┐    ┌─────────────────┐  │
│  │ Svelte Frontend │     │ Go Routing API  │    │ Python SOP Svc  │  │
│  │                 │────▶│                 │───▶│                 │  │
│  │ • SOP Upload    │ SSE │ • Event Router  │    │ • SOP Parser    │  │
│  │ • Event Trigger │◀────│ • Rule Cache    │    │ • Semantic Gen  │  │
│  │ • Status View   │     │ • Agent Dispatch│    │ • Rule Builder  │  │
│  └─────────────────┘     └────────┬────────┘    └─────────────────┘  │
│                                   │                                    │
│                          ┌────────▼────────┐                          │
│                          │   PostgreSQL    │                          │
│                          │                 │                          │
│                          │ • SOP Rules     │                          │
│                          │ • Event History │                          │
│                          │ • Agent Config  │                          │
│                          └─────────────────┘                          │
│                                                                         │
│  Future Agent Services (Phase 2):                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │ Access   │ │Perimeter │ │ Environ  │ │Escalation│                │
│  │ Agent    │ │ Agent    │ │ Agent    │ │ Agent    │                │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Functional Requirements

### 3.1 Go Routing Engine API

#### 3.1.1 Core Endpoints

```go
// Event Processing Endpoints
POST   /api/v1/events/process     // Process single event
POST   /api/v1/events/batch       // Process batch of events
GET    /api/v1/events/stream      // SSE endpoint for status updates

// Rule Management (calls Python service)
POST   /api/v1/rules/refresh      // Refresh rules from database
GET    /api/v1/rules/cache/stats  // Cache statistics

// Testing Endpoints
POST   /api/v1/test/load-csv      // Load events from CSV
GET    /api/v1/test/mock-event    // Generate mock event

// Health & Monitoring
GET    /api/v1/health             // Service health
GET    /api/v1/metrics            // Performance metrics
```

#### 3.1.2 Event Processing Flow

```go
// Simplified event structure
type SecurityEvent struct {
    ID           string                 `json:"id"`
    Source       string                 `json:"source"` // "access_control" | "computer_vision"
    Type         string                 `json:"type"`   // e.g., "Person Fall Detected"
    Location     string                 `json:"location"`
    Timestamp    time.Time              `json:"timestamp"`
    Severity     string                 `json:"severity"`
    MediaURL     string                 `json:"media_url,omitempty"` // For MP4s
    RawData      map[string]interface{} `json:"raw_data"`
}

// Routing decision structure
type RoutingDecision struct {
    EventID      string         `json:"event_id"`
    Priority     string         `json:"priority"` // CRITICAL|HIGH|MEDIUM|LOW
    MatchedSOP   string         `json:"matched_sop"`
    Confidence   float64        `json:"confidence"`
    AssignedAgents []AgentRoute `json:"assigned_agents"`
    ResponseTime time.Duration  `json:"response_time"`
}
```

#### 3.1.3 Rule Caching Strategy

```go
// In-memory rule cache for <1ms matching
type RuleCache struct {
    exactMatches   map[string]*Rule  // O(1) lookup
    keywordIndex   *TrieIndex        // Fast prefix matching
    patternMatches []*RegexRule      // Compiled regex patterns
    semanticRules  []*SemanticRule   // Requires Python service call
}

// TODO: Future enhancement - implement distributed cache for horizontal scaling
// Consider Redis or Hazelcast when scaling beyond single instance
```

### 3.2 Python SOP Processing Service

#### 3.2.1 API Endpoints

```python
# FastAPI endpoints
POST   /api/v1/sop/process        # Process uploaded SOP document
POST   /api/v1/sop/extract-rules  # Extract rules from SOP text
POST   /api/v1/semantic/match     # Semantic similarity matching
GET    /api/v1/semantic/health    # Service health check
```

#### 3.2.2 SOP Processing Pipeline

```python
class SOPProcessor:
    """
    Processes SOP documents into actionable rules
    """
    def process_document(self, file_content: bytes, file_type: str) -> SOPRules:
        # 1. Extract text from docx/md
        text = self.extract_text(file_content, file_type)
        
        # 2. Parse sections and identify key components
        sections = self.parse_sections(text)
        
        # 3. Extract triggers and conditions
        triggers = self.extract_triggers(sections)
        
        # 4. Generate semantic embeddings
        embeddings = self.generate_embeddings(triggers)
        
        # 5. Build rule structure
        return self.build_rules(sections, triggers, embeddings)

class SemanticMatcher:
    """
    Uses sentence-transformers for semantic matching
    """
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def generate_embeddings(self, phrases: List[str]) -> List[np.ndarray]:
        return self.model.encode(phrases)
        
    def calculate_similarity(self, event_text: str, sop_embeddings: List[np.ndarray]) -> float:
        event_embedding = self.model.encode([event_text])[0]
        similarities = [cosine_similarity(event_embedding, sop_emb) for sop_emb in sop_embeddings]
        return max(similarities)
```

### 3.3 Svelte Frontend

#### 3.3.1 Page Structure

```
/                           # Landing page with navigation
/sop-manager                # SOP upload and management
/event-simulator            # Event triggering and monitoring
```

#### 3.3.2 SOP Manager Page

```svelte
<!-- Key Components -->
<SOPUploader>
  - Drag-and-drop for .docx/.md files
  - Upload progress indicator
  - Validation feedback
</SOPUploader>

<SOPList>
  - Display all loaded SOPs
  - View extracted rules
  - Export/Import JSON
  - Delete functionality
</SOPList>

<RuleViewer>
  - Show extracted triggers
  - Display priority mappings
  - Preview agent assignments
</RuleViewer>
```

#### 3.3.3 Event Simulator Page

```svelte
<!-- Event Source Selection -->
<EventSourceSelector>
  - Choose: Access Control | Computer Vision | Custom
  - Load from CSV option
  - Manual event creation form
</EventSourceSelector>

<!-- Event Trigger Controls -->
<TriggerControls>
  - Single Event button
  - Batch (10 events) button
  - Auto-generate options
</TriggerControls>

<!-- Real-time Status Display -->
<EventStatusDisplay>
  - SSE connection for updates
  - Show routing decision
  - Display assigned agents
  - Processing time metrics
  - Loading states with descriptive text:
    * "Analyzing event..."
    * "Matching against SOPs..."
    * "Routing to agents..."
    * "Complete!"
</EventStatusDisplay>

<!-- Results Grid -->
<ResultsGrid>
  - Event details
  - Matched SOP
  - Priority assignment
  - Agent routing
  - Response timeline
</ResultsGrid>
```

### 3.4 Database Schema

```sql
-- PostgreSQL schema

-- SOP storage
CREATE TABLE sops (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    file_name VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Extracted rules
CREATE TABLE rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sop_id UUID REFERENCES sops(id) ON DELETE CASCADE,
    rule_type VARCHAR(50), -- 'exact', 'keyword', 'pattern', 'semantic'
    rule_value JSONB,
    priority VARCHAR(20), -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    agent_assignments TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- Semantic embeddings
CREATE TABLE embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id UUID REFERENCES rules(id) ON DELETE CASCADE,
    phrase TEXT,
    embedding VECTOR(384), -- Using pgvector extension
    created_at TIMESTAMP DEFAULT NOW()
);

-- Event history
CREATE TABLE event_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_data JSONB,
    routing_decision JSONB,
    processed_at TIMESTAMP DEFAULT NOW(),
    processing_time_ms INTEGER
);

-- Agent configuration (for future use)
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100),
    type VARCHAR(50), -- 'access', 'perimeter', 'environment', etc.
    endpoint VARCHAR(255),
    capabilities JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- TODO: Add indexes for performance optimization
-- CREATE INDEX idx_rules_sop_id ON rules(sop_id);
-- CREATE INDEX idx_embeddings_rule_id ON embeddings(rule_id);
```

### 3.5 Agent Integration (Future Phase)

```go
// Agent interface for future implementation
type SecurityAgent interface {
    // Process receives an event and returns a response
    Process(ctx context.Context, event SecurityEvent) (*AgentResponse, error)
    
    // GetCapabilities returns what types of events this agent handles
    GetCapabilities() []string
    
    // HealthCheck verifies agent availability
    HealthCheck(ctx context.Context) error
}

// TODO: Implement these agents in Phase 2
// - AccessControlAgent: Badge validation, door timing, tailgating
// - PerimeterAgent: Camera analysis, fence monitoring, intrusion detection  
// - EnvironmentAgent: Fire systems, HVAC, life safety
// - EscalationAgent: Notifications, dispatch, incident management
// - CoordinationAgent: Multi-agent orchestration, correlation
// - DocumentationAgent: Logging, compliance, reporting
```

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements

| Metric | Target | Notes |
|--------|--------|-------|
| Event Routing Latency | <50ms | 95th percentile |
| Rule Cache Hit Rate | >90% | After warm-up |
| Concurrent Events | 10/sec | Initial target |
| SOP Processing Time | <30sec | Per document |
| Frontend Load Time | <2sec | Initial page load |
| SSE Latency | <100ms | Status updates |

### 4.2 System Requirements

- **Go Version**: 1.21+ (for better performance)
- **Python Version**: 3.11+ (for latest ML libraries)
- **Node Version**: 18+ (for Svelte)
- **PostgreSQL**: 15+ with pgvector extension
- **Memory**: 4GB minimum (2GB for Go service)
- **Storage**: 50GB for media files

### 4.3 Security Considerations

```go
// API Security
// TODO: Implement in production phase
// - API key authentication
// - Rate limiting (100 req/min)
// - Input validation
// - SQL injection prevention
// - XSS protection in frontend
```

---

## 5. API Integration Examples

### 5.1 Processing an Event

```bash
# Single event processing
curl -X POST http://localhost:8080/api/v1/events/process \
  -H "Content-Type: application/json" \
  -d '{
    "source": "computer_vision",
    "type": "Person Fall Detected",
    "location": "Lobby Camera 01",
    "severity": "SEV2",
    "media_url": "s3://security-media/event-123.mp4",
    "timestamp": "2025-01-14T10:30:00Z"
  }'

# Response
{
  "event_id": "evt_123",
  "priority": "CRITICAL",
  "matched_sop": "Medical Emergency Response",
  "confidence": 0.95,
  "assigned_agents": [
    {"name": "EnvironmentAgent", "action": "Check life safety"},
    {"name": "EscalationAgent", "action": "Contact EMS"},
    {"name": "DocumentationAgent", "action": "Log for OSHA"}
  ],
  "response_time": "23ms"
}
```

### 5.2 SSE Status Stream

```javascript
// Svelte component example
const eventSource = new EventSource('/api/v1/events/stream');

eventSource.onmessage = (event) => {
  const status = JSON.parse(event.data);
  // Update UI with status
  updateEventStatus(status);
};

// Status message format
{
  "event_id": "evt_123",
  "stage": "routing",
  "message": "Matching against SOPs...",
  "progress": 50
}
```

---

## 6. Development Phases

### Phase 1: Core System (Current)
- [ ] Go routing engine with rule caching
- [ ] Python SOP processing service  
- [ ] Svelte frontend (2 pages)
- [ ] PostgreSQL integration
- [ ] CSV test data loading
- [ ] Basic SSE status updates

### Phase 2: Agent Implementation
```go
// TODO: Build specialized agents when prompted for Phase 2
// Each agent should implement the SecurityAgent interface
// Start with mock responses, then add real logic
```

### Phase 3: Production Readiness
```go
// TODO: Add when prompted for production deployment
// - Docker containers for each service
// - Kubernetes manifests
// - Monitoring (Prometheus/Grafana)
// - Centralized logging (ELK stack)
// - Horizontal scaling capabilities
```

---

## 7. Testing Strategy

### 7.1 Test Data

Use provided CSV files:
- **MockData_AccessControl.csv**: 368 rows, 8 columns
- **MockData_ComputerVision.csv**: 150 rows, 7 columns

### 7.2 Test Scenarios

```go
// Key test cases to implement
func TestExactMatchRouting(t *testing.T) {
    // Test that exact event matches route correctly
}

func TestSemanticMatchFallback(t *testing.T) {
    // Test semantic matching when exact/keyword fail
}

func TestHighVolumeProcessing(t *testing.T) {
    // Test 10 events/second throughput
}

func TestSOPPrioritization(t *testing.T) {
    // Verify SOP priority overrides default severity
}
```

---

## 8. Configuration

### 8.1 Environment Variables

```bash
# Go Service
POSTGRES_URL=postgresql://user:pass@localhost:5432/security_ops
PYTHON_SERVICE_URL=http://localhost:8001
PORT=8080
CACHE_TTL=3600
MEDIA_STORAGE_PATH=/var/security/media

# Python Service  
POSTGRES_URL=postgresql://user:pass@localhost:5432/security_ops
MODEL_CACHE_DIR=/tmp/models
PORT=8001

# Frontend
API_URL=http://localhost:8080
SSE_ENDPOINT=http://localhost:8080/api/v1/events/stream
```

---

## 9. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Routing Accuracy | >95% | Correct SOP matches |
| System Uptime | 99.9% | Service availability |
| Processing Speed | <50ms | 95th percentile |
| SOP Coverage | >80% | Events with SOP match |
| False Positives | <5% | Incorrect CRITICAL routing |

---

## 10. Appendices

### 10.1 Example SOP Rule Structure

```json
{
  "sop_id": "med_001",
  "name": "Medical Emergency Response",
  "rules": {
    "exact_matches": ["Person Fall Detected", "Medical Emergency"],
    "keywords": ["fall", "collapsed", "injury", "medical"],
    "patterns": ["person.*(fallen|down)", "medical.*emergency"],
    "semantic_phrases": [
      "person has fallen",
      "someone is injured",
      "medical assistance needed"
    ]
  },
  "priority": "CRITICAL",
  "agent_routing": {
    "primary": ["EnvironmentAgent", "EscalationAgent"],
    "secondary": ["DocumentationAgent"],
    "instructions": {
      "EnvironmentAgent": "Clear area and check life safety systems",
      "EscalationAgent": "Contact EMS and medical team immediately",
      "DocumentationAgent": "Create OSHA-compliant incident report"
    }
  }
}
```

### 10.2 CSV Data Transformation

```go
// Transform Access Control CSV
type AccessControlEvent struct {
    SerialNumber  string `csv:"serial_number"`
    DeviceID      string `csv:"device_id"`
    ControllerID  string `csv:"controller_id"`
    SegmentID     string `csv:"segment_id"`
    AlarmName     string `csv:"alarm_name"`
    Timestamp     int64  `csv:"timestamp"`
    AlarmID       int    `csv:"alarm_id"`
    BadgeID       int    `csv:"badge_id"`
}

// Transform to standard SecurityEvent
func TransformAccessControl(ac AccessControlEvent) SecurityEvent {
    return SecurityEvent{
        Source:   "access_control",
        Type:     ac.AlarmName,
        Location: ac.DeviceID,
        // ... additional mapping
    }
}
```

---

**This PRD provides a complete blueprint for building the SOP-Enhanced Agentic Security Operations System. The architecture is designed for current implementation while maintaining clear paths for future agent integration and scaling.**