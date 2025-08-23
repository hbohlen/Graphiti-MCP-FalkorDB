# AGENTS.md

This file provides guidance to AI agents when working with API router components.

## Directory Overview

This directory contains FastAPI router modules that organize API endpoints by functionality, providing clean separation of concerns and modular endpoint management.

## Files

- `ingest.py` - API endpoints for data ingestion and content processing
- `retrieve.py` - API endpoints for data retrieval and search operations
- `__init__.py` - Module initialization and router exports

## Router Architecture

### Ingestion Router (`ingest.py`)

Handles data input operations:

1. **Episode Management**: Add, update, and manage episodes
2. **Bulk Operations**: Batch processing of multiple items
3. **Content Processing**: Text and structured data ingestion
4. **Validation**: Input validation and error handling
5. **Progress Tracking**: Long-running operation progress

### Retrieval Router (`retrieve.py`)

Handles data query operations:

1. **Search Operations**: Entity and relationship search
2. **Graph Traversal**: Navigate graph relationships
3. **Filtering**: Apply filters and constraints to queries
4. **Pagination**: Handle large result sets efficiently
5. **Export**: Data export and formatting

## Agent Guidelines

### Router Organization

```python
from fastapi import APIRouter, HTTPException, Depends
from graph_service.dto import EpisodeCreate, EpisodeResponse
from graph_service.zep_graphiti import GraphitiService

# Create router instance
ingest_router = APIRouter(prefix="/ingest", tags=["ingestion"])
retrieve_router = APIRouter(prefix="/retrieve", tags=["retrieval"])

# Include routers in main app
app.include_router(ingest_router)
app.include_router(retrieve_router)
```

### Ingestion Endpoints

```python
# Episode creation
@ingest_router.post("/episodes", response_model=EpisodeResponse)
async def create_episode(
    episode: EpisodeCreate,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Create a new episode in the knowledge graph"""
    try:
        result = await service.add_episode(episode.dict())
        return EpisodeResponse(**result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create episode: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Bulk episode creation
@ingest_router.post("/episodes/batch", response_model=List[EpisodeResponse])
async def create_episodes_batch(
    episodes: List[EpisodeCreate],
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Create multiple episodes in batch"""
    results = []
    errors = []
    
    for i, episode in enumerate(episodes):
        try:
            result = await service.add_episode(episode.dict())
            results.append(EpisodeResponse(**result))
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    
    if errors and not results:
        raise HTTPException(status_code=400, detail={"errors": errors})
    
    return results
```

### Retrieval Endpoints

```python
# Entity search
@retrieve_router.get("/entities/search", response_model=List[EntityResponse])
async def search_entities(
    query: str,
    entity_types: Optional[List[str]] = None,
    limit: int = 10,
    offset: int = 0,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Search for entities in the knowledge graph"""
    try:
        results = await service.search_entities(
            query=query,
            entity_types=entity_types,
            limit=limit,
            offset=offset
        )
        return [EntityResponse(**entity) for entity in results]
    except Exception as e:
        logger.error(f"Entity search failed: {e}")
        raise HTTPException(status_code=500, detail="Search failed")

# Relationship retrieval
@retrieve_router.get("/entities/{entity_id}/relationships")
async def get_entity_relationships(
    entity_id: str,
    relationship_types: Optional[List[str]] = None,
    limit: int = 50,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Get relationships for a specific entity"""
    try:
        relationships = await service.get_entity_relationships(
            entity_id=entity_id,
            relationship_types=relationship_types,
            limit=limit
        )
        return {"entity_id": entity_id, "relationships": relationships}
    except EntityNotFoundError:
        raise HTTPException(status_code=404, detail="Entity not found")
    except Exception as e:
        logger.error(f"Failed to get relationships: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve relationships")
```

### Best Practices for Agents

1. **Endpoint Organization**: Group related endpoints in appropriate routers
2. **Error Handling**: Implement consistent error handling across endpoints
3. **Documentation**: Use docstrings and response models for API documentation
4. **Validation**: Validate inputs using Pydantic models
5. **Dependencies**: Use FastAPI dependencies for common functionality

### Request/Response Patterns

```python
# Standard response pattern
from typing import Optional, List, Union
from pydantic import BaseModel

class StandardResponse(BaseModel):
    success: bool
    data: Optional[Union[dict, List[dict]]] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None

# Pagination pattern
class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool

# Error response pattern
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### Advanced Endpoint Patterns

```python
# Streaming responses for large datasets
from fastapi.responses import StreamingResponse
import json

