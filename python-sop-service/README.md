# SOP Processing Service - Restructured

This is the consolidated and restructured version of the SOP Processing Service, combining functionality from the previous multiple main files into a clean, scalable architecture.

## 🏗️ Architecture Overview

The service has been restructured with proper separation of concerns:

```
python-sop-service/
├── main.py                    # Single entry point
├── config/
│   ├── settings.py           # Environment configuration
│   └── database.py           # Database connection logic
├── api/
│   ├── routes/
│   │   ├── health.py         # Health check endpoints
│   │   ├── sop.py           # SOP management endpoints
│   │   ├── events.py        # Event processing endpoints
│   │   └── threats.py       # Threat correlation endpoints
│   └── dependencies.py      # FastAPI dependencies
├── agents/
│   ├── base.py              # Base agent class
│   ├── crews/
│   │   └── tailgating.py    # Tailgating correlation crew
│   └── tools/
│       ├── database_tools.py # Database utilities for agents
│       └── analysis_tools.py # Analysis utilities for agents
├── models/
│   ├── database.py          # SQLAlchemy models and database operations
│   └── schemas.py           # Pydantic models for API
├── services/
│   ├── sop_processor.py     # SOP document processing
│   ├── semantic_matcher.py  # Semantic matching service
│   └── event_processor.py   # Event processing service
├── utils/
│   └── logging.py           # Logging configuration
└── requirements.txt         # Consolidated dependencies
```

## 🚀 Key Features

### Unified Functionality
- **SOP Processing**: Document upload and rule extraction
- **Event Processing**: Security event handling with SOP matching
- **Threat Correlation**: AI-powered tailgating analysis with CrewAI
- **Semantic Matching**: Advanced text similarity matching
- **Database Integration**: PostgreSQL with SQLAlchemy ORM

### Scalable Design
- **Modular Architecture**: Clean separation of concerns
- **Agent Framework**: Base classes for future agent expansion
- **Configuration Management**: Environment-based settings
- **Comprehensive Logging**: Structured logging throughout

### API Endpoints

#### Health & Status
- `GET /api/v1/health` - Service health check
- `GET /` - Root endpoint with feature overview

#### SOP Management
- `POST /api/v1/sop/process` - Upload and process SOP documents
- `GET /api/v1/sops` - List all SOPs
- `GET /api/v1/sops/{id}/rules` - Get SOP rules
- `DELETE /api/v1/sops/{id}` - Delete SOP

#### Event Processing
- `POST /api/v1/events/process` - Process security events
- `GET /api/v1/events/recent` - Get recent events

#### Threat Correlation
- `GET /api/v1/threats/access-control` - Get threat correlations
- `GET /api/v1/threats/access-control/{id}` - Get specific correlation
- `POST /api/v1/threats/access-control/{id}/status` - Update threat status
- `GET /api/v1/threats/stats` - Get threat statistics

## 🛠️ Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/sop_events"
   export OPENAI_API_KEY="your-openai-api-key"  # Optional for CrewAI
   ```

3. **Run the Service**
   ```bash
   python main.py
   ```

## 📊 Configuration

The service uses environment variables for configuration:

- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for CrewAI agents
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8001)

## 🔧 Development

### Adding New Agents

1. Create agent in `agents/crews/` directory
2. Extend `BaseAgent` class from `agents/base.py`
3. Implement required methods: `analyze()` and `get_capabilities()`
4. Register in main application

### Adding New Endpoints

1. Create router in `api/routes/`
2. Follow existing patterns for error handling and logging
3. Use dependency injection for database sessions
4. Include router in `main.py`

## 🧪 Testing

The service includes comprehensive error handling and logging. Test endpoints using:

```bash
# Health check
curl http://localhost:8001/api/v1/health

# Upload SOP
curl -X POST -F "file=@sop.docx" http://localhost:8001/api/v1/sop/process

# Process event
curl -X POST -H "Content-Type: application/json" \
  -d '{"event_type": "Tailgating", "location": "Main Door", "timestamp": "2024-01-01T10:00:00Z"}' \
  http://localhost:8001/api/v1/events/process
```

## 📈 Performance & Scalability

- **Async/Await**: Full async support for I/O operations
- **Background Tasks**: CrewAI analysis runs in background
- **Database Optimization**: Indexed queries and connection pooling
- **Modular Design**: Easy to scale individual components

## 🔒 Security

- **Input Validation**: Pydantic models for all inputs
- **Error Handling**: Comprehensive error catching and logging
- **Database Security**: Parameterized queries prevent SQL injection
- **CORS Configuration**: Configurable cross-origin settings

## 📝 Migration Notes

This restructured version maintains **full backward compatibility** with the previous API while adding:

- Better organization and maintainability
- Improved error handling and logging
- Scalable architecture for future enhancements
- Cleaner separation of concerns
- Comprehensive documentation

The old files (`main_enhanced.py`, `main_simple.py`, `database_new.py`, `crew_ai_agents.py`) have been consolidated into this new structure without losing any functionality.