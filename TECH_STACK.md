# Tech Stack Documentation

## SOP-Enhanced Security Triage Agent

This document outlines the complete technology stack used in the SOP-Enhanced Security Triage Agent system.

---

## 🏗️ **Core Architecture**

### **Backend Framework**
- **FastAPI** (v0.104+) - Modern, high-performance Python web framework
  - Async/await support for concurrent request handling
  - Automatic API documentation generation (OpenAPI/Swagger)
  - Built-in request validation and serialization
  - Type hints and Pydantic integration
  - CORS middleware for cross-origin requests

### **Web Server**
- **Uvicorn** - Lightning-fast ASGI server
  - Production-ready with auto-reload capabilities
  - Supports HTTP/1.1 and WebSockets
  - Configurable host/port settings via environment variables

---

## 🤖 **AI & Machine Learning Stack**

### **Multi-Agent Framework**
- **CrewAI** (v0.141.0) - Advanced multi-agent AI orchestration
  - Sequential and hierarchical agent workflows
  - Tool integration and task delegation
  - Agent memory and context management
  - Verbose logging and execution tracking

### **Language Models**
- **OpenAI API** - Primary LLM provider
  - GPT-4o-mini for cost-effective analysis
  - Configurable model selection
  - Rate limiting and quota management
- **LiteLLM** - Unified interface for multiple LLM providers
  - Provider abstraction layer
  - Cost calculation and usage tracking
  - Fallback and retry mechanisms

### **AI-Powered Analysis Tools**
- **Computer Vision Threat Analyzer** - Custom CV event assessment
- **Access Control Analyzer** - Security system event evaluation
- **SOPContextualSearch** - Semantic SOP matching and consultation

---

## 🗄️ **Data Storage & Management**

### **Primary Database**
- **SQLite** - Lightweight, serverless database
  - SOP knowledge base storage (`sop_knowledge_base.db`)
  - Full-text search capabilities
  - ACID compliance and reliability
  - Zero-configuration deployment

### **Data Processing**
- **Pandas** - Data manipulation and CSV processing
  - Mock data loading for CV and access control events
  - Event categorization and filtering
- **JSON** - Structured data exchange format
  - API request/response serialization
  - SOP document processing and storage

### **File Storage**
- **Local File System** - Document and asset storage
  - SOP document uploads (Word, Markdown)
  - Static web assets (HTML, CSS, JavaScript)
  - Log file management

---

## 🔍 **Search & Processing**

### **Semantic Search**
- **Custom SQLite-based Search Engine**
  - Keyword matching and relevance scoring
  - Trigger phrase identification
  - Similarity calculation algorithms
  - Category-based filtering

### **Document Processing**
- **AI-Powered SOP Extraction**
  - Natural language processing for SOP parsing
  - Automatic trigger identification
  - Priority override detection
  - Regulatory requirement extraction

---

## 🌐 **Frontend Technologies**

### **Web Technologies**
- **HTML5** - Modern semantic markup
- **CSS3** - Responsive styling and animations
- **JavaScript (ES6+)** - Interactive functionality
  - Async/await for API communication
  - DOM manipulation and event handling
  - Real-time data updates

### **UI Framework**
- **Bootstrap 5** - Responsive CSS framework
  - Grid system and component library
  - Mobile-first responsive design
  - Custom theme and styling

### **Data Visualization**
- **Custom Priority Indicators** - Visual priority scoring
- **Real-time Activity Feeds** - Dynamic content updates
- **Dual Priority Display** - Original vs SOP-enhanced comparison

---

## 📡 **API & Communication**

### **HTTP Client**
- **HTTPX** - Modern async HTTP client
  - OpenAI API communication
  - External service integration
  - Connection pooling and retry logic

### **API Design**
- **RESTful Architecture** - Standard HTTP methods and status codes
- **JSON API** - Consistent request/response format
- **OpenAPI 3.0** - Automatic documentation generation
- **Async Endpoints** - Non-blocking request processing

### **Key API Endpoints**
```
GET  /activities                     # Activity simulation with SOP enhancement
POST /analyze/cv-threat-sop          # SOP-enhanced CV analysis
POST /analyze/access-control-sop     # SOP-enhanced access control analysis
GET  /sop/                           # SOP management interface
GET  /health                         # Service health check
GET  /docs                           # Interactive API documentation
```

---

## 🔒 **Security & Validation**

### **Data Validation**
- **Pydantic** - Runtime type checking and validation
  - Input sanitization and type coercion
  - Automatic error handling
  - Schema validation for API requests

### **Authentication & API Keys**
- **Environment-based Configuration** - Secure credential management
- **OpenAI API Key Management** - Encrypted API communication
- **CORS Security** - Controlled cross-origin access

---

## ⚡ **Performance & Optimization**

### **Caching Strategy**
- **In-Memory Result Caching** - Function-level response caching
- **Event Type Caching** - Repeated analysis optimization
- **Database Query Optimization** - Indexed searches and connection reuse

### **Performance Features**
- **Fast Mode** - Pre-calculated SOP overrides for demonstrations
- **Async Processing** - Concurrent request handling
- **Background Tasks** - Non-blocking operations
- **Connection Pooling** - Efficient resource management

