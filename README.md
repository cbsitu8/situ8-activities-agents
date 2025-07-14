# SOP-Enhanced Security Triage Agent

An intelligent security operations system that automatically analyzes security events and applies organizational Standard Operating Procedures (SOPs) to override AI threat assessments when appropriate. Built with CrewAI multi-agent framework and OpenAI integration.

## 🛡️ Overview

### **The Problem We Solve**
Traditional security systems rely purely on AI threat detection, which may not account for organizational priorities. For example:
- A "person falling down" might be classified as **LOW priority (2/10)** by AI
- But your **Medical Emergency SOP** requires it to be **CRITICAL priority (10/10)**
- This system automatically applies the SOP override for proper emergency response

### **Dual-Priority Analysis System**
This system provides intelligent analysis using CrewAI's multi-agent framework with two analysis modes:

1. **Standard AI Analysis**: Computer vision and access control threat assessment
2. **SOP-Enhanced Analysis**: Organizational procedures override AI when applicable

**Event Sources:**
- **Computer Vision Systems**: Threat detection alerts from video analytics  
- **Access Control Systems**: Door sensors, card readers, and security device events

**Key Innovation:** SOPs (Standard Operating Procedures) take precedence over AI assessments, ensuring organizational priorities and emergency protocols are properly followed.

## 🚀 Key Features

### **🧠 SOP-Enhanced Analysis**
- **Dual-Priority System**: Original AI assessment vs SOP-influenced priority
- **Automatic Override**: SOPs supersede AI when organizational policies apply
- **Visual Comparison**: Side-by-side display showing priority changes
- **Smart Reasoning**: AI explains why and how SOPs influenced decisions

### **📋 Standard Operating Procedures**
- **Medical Emergency Protocol**: Elevates fall detection to maximum priority
- **Weapon Incident Protocol**: Ensures firearm threats get immediate response  
- **Access Control Procedures**: Handles unauthorized access with proper escalation
- **Custom SOP Upload**: Add your own organizational procedures via web interface

### **🤖 Multi-Agent AI Framework**
- **CrewAI Integration**: Sophisticated multi-agent analysis workflow
- **Contextual Search**: Semantic matching of events to relevant SOPs
- **OpenAI GPT-4o-mini**: Advanced natural language processing
- **Intelligent Threat Classification**: 4-tier threat levels with confidence scoring

### **⚡ Performance & Interface**
- **Fast Mode**: 1-2 second responses with pre-calculated SOP overrides
- **Web Dashboards**: OpenAI Only vs OpenAI + SOPs comparison views
- **RESTful API**: FastAPI-based endpoints for easy integration
- **Real-time Processing**: Async handling of multiple security events

## 🚀 Quick Start

### **Prerequisites**
- Python 3.13+
- OpenAI API key
- Git

### **1. Installation**

```bash
# Clone the repository
git clone https://github.com/cbsitu8/situ8-activities-agents.git
cd situ8-activities-agents

# Install dependencies
pip install -r requirements.txt
```

### **2. Configuration**

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

**Required Configuration:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
PORT=8003
HOST=127.0.0.1
SOP_DATABASE_PATH=./sop_knowledge_base.db
```

### **3. Launch the System**

```bash
# Start the server
python main.py