@retrieve_router.get("/entities/export")
async def export_entities(
    format: str = "jsonl",
    entity_types: Optional[List[str]] = None,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Stream entity export"""
    async def generate_entities():
        async for entity in service.stream_entities(entity_types):
            if format == "jsonl":
                yield json.dumps(entity) + "\n"
            elif format == "csv":
                yield entity_to_csv_row(entity)
    
    return StreamingResponse(
        generate_entities(),
        media_type="application/json" if format == "jsonl" else "text/csv"
    )

# WebSocket endpoints for real-time updates
from fastapi import WebSocket

@retrieve_router.websocket("/entities/watch")
async def watch_entities(
    websocket: WebSocket,
    entity_types: Optional[List[str]] = None
):
    """WebSocket endpoint for real-time entity updates"""
    await websocket.accept()
    
    try:
        async for update in service.watch_entity_changes(entity_types):
            await websocket.send_json(update)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
```

### Authentication and Authorization

```python
from fastapi import Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> User:
    """Validate API token and return user"""
    token = credentials.credentials
    user = await validate_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Protected endpoint
@ingest_router.post("/episodes/premium")
async def create_premium_episode(
    episode: EpisodeCreate,
    user: User = Depends(get_current_user),
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Create episode with premium features"""
    if not user.has_premium_access:
        raise HTTPException(status_code=403, detail="Premium access required")
    
    result = await service.add_premium_episode(episode.dict(), user.id)
    return EpisodeResponse(**result)
```

### Caching Strategies

```python
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

# Cache search results
@retrieve_router.get("/entities/search")
@cache(expire=300)  # Cache for 5 minutes
async def cached_search_entities(
    query: str,
    entity_types: Optional[List[str]] = None,
    limit: int = 10,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Cached entity search"""
    results = await service.search_entities(query, entity_types, limit)
    return results

# Cache invalidation on updates
@ingest_router.post("/episodes")
async def create_episode_with_cache_invalidation(
    episode: EpisodeCreate,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Create episode and invalidate related caches"""
    result = await service.add_episode(episode.dict())
    
    # Invalidate related caches
    await FastAPICache.clear(namespace="search")
    await FastAPICache.clear(namespace="entities")
    
    return EpisodeResponse(**result)
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

# Apply rate limiting to endpoints
@retrieve_router.get("/entities/search")
@limiter.limit("10/minute")
async def rate_limited_search(
    request: Request,
    query: str,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Rate-limited entity search"""
    return await service.search_entities(query)

# Custom rate limit handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded", "detail": str(exc)}
    )
```

### Testing Router Endpoints

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

@pytest.fixture
def mock_service():
    service = AsyncMock(spec=GraphitiService)
    return service

@pytest.fixture
def client(mock_service):
    app.dependency_overrides[get_graphiti_service] = lambda: mock_service
    return TestClient(app)

def test_create_episode(client, mock_service):
    # Setup mock
    mock_service.add_episode.return_value = {
        "uuid": "test-uuid",
        "name": "Test Episode"
    }
    
    # Test endpoint
    response = client.post("/ingest/episodes", json={
        "name": "Test Episode",
        "content": "Test content"
    })
    
    assert response.status_code == 200
    assert response.json()["uuid"] == "test-uuid"
    mock_service.add_episode.assert_called_once()

def test_search_entities(client, mock_service):
    # Setup mock
    mock_service.search_entities.return_value = [
        {"uuid": "entity-1", "name": "Entity 1", "type": "Person"}
    ]
    
    # Test endpoint
    response = client.get("/retrieve/entities/search?query=test")
    
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Entity 1"
```

### Performance Optimization

```python
# Async batch operations
@ingest_router.post("/episodes/parallel-batch")
async def create_episodes_parallel(
    episodes: List[EpisodeCreate],
    max_concurrent: int = 10,
    service: GraphitiService = Depends(get_graphiti_service)
):
    """Create episodes with parallel processing"""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_episode(episode):
        async with semaphore:
            return await service.add_episode(episode.dict())
    
    # Process episodes in parallel
    tasks = [process_episode(episode) for episode in episodes]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Separate successful results from errors
    successful = []
    errors = []
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            errors.append({"index": i, "error": str(result)})
        else:
            successful.append(result)
    
    return {
        "successful": successful,
        "errors": errors,
        "total_processed": len(episodes)
    }
```

### Best Practices Summary

1. **Router Organization**: Separate concerns into logical router modules
2. **Consistent Patterns**: Use consistent request/response patterns across endpoints
3. **Error Handling**: Implement comprehensive error handling with proper HTTP status codes
4. **Documentation**: Provide clear documentation and examples for all endpoints
5. **Performance**: Optimize for performance with caching, rate limiting, and parallel processing