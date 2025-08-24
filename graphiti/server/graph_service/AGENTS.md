# AGENTS.md

This file provides guidance to AI agents when working with the graph service components.

## Directory Overview

This directory contains the core FastAPI application implementation, including the main server setup, configuration management, and the primary service logic for the Graphiti REST API.

## Files

- `main.py` - Main FastAPI application setup and server configuration
- `config.py` - Configuration management and environment variable handling
- `zep_graphiti.py` - Core Graphiti service integration and business logic
- `routers/` - API endpoint routing modules organized by functionality
- `dto/` - Data Transfer Objects for API request/response models

## Service Architecture

### Main Application (`main.py`)

The main FastAPI application provides:

1. **Application Setup**: FastAPI app initialization and configuration
2. **Middleware**: CORS, logging, error handling middleware
3. **Router Registration**: Include routers for different API endpoints
4. **Documentation**: Automatic OpenAPI/Swagger documentation setup
5. **Health Checks**: Basic health and status endpoints

### Configuration Management (`config.py`)

Configuration handling includes:

1. **Environment Variables**: Load configuration from environment
2. **Default Values**: Sensible defaults for development
3. **Validation**: Configuration validation and error handling
4. **Database Settings**: Database connection configuration
5. **API Settings**: API-specific configuration options

### Service Integration (`zep_graphiti.py`)

Core service logic provides:

1. **Graphiti Integration**: Bridge between FastAPI and Graphiti core
2. **Business Logic**: High-level operations and workflows
3. **Error Handling**: Service-level error handling and logging
4. **Resource Management**: Database connections and resource cleanup
5. **Performance Optimization**: Caching and optimization logic

## Agent Guidelines

### Development Setup

#### With Neo4j
```bash
cd server/
# Install dependencies
uv sync --extra dev

# Set environment variables for Neo4j
export OPENAI_API_KEY=your_key
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# Run development server
uvicorn graph_service.main:app --reload --host 0.0.0.0 --port 8000
```

#### With FalkorDB
```bash
cd server/
# Install dependencies
uv sync --extra dev

# Set environment variables for FalkorDB
export OPENAI_API_KEY=your_key
export FALKORDB_HOST=localhost
export FALKORDB_PORT=6379
export DATABASE_TYPE=falkordb
# Optional authentication
export FALKORDB_USERNAME=your_username
export FALKORDB_PASSWORD=your_password

# Run development server
uvicorn graph_service.main:app --reload --host 0.0.0.0 --port 8000
```

### Configuration Management

```python
from graph_service.config import Settings

# Load configuration
settings = Settings()

# Access configuration values
database_uri = settings.neo4j_uri
api_key = settings.openai_api_key
debug_mode = settings.debug

# Environment-specific configuration
if settings.environment == "production":
    # Production-specific settings
    pass
elif settings.environment == "development":
    # Development-specific settings
    pass
```

### Service Integration

```python
from graph_service.zep_graphiti import GraphitiService

# Initialize service
graphiti_service = GraphitiService(
    database_uri=settings.neo4j_uri,
    database_user=settings.neo4j_user,
    database_password=settings.neo4j_password,
    openai_api_key=settings.openai_api_key
)

# Use service in endpoints
async def add_episode_endpoint(episode_data):
    try:
        result = await graphiti_service.add_episode(episode_data)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to add episode: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Best Practices for Agents

1. **Configuration**: Use environment variables for configuration
2. **Error Handling**: Implement comprehensive error handling
3. **Logging**: Use structured logging for debugging and monitoring
4. **Validation**: Validate all inputs using DTOs
5. **Performance**: Monitor performance and optimize bottlenecks

### Application Lifecycle

```python
# Application startup
@app.on_event("startup")
async def startup_event():
    # Initialize database connections
    await graphiti_service.initialize()
    
    # Setup monitoring
    await setup_monitoring()
    
    # Warm up services
    await warm_up_services()

# Application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    await graphiti_service.cleanup()
    
    # Close connections
    await cleanup_connections()
```

### Error Handling

```python
from fastapi import HTTPException
from graph_service.exceptions import GraphitiServiceError

# Custom exception handler
@app.exception_handler(GraphitiServiceError)
async def graphiti_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Graphiti service error", "detail": str(exc)}
    )