# Server runs on http://localhost:8003
```

### **4. Access the Application**

**🌐 Web Interfaces:**
- **Fast Demo**: http://localhost:8003/activities?fast_mode=true *(1-2 seconds)*
- **Full System**: http://localhost:8003/activities *(SOP-enhanced analysis)*
- **SOP Manager**: http://localhost:8003/sop/ *(Upload & manage SOPs)*
- **API Docs**: http://localhost:8003/docs *(Interactive documentation)*

**✅ Health Check:**
```bash
curl http://localhost:8003/health
```

## 📊 API Endpoints

### **🧠 SOP-Enhanced Analysis**
- `GET /activities` - Simulate security activities with SOP enhancement
- `POST /analyze/cv-threat-sop` - Analyze computer vision events with SOPs
- `POST /analyze/access-control-sop` - Analyze access control events with SOPs
- `POST /analyze/sop-enhanced` - Generic SOP-enhanced event analysis

### **🤖 Standard Analysis**
- `POST /analyze/cv-threat` - Standard computer vision threat analysis
- `POST /analyze/access-control` - Standard access control analysis
- `POST /analyze/batch` - Batch analysis of multiple events
- `POST /analyze` - Generic analysis endpoint

### **📋 SOP Management**
- `GET /sop/` - SOP management web interface
- `POST /sop/upload` - Upload new SOP documents
- `GET /sop/stats` - View SOP database statistics
- `DELETE /sop/{sop_id}` - Remove specific SOP

### **🔧 System Utilities**
- `GET /health` - Service health check
- `GET /stats` - API usage statistics  
- `GET /config` - Configuration information
- `GET /docs` - Interactive API documentation (Swagger)
- `GET /redoc` - Alternative API documentation

## 🏥 Real-World SOP Examples

### **Medical Emergency Response**
```
Event: "Person falling down detected in lobby"
├── AI Analysis: 2/10 priority (routine monitoring)
├── SOP Consultation: Medical Emergency Protocol found
├── Priority Override: Elevated to 10/10 (critical)
├── Response Plan: Immediate first aid dispatch, emergency services
└── Timeline: 30 seconds (not 60 minutes)
```

### **Weapon Incident Handling**
```
Event: "Person brandishing firearm in Building A"
├── AI Analysis: 2/10 priority (possible false positive)
├── SOP Consultation: Weapon Incident Protocol found
├── Priority Override: Elevated to 9/10 (high)
├── Response Plan: Law enforcement, evacuation procedures
└── Timeline: Immediate (not routine)
```

### **Priority Display in Web Interface**
Each security event shows:
```
Original Priority: 2/10 (LOW)     →     Priority v2: 10/10 (MEDICAL EMERGENCY)
                                        ✅ SOP Override Applied
                                        📋 Medical Emergency Response Protocol