### **Optimization Techniques**
- **Lazy Loading** - On-demand resource initialization
- **Response Compression** - Reduced bandwidth usage
- **Query Optimization** - Efficient database operations

---

## 📊 **Monitoring & Logging**

### **Logging Framework**
- **Python Logging** - Structured application logging
  - Multiple log levels (DEBUG, INFO, WARNING, ERROR)
  - File-based log rotation
  - Console output for development

### **Error Handling**
- **Graceful Degradation** - Fallback mechanisms for service failures
- **Exception Tracking** - Comprehensive error logging
- **API Error Responses** - User-friendly error messages

---

## 🛠️ **Development & Deployment**

### **Development Tools**
- **Python 3.13+** - Modern Python runtime
- **Virtual Environment** - Isolated dependency management
- **Environment Variables** - Configuration management via `.env`

### **Package Management**
- **pip** - Python package installer
- **requirements.txt** - Dependency specification
- **Version Pinning** - Reproducible builds

### **Code Quality**
- **Type Hints** - Static type checking support
- **Async/Await** - Modern Python concurrency
- **Error Handling** - Comprehensive exception management

---

## 📦 **Key Dependencies**

### **Core Dependencies**
```
fastapi>=0.104.0          # Web framework
uvicorn>=0.24.0           # ASGI server
crewai==0.141.0           # Multi-agent AI framework
openai>=1.0.0             # OpenAI API client
pydantic>=2.0.0           # Data validation
pandas>=2.0.0             # Data processing
sqlite3                   # Database (built-in)
```

### **Supporting Libraries**
```
httpx>=0.25.0             # HTTP client
litellm>=1.0.0            # LLM provider abstraction
python-multipart>=0.0.6   # File upload support
python-dotenv>=1.0.0      # Environment variable loading
```

---

## 🚀 **Deployment Configuration**

### **Environment Variables**
```bash
OPENAI_API_KEY=your_openai_api_key_here
PORT=8003
HOST=127.0.0.1
SOP_DATABASE_PATH=./sop_knowledge_base.db
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### **Server Configuration**
- **Default Port**: 8003
- **Host**: 127.0.0.1 (configurable)
- **Reload**: Disabled in production
- **Log Level**: INFO (configurable)

---

## 🔄 **Data Flow Architecture**

### **Request Processing Pipeline**
1. **FastAPI** receives HTTP request
2. **Pydantic** validates request data
3. **CrewAI** orchestrates multi-agent analysis
4. **OpenAI API** processes natural language tasks
5. **SQLite** provides SOP knowledge consultation
6. **Response** returns JSON with priority recommendations

### **SOP Enhancement Workflow**
1. Standard security analysis (baseline priority)
2. SOP contextual search (semantic matching)
3. Priority override application (SOP supersedes security)
4. Merged response generation (combined recommendations)
5. Dual priority display (original vs enhanced)

---

## 📈 **Performance Characteristics**

### **Response Times**
- **Fast Mode**: 1-2 seconds (pre-calculated overrides)
- **Cached Mode**: 2-3 seconds (subsequent requests)
- **Full Analysis**: 10-30 seconds (first-time AI processing)

### **Scalability Features**
- **Async Architecture** - High concurrent request handling
- **Database Optimization** - Efficient SOP searches
- **Caching Strategy** - Reduced API calls and processing time
- **Resource Management** - Connection pooling and cleanup

---

## 🧪 **Testing & Quality Assurance**

### **Testing Strategy**
- **Manual Integration Testing** - End-to-end workflow validation
- **API Endpoint Testing** - Request/response verification
- **SOP Priority Testing** - Override logic validation
- **Performance Testing** - Load and response time analysis

### **Quality Metrics**
- **Priority Accuracy** - Correct SOP override application
- **Response Consistency** - Reliable API behavior
- **Error Recovery** - Graceful failure handling
- **Performance Benchmarks** - Acceptable response times

---

## 📚 **Documentation & Resources**

### **API Documentation**
- **Swagger UI**: `http://localhost:8003/docs`
- **ReDoc**: `http://localhost:8003/redoc`
- **OpenAPI Schema**: Auto-generated from code

### **System Documentation**
- **README.md** - Project overview and setup instructions
- **TECH_STACK.md** - This comprehensive technical documentation
- **Code Comments** - Inline documentation and examples

---

## 🔮 **Future Enhancement Opportunities**

### **Potential Upgrades**
- **Vector Database Integration** - ChromaDB for advanced semantic search
- **Real-time Analytics** - Performance monitoring and metrics
- **WebSocket Support** - Real-time notifications and updates
- **Microservices Architecture** - Service decomposition for scale
- **Container Deployment** - Docker and Kubernetes support

### **AI Model Enhancements**
- **Custom Fine-tuning** - Domain-specific model training
- **Multi-modal Analysis** - Image and text processing
- **Streaming Responses** - Real-time AI output
- **Model Ensemble** - Multiple AI provider integration

---

*This documentation reflects the current state of the SOP-Enhanced Security Triage Agent as of the latest deployment. For the most up-to-date information, refer to the source code and API documentation.*