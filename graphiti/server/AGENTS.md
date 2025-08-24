# AGENTS.md

This file provides guidance to AI agents when working with the Graphiti server components.

## Directory Overview

This directory contains the FastAPI-based REST API server that provides HTTP endpoints for accessing Graphiti functionality. It enables integration with web applications, microservices, and other systems that need to interact with knowledge graphs via HTTP APIs.

## Server Architecture

### FastAPI Service

The server provides:

1. **REST API Endpoints**: HTTP endpoints for graph operations
2. **Data Transfer Objects (DTOs)**: Structured API request/response models
3. **Routers**: Organized endpoint routing for different functionalities
4. **Middleware**: Authentication, logging, and request processing
5. **Documentation**: Automatic OpenAPI/Swagger documentation

### Key Components

- `graph_service/main.py` - Main FastAPI application and server setup
- `graph_service/routers/` - API endpoint routing modules
- `graph_service/dto/` - Data transfer objects for API contracts

## Agent Guidelines

### Server Development Setup

```bash
cd server/
# Install server dependencies
uv sync --extra dev

# Run server in development mode
uvicorn graph_service.main:app --reload

# Access API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

### API Endpoint Categories

1. **Episode Management**: Add, retrieve, and manage episodes
2. **Entity Operations**: Create, update, and search entities
3. **Relationship Management**: Manage entity relationships
4. **Search Operations**: Search nodes, edges, and perform hybrid search
5. **Graph Maintenance**: Administrative and maintenance operations

### Best Practices for Agents

1. **API Documentation**: Always check Swagger/OpenAPI docs for current endpoints
2. **Error Handling**: Implement proper HTTP error handling
3. **Authentication**: Use appropriate authentication mechanisms
4. **Rate Limiting**: Respect API rate limits and implement backoff
5. **Validation**: Validate request/response data against DTOs

### Common API Operations

#### Episode Management
```python
import httpx

# Add episode via API
async def add_episode_via_api(episode_data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/episodes",
            json={
                "name": episode_data["name"],
                "content": episode_data["content"],
                "timestamp": episode_data["timestamp"].isoformat()
            }
        )
        return response.json()

# Retrieve episodes
async def get_episodes():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/episodes")
        return response.json()
```

#### Entity Search
```python
# Search entities via API
async def search_entities_api(query, entity_types=None):
    async with httpx.AsyncClient() as client:
        params = {"query": query}
        if entity_types:
            params["entity_types"] = entity_types
        
        response = await client.get(
            "http://localhost:8000/entities/search",
            params=params
        )
        return response.json()
```

#### Relationship Queries
```python
# Get entity relationships via API
async def get_entity_relationships(entity_uuid):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/entities/{entity_uuid}/relationships"
        )
        return response.json()
```

### Server Configuration

#### Neo4j Configuration
```python
# Example server configuration for Neo4j
server_config = {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "log_level": "info",
    "access_log": True,
    "cors_enabled": True,
    "cors_origins": ["http://localhost:3000", "https://myapp.com"]
}

# Neo4j environment variables
environment_vars = {
    "OPENAI_API_KEY": "your-openai-key",
    "NEO4J_URI": "bolt://localhost:7687",
    "NEO4J_USER": "neo4j",
    "NEO4J_PASSWORD": "password",
    "LOG_LEVEL": "INFO"
}
```

#### FalkorDB Configuration
```python
# Example server configuration for FalkorDB
server_config = {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "log_level": "info",
    "access_log": True,
    "cors_enabled": True,
    "cors_origins": ["http://localhost:3000", "https://myapp.com"]
}

# FalkorDB environment variables
environment_vars = {
    "OPENAI_API_KEY": "your-openai-key",
    "FALKORDB_HOST": "localhost",
    "FALKORDB_PORT": "6379",
    "FALKORDB_USERNAME": "",  # optional
    "FALKORDB_PASSWORD": "",  # optional
    "FALKORDB_DATABASE": "default_db",
    "DATABASE_TYPE": "falkordb",
    "LOG_LEVEL": "INFO"
}
```

### Docker Deployment

#### Neo4j Docker Setup
```yaml
# Example docker-compose.yml setup for Neo4j
version: '3.8'

services:
  graphiti-server:
    image: zepai/graphiti:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=${NEO4J_USER}
      - NEO4J_PASSWORD=${NEO4J_PASSWORD}
    depends_on:
      - neo4j

  neo4j:
    image: neo4j:5.22.0
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=${NEO4J_USER}/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

#### FalkorDB Docker Setup
```yaml
# Example docker-compose.yml setup for FalkorDB
version: '3.8'

services:
  graphiti-server:
    image: zepai/graphiti:latest
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FALKORDB_HOST=falkordb
      - FALKORDB_PORT=6379
      - DATABASE_TYPE=falkordb
    depends_on:
      - falkordb

  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"  # Redis protocol
    volumes:
      - falkordb_data:/data

volumes:
  falkordb_data:
```