```

---

## 📱 Event Types

### Computer Vision Threats

```json
{
  "stored_at": "2025-07-08T18:30:03.703783Z",
  "record_id": "59786dbb-611b-4414-b3f0-f2bd1e980709",
  "data": {
    "threatSignature": {
      "id": 72,
      "name": "Person Brandishing Firearm",
      "icon": "GUN"
    },
    "site": {
      "id": 417,
      "name": "San Jose",
      "slug": "sjc"
    },
    "stream": {
      "id": 12421,
      "name": "HQ-SJ-B1F2-1",
      "space": {
        "id": 2698,
        "name": "Office",
        "fullPath": "San Jose > Building 1 > Floor 2 > Office"
      }
    },
    "alertId": 32552,
    "alertName": "Person Brandishing Firearm",
    "severity": "SEV0",
    "status": "RAISED"
  }
}
```

### Access Control Events

```json
{
  "serial_number": "AC001234",
  "device_id": "DR-B1-101",
  "controller_id": "CTRL-B1-01",
  "segment_id": "SEG-01",
  "timestamp_processed": "2025-07-09T14:23:45Z",
  "alarm_name": "Door Held Open",
  "timestamp": "2025-07-09T14:23:30Z",
  "alarm_id": "AL-45678",
  "source": "door_contact_sensor",
  "Subdevice_id": "SUB-001"
}
```

## 🔍 SOP-Enhanced Analysis Output

### **Example: Fall Detection with Medical Emergency SOP**

**Input Event:**
```json
{
  "device_id": "CAM-001",
  "location": "Lobby", 
  "detection_type": "Person Fall Detected",
  "confidence": 0.95,
  "timestamp": "2025-07-14T10:30:00Z"
}
```

**SOP-Enhanced Output:**
```json
{
  "original_security_analysis": {
    "ai_threat_level": "LOW",
    "priority_score": 2,
    "recommended_actions": ["Log incident", "Monitor for patterns"],
    "response_timeline": "ROUTINE (within 60 minutes)"
  },
  "sop_enhanced_result": {
    "final_threat_level": "MEDICAL EMERGENCY",
    "final_priority_score": 10,
    "applicable_sops": [
      {
        "title": "Medical Emergency Response Protocol",
        "priority_override": "HIGH",
        "similarity_score": 1.0
      }
    ],
    "merged_response_actions": [
      "IMMEDIATE: Dispatch first aid responder",
      "CONTACT: Emergency services and medical team", 
      "SECURE: Clear access path for emergency vehicles",
      "DOCUMENT: Incident details for OSHA compliance"
    ],
    "response_timeline": "IMMEDIATE (within 30 seconds)",
    "escalation_required": true,
    "regulatory_requirements": [
      "OSHA Incident Reporting",
      "Workers Compensation Documentation", 
      "Medical Privacy (HIPAA)"
    ],
    "sop_influence_reasoning": "Medical Emergency SOP applied - HIGH priority override for fall detection events",
    "confidence_score": 0.95
  }
}
```

## Threat Classification

### Threat Levels

| Level | Response Time | Escalation | Example Events |
|-------|---------------|------------|----------------|
| **CRITICAL** | 2 minutes | Required | Weapons, Violence, Forced Entry, Duress |
| **HIGH** | 5 minutes | Required | Unauthorized Access, Door Held Open, Invalid Cards |
| **MEDIUM** | 15 minutes | Optional | System Issues, Communication Lost, Door Ajar |
| **LOW** | 60 minutes | None | Maintenance Alerts, Routine Events |

### Confidence Scoring

- **High Confidence (>90%)**: Low false positive rate (5-10%)
- **Medium Confidence (70-90%)**: Moderate false positive rate (15-25%)
- **Low Confidence (<70%)**: Higher false positive rate (25-35%)

## Testing

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_cv_events.py
pytest tests/test_access_events.py

# Run with coverage
pytest --cov=agents --cov=models

# Run with verbose output
pytest -v
```

## Project Structure

```
security-triage-agent/
├── agents/
│   ├── __init__.py
│   ├── triage_agent.py          # Main CrewAI agent
│   └── tools/
│       ├── __init__.py
│       ├── cv_analyzer.py       # Computer vision analyzer
│       └── access_analyzer.py   # Access control analyzer
├── models/
│   ├── __init__.py
│   └── event_models.py          # Pydantic models
├── config/
│   ├── __init__.py
│   └── settings.py              # Configuration management
├── tests/
│   ├── __init__.py
│   ├── test_cv_events.py        # CV event tests
│   └── test_access_events.py    # Access control tests
├── data/
│   ├── sample_cv_events.json    # Sample CV events
│   └── sample_access_events.json # Sample AC events
├── main.py                      # FastAPI application
├── requirements.txt             # Dependencies
├── .env.template               # Environment template
└── README.md                   # This file
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | None |
| `API_HOST` | API host address | 0.0.0.0 |
| `API_PORT` | API port number | 8000 |
| `ENVIRONMENT` | Environment (dev/prod) | development |
| `LOG_LEVEL` | Logging level | INFO |
| `MAX_BATCH_SIZE` | Maximum batch size | 100 |
| `ANALYSIS_TIMEOUT` | Analysis timeout (seconds) | 30 |

### Threat Assessment Thresholds

| Threshold | Description | Default |
|-----------|-------------|---------|
| `CRITICAL_CONFIDENCE_THRESHOLD` | Critical threat confidence | 0.9 |
| `HIGH_CONFIDENCE_THRESHOLD` | High threat confidence | 0.8 |
| `WEAPON_DETECTION_FP_RATE` | Weapon detection false positive rate | 0.05 |
| `ACCESS_VIOLATION_FP_RATE` | Access violation false positive rate | 0.10 |

## Integration

### Go Backend Integration

The system is designed for easy integration with Go backends:

```go
// Example Go integration
type TriageRequest struct {
    EventData map[string]interface{} `json:"event_data"`
    EventType string                 `json:"event_type"`
}