# Service-level error handling
class GraphitiService:
    async def safe_operation(self, operation_func, *args, **kwargs):
        try:
            return await operation_func(*args, **kwargs)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Validation error: {e}")
        except ConnectionError as e:
            raise HTTPException(status_code=503, detail="Service unavailable")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
```

### Middleware Configuration

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts
)

# Custom logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} in {process_time:.3f}s")
    
    return response
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check including dependencies"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {}
    }
    
    # Check database connectivity
    try:
        await graphiti_service.check_database_connection()
        health_status["services"]["database"] = "healthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"
    
    # Check API dependencies
    try:
        await graphiti_service.check_llm_connectivity()
        health_status["services"]["llm"] = "healthy"
    except Exception as e:
        health_status["services"]["llm"] = f"unhealthy: {e}"
        health_status["status"] = "degraded"
    
    return health_status
```

### Performance Monitoring

```python
from prometheus_fastapi_instrumentator import Instrumentator

# Setup Prometheus monitoring
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Custom metrics
from prometheus_client import Counter, Histogram

# Request metrics
request_count = Counter('api_requests_total', 'Total API requests', ['method', 'endpoint'])
request_duration = Histogram('api_request_duration_seconds', 'Request duration')

# Custom monitoring middleware
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    # Track request count
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    
    # Track request duration
    with request_duration.time():
        response = await call_next(request)
    
    return response
```

### Service Testing

```python
from fastapi.testclient import TestClient
from graph_service.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_add_episode():
    episode_data = {
        "name": "Test Episode",
        "content": "Test content",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    response = client.post("/episodes", json=episode_data)
    assert response.status_code == 201
    assert "uuid" in response.json()

async def test_service_integration():
    # Test service methods directly
    service = GraphitiService()
    await service.initialize()
    
    try:
        result = await service.add_episode({
            "name": "Test",
            "content": "Test content"
        })
        assert result["uuid"] is not None
    finally:
        await service.cleanup()
```

### Development Workflow

```python
# Development server with auto-reload
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "graph_service.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="debug"
    )

# Production server configuration
production_config = {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,  # Multiple worker processes
    "log_level": "info",
    "access_log": True,
    "proxy_headers": True,
    "forwarded_allow_ips": "*"
}
```

### Environment Configuration

```python
# Configuration for different environments
class Settings(BaseSettings):
    # Database selection
    database_type: str = "neo4j"  # or "falkordb"
    
    # Neo4j settings
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    neo4j_database: str = "neo4j"
    
    # FalkorDB settings
    falkordb_host: str = "localhost"
    falkordb_port: int = 6379
    falkordb_username: Optional[str] = None
    falkordb_password: Optional[str] = None
    falkordb_database: str = "default_db"
    
    # API settings
    openai_api_key: str
    anthropic_api_key: Optional[str] = None
    
    # Server settings
    debug: bool = False
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Database driver factory
def create_database_driver(settings: Settings):
    if settings.database_type.lower() == "falkordb":
        from graphiti_core.driver import FalkorDBDriver
        return FalkorDBDriver(
            host=settings.falkordb_host,
            port=settings.falkordb_port,
            username=settings.falkordb_username,
            password=settings.falkordb_password,
            database=settings.falkordb_database
        )
    else:
        from graphiti_core.driver import Neo4jDriver
        return Neo4jDriver(
            uri=settings.neo4j_uri,
            user=settings.neo4j_user,
            password=settings.neo4j_password,
            database=settings.neo4j_database
        )
```

### Security Considerations

```python
# API key authentication
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

# Protected endpoint
@app.get("/protected-endpoint")
async def protected_endpoint(api_key: str = Depends(get_api_key)):
    return {"message": "Access granted"}

# Input validation
from pydantic import BaseModel, validator

class EpisodeCreate(BaseModel):
    name: str
    content: str
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v
    
    @validator('content')
    def content_length_check(cls, v):
        if len(v) > 100000:  # 100KB limit
            raise ValueError('Content too large')
        return v
```

### Best Practices Summary

1. **Configuration Management**: Use environment variables and validation
2. **Error Handling**: Implement comprehensive error handling at all levels
3. **Monitoring**: Include health checks, metrics, and logging
4. **Security**: Implement authentication, validation, and security headers
5. **Testing**: Include unit tests, integration tests, and performance tests