### API Client Development

```python
class GraphitiAPIClient:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def add_episode(self, name, content, timestamp=None):
        async with httpx.AsyncClient() as client:
            data = {"name": name, "content": content}
            if timestamp:
                data["timestamp"] = timestamp.isoformat()
            
            response = await client.post(
                f"{self.base_url}/episodes",
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def search_entities(self, query, limit=10):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/entities/search",
                params={"query": query, "limit": limit},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_entity_relationships(self, entity_uuid):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/entities/{entity_uuid}/relationships",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
```

### Error Handling

```python
# Robust API error handling
async def safe_api_call(api_func, *args, **kwargs):
    try:
        return await api_func(*args, **kwargs)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise AuthenticationError("Invalid API credentials")
        elif e.response.status_code == 404:
            raise NotFoundError("Resource not found")
        elif e.response.status_code == 429:
            raise RateLimitError("API rate limit exceeded")
        elif e.response.status_code >= 500:
            raise ServerError("Server error occurred")
        else:
            raise APIError(f"API error: {e.response.status_code}")
    except httpx.ConnectError:
        raise ConnectionError("Cannot connect to Graphiti server")
    except httpx.TimeoutException:
        raise TimeoutError("API request timed out")
```

### Performance Optimization

```python
# Optimize API performance
class OptimizedAPIClient:
    def __init__(self, base_url, max_connections=100):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=max_connections),
            timeout=httpx.Timeout(30.0)
        )
    
    async def batch_add_episodes(self, episodes):
        # Use batch endpoint for better performance
        response = await self.client.post(
            f"{self.base_url}/episodes/batch",
            json={"episodes": episodes}
        )
        return response.json()
    
    async def parallel_searches(self, queries):
        # Execute multiple searches in parallel
        tasks = [
            self.search_entities(query) for query in queries
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    async def close(self):
        await self.client.aclose()
```

### Monitoring and Health Checks

```python
# Health check endpoint usage
async def check_server_health():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            health_data = response.json()
            
            if health_data["status"] == "healthy":
                return True
            else:
                logger.warning(f"Server health issue: {health_data}")
                return False
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

# Monitor API performance
class APIMonitor:
    def __init__(self):
        self.metrics = {
            "request_count": 0,
            "error_count": 0,
            "total_latency": 0
        }
    
    async def tracked_request(self, request_func, *args, **kwargs):
        start_time = time.time()
        self.metrics["request_count"] += 1
        
        try:
            result = await request_func(*args, **kwargs)
            latency = time.time() - start_time
            self.metrics["total_latency"] += latency
            return result
        except Exception as e:
            self.metrics["error_count"] += 1
            raise
    
    def get_stats(self):
        if self.metrics["request_count"] > 0:
            avg_latency = self.metrics["total_latency"] / self.metrics["request_count"]
            error_rate = self.metrics["error_count"] / self.metrics["request_count"]
            return {
                "average_latency": avg_latency,
                "error_rate": error_rate,
                "total_requests": self.metrics["request_count"]
            }
        return {"no_data": True}
```

### Testing API Endpoints

```python
import pytest

@pytest.mark.asyncio
async def test_episode_creation():
    client = GraphitiAPIClient("http://localhost:8000")
    
    episode_data = {
        "name": "Test Episode",
        "content": "This is a test episode for API testing"
    }
    
    # Create episode
    result = await client.add_episode(**episode_data)
    assert "uuid" in result
    assert result["name"] == episode_data["name"]
    
    # Verify episode exists
    episodes = await client.get_episodes()
    episode_uuids = [ep["uuid"] for ep in episodes]
    assert result["uuid"] in episode_uuids

@pytest.mark.asyncio 
async def test_entity_search():
    client = GraphitiAPIClient("http://localhost:8000")
    
    # Search for entities
    results = await client.search_entities("test entity", limit=5)
    assert isinstance(results, list)
    assert len(results) <= 5
    
    # Verify result structure
    if results:
        assert "uuid" in results[0]
        assert "name" in results[0]
        assert "type" in results[0]
```

### Integration Patterns

Common integration patterns with the server:

1. **Web Applications**: Frontend apps consuming the REST API
2. **Microservices**: Other services interacting with knowledge graph
3. **ETL Pipelines**: Data processing pipelines feeding into Graphiti
4. **Analytics Systems**: Analytics tools querying graph data
5. **Mobile Applications**: Mobile apps accessing graph functionality

### Best Practices Summary

1. **API Documentation**: Use Swagger/OpenAPI docs for accurate endpoint information
2. **Error Handling**: Implement comprehensive error handling for all API calls
3. **Performance**: Use batch operations and parallel requests for better performance
4. **Monitoring**: Monitor API health and performance metrics
5. **Security**: Implement proper authentication and input validation