func analyzeEvent(eventData map[string]interface{}, eventType string) (*TriageResponse, error) {
    url := "http://localhost:8000/analyze"
    
    payload := TriageRequest{
        EventData: eventData,
        EventType: eventType,
    }
    
    // Send POST request to triage agent
    // Handle response...
}
```

### Message Queue Integration

For high-throughput scenarios, integrate with message queues:

```python
# Redis/RabbitMQ integration example
import redis
import json

def process_event_queue():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    while True:
        event = r.blpop('security_events', timeout=5)
        if event:
            event_data = json.loads(event[1])
            result = run_triage_analysis(event_data['data'], event_data['type'])
            r.lpush('triage_results', json.dumps(result))
```

## Performance Considerations

- **Batch Processing**: Use `/analyze/batch` for multiple events
- **Caching**: Implement response caching for similar events
- **Rate Limiting**: Configure rate limiting for production use
- **Database Integration**: Add database for event storage and analytics

## Security Considerations

- **API Keys**: Secure OpenAI API key storage
- **Authentication**: Implement API authentication for production
- **CORS**: Configure CORS origins appropriately
- **Input Validation**: All inputs are validated using Pydantic models
- **Logging**: Comprehensive logging for audit trails

## Monitoring and Metrics

- **Health Checks**: `/health` endpoint for monitoring
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Comprehensive error handling and logging
- **Event Analytics**: Track threat patterns and false positive rates

## 🎉 Success Metrics

This system has successfully demonstrated:
- ✅ **Fall detection events** elevated from 2/10 to 10/10 priority
- ✅ **Medical emergency response** time reduced from 60 minutes to 30 seconds  
- ✅ **Weapon incidents** properly escalated with immediate law enforcement notification
- ✅ **Organizational compliance** automatically integrated into security responses
- ✅ **Fast demonstration mode** for stakeholder presentations (1-2 second response)

## 🔮 Future Enhancements

### **Planned Features**
- **Real-time Notifications**: WebSocket integration for instant alerts
- **Advanced Analytics**: Historical trend analysis and reporting
- **Mobile Interface**: Responsive mobile app for field operations
- **Integration APIs**: Connect with existing SIEM and security systems

### **AI Improvements**
- **Custom Model Training**: Fine-tuned models for specific organizational needs
- **Multi-modal Analysis**: Process images, video, and text simultaneously
- **Predictive Analytics**: Anticipate security events before they occur
- **Vector Database**: ChromaDB integration for advanced semantic search

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   ```
   Error: OpenAI API key is required
   Solution: Add OPENAI_API_KEY to .env file
   ```

2. **Import Errors**
   ```
   Error: Module not found
   Solution: Ensure virtual environment is activated
   ```

3. **Port Already in Use**
   ```
   Error: Port 8000 is already in use
   Solution: Change API_PORT in .env or kill existing process
   ```

### Debugging

```bash
# Enable debug mode
export DEBUG=true

# Increase log level
export LOG_LEVEL=DEBUG

# Run with verbose output
python main.py --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## 📞 Support

### **Getting Help**
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Comprehensive guides at `/docs` endpoint
- **Tech Stack**: Review `TECH_STACK.md` for technical details

### **Contact**
- **Project Repository**: [GitHub - SOP-Enhanced Security Triage Agent](https://github.com/cbsitu8/situ8-activities-agents)
- **Issues & Feature Requests**: Use GitHub Issues for project-related inquiries

---

**The SOP-Enhanced Security Triage Agent bridges the gap between AI automation and organizational wisdom, ensuring that technology serves human priorities and safety protocols.**

*Built with ❤️ using FastAPI, CrewAI, and OpenAI*