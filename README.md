# CrewAI Security Triage Agent

A CrewAI-powered security event analysis and triage system for computer vision threat detection and access control systems.

## Overview

This system provides intelligent analysis and prioritization of security events using CrewAI's multi-agent framework. It processes events from two main sources:
- **Computer Vision Systems**: Threat detection alerts from video analytics
- **Access Control Systems**: Door sensors, card readers, and security device events

The system provides real-time threat assessment, confidence scoring, and actionable recommendations for security operations teams.

## Features

- **Multi-Agent Analysis**: Specialized agents for different event types
- **Intelligent Threat Classification**: 4-tier threat levels (CRITICAL, HIGH, MEDIUM, LOW)
- **Confidence Scoring**: AI-powered confidence levels and false positive probability
- **Actionable Recommendations**: Specific, time-bound action items for security teams
- **Escalation Logic**: Automatic escalation rules for high-priority threats
- **RESTful API**: FastAPI-based endpoints for easy integration
- **Batch Processing**: Handle multiple events efficiently
- **Comprehensive Testing**: Full test suite with pytest

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd situ8-triage-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your OpenAI API key
nano .env
```

**Required Configuration:**
- `OPENAI_API_KEY`: Your OpenAI API key (get from [OpenAI Platform](https://platform.openai.com/api-keys))

### 3. Run the Application

```bash
# Start the API server
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

## API Endpoints

### Core Analysis Endpoints

- `POST /analyze/cv-threat` - Analyze computer vision threat events
- `POST /analyze/access-control` - Analyze access control events
- `POST /analyze/batch` - Batch analysis of multiple events
- `POST /analyze` - Generic analysis endpoint

### Utility Endpoints

- `GET /health` - Health check
- `GET /stats` - API usage statistics
- `GET /config` - Configuration information
- `GET /` - API information and documentation links

## Event Types

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

## Analysis Output

The system returns comprehensive triage analysis:

```json
{
  "event_type": "CV_THREAT",
  "ai_threat_level": "CRITICAL",
  "false_positive_probability": 0.05,
  "confidence_score": 0.95,
  "recommended_actions": [
    "IMMEDIATE: Dispatch security personnel to location",
    "IMMEDIATE: Notify law enforcement if weapon confirmed",
    "IMMEDIATE: Consider lockdown procedures if necessary"
  ],
  "escalation_required": true,
  "response_timeline": "IMMEDIATE (within 2 minutes)",
  "analysis_reasoning": "Weapon detection at critical facility location requires immediate response",
  "event_summary": "Person Brandishing Firearm detected at San Jose > Building 1 > Floor 2 > Office (San Jose)",
  "priority_score": 10
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

## Future Enhancements

- **Database Integration**: PostgreSQL for event storage
- **Real-time Dashboard**: Web interface for security operations
- **Machine Learning**: Custom ML models for threat detection
- **Integration APIs**: Connectors for popular SIEM systems
- **Mobile Notifications**: Push notifications for critical events
- **Automated Response**: Integration with physical security systems

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

## Support

For support and questions:
- Create an issue on GitHub
- Check the documentation at `/docs` endpoint
- Review the test files for usage examples