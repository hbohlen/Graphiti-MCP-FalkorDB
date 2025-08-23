# AGENTS.md

This file provides guidance to AI agents when working with Data Transfer Object (DTO) components.

## Directory Overview

This directory contains Pydantic models that define the structure of API requests and responses, ensuring type safety, validation, and consistent data contracts for the Graphiti REST API.

## Files

- `common.py` - Common DTO models shared across multiple endpoints
- `ingest.py` - DTO models for data ingestion and content processing endpoints
- `retrieve.py` - DTO models for data retrieval and search endpoints
- `__init__.py` - Module initialization and DTO exports

## DTO Architecture

### Purpose and Benefits

DTOs provide:

1. **Type Safety**: Strong typing for API contracts
2. **Validation**: Automatic validation of request/response data
3. **Documentation**: Self-documenting API through model definitions
4. **Serialization**: Automatic JSON serialization/deserialization
5. **Consistency**: Consistent data structures across API endpoints

### Model Categories

1. **Request Models**: Define structure of incoming API requests
2. **Response Models**: Define structure of API responses
3. **Common Models**: Shared models used across multiple endpoints
4. **Nested Models**: Complex models with nested relationships
5. **Validation Models**: Models with custom validation logic

## Agent Guidelines

### Common DTOs (`common.py`)

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

# Base response model
class BaseResponse(BaseModel):
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

# Pagination model
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(10, ge=1, le=100, description="Page size")
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    size: int
    
    @property
    def has_next(self) -> bool:
        return self.page * self.size < self.total
    
    @property
    def has_prev(self) -> bool:
        return self.page > 1

# Error models
class ErrorDetail(BaseModel):
    code: str
    message: str
    field: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

### Ingestion DTOs (`ingest.py`)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime

# Episode creation models
class EpisodeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Episode name")
    content: str = Field(..., min_length=1, description="Episode content")
    timestamp: Optional[datetime] = Field(None, description="Episode timestamp")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace only')
        return v.strip()
    
    @validator('content')
    def content_length_check(cls, v):
        if len(v) > 100000:  # 100KB limit
            raise ValueError('Content exceeds maximum length of 100KB')
        return v
    
    @validator('metadata')
    def validate_metadata(cls, v):
        if v is not None and len(v) > 50:
            raise ValueError('Metadata cannot have more than 50 fields')
        return v

class EpisodeResponse(BaseModel):
    uuid: str
    name: str
    content: str
    timestamp: datetime
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

# Batch operation models
class BatchEpisodeCreate(BaseModel):
    episodes: List[EpisodeCreate] = Field(..., min_items=1, max_items=100)
    
    @validator('episodes')
    def validate_batch_size(cls, v):
        if len(v) > 100:
            raise ValueError('Batch size cannot exceed 100 episodes')
        return v

class BatchEpisodeResponse(BaseModel):
    successful: List[EpisodeResponse]
    failed: List[Dict[str, Any]]
    total_processed: int
    
    @property
    def success_rate(self) -> float:
        if self.total_processed == 0:
            return 0.0
        return len(self.successful) / self.total_processed
```

### Retrieval DTOs (`retrieve.py`)

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum

# Search parameters
class SearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    entity_types: Optional[List[str]] = Field(None, description="Filter by entity types")
    limit: int = Field(10, ge=1, le=100, description="Maximum results to return")
    offset: int = Field(0, ge=0, description="Number of results to skip")
    
    @validator('entity_types')
    def validate_entity_types(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError('Cannot filter by more than 10 entity types')
        return v

# Entity models
class EntityResponse(BaseModel):
    uuid: str
    name: str
    type: str
    summary: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class EntitySearchResponse(BaseModel):
    entities: List[EntityResponse]
    total: int
    query: str
    search_metadata: Optional[Dict[str, Any]] = None

# Relationship models
class RelationshipResponse(BaseModel):
    uuid: str
    source_uuid: str
    target_uuid: str
    relationship_type: str
    summary: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None

class EntityRelationshipsResponse(BaseModel):
    entity_uuid: str
    relationships: List[RelationshipResponse]
    total: int

# Search filters
class SearchFilters(BaseModel):
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    confidence_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata_filters: Optional[Dict[str, Any]] = None
    
    @validator('date_to')
    def validate_date_range(cls, v, values):
        if v is not None and 'date_from' in values and values['date_from'] is not None:
            if v <= values['date_from']:
                raise ValueError('date_to must be after date_from')
        return v
```

### Best Practices for Agents

1. **Validation**: Use appropriate validators for data integrity
2. **Documentation**: Include clear field descriptions
3. **Type Safety**: Use specific types rather than generic Any
4. **Constraints**: Apply reasonable field constraints (length, ranges)
5. **Consistency**: Maintain consistent naming and structure patterns

### Advanced DTO Patterns

```python
# Conditional validation
class ConditionalModel(BaseModel):
    operation_type: str
    data: Dict[str, Any]
    
    @validator('data')
    def validate_data_by_operation(cls, v, values):
        operation_type = values.get('operation_type')
        
        if operation_type == 'create_entity':
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in v:
                    raise ValueError(f'{field} is required for {operation_type}')
        elif operation_type == 'create_relationship':
            required_fields = ['source_uuid', 'target_uuid', 'type']
            for field in required_fields:
                if field not in v:
                    raise ValueError(f'{field} is required for {operation_type}')
        
        return v

# Custom serialization
class CustomSerializationModel(BaseModel):
    sensitive_data: str
    public_data: str
    
    def dict(self, include_sensitive: bool = False, **kwargs):
        d = super().dict(**kwargs)
        if not include_sensitive:
            d.pop('sensitive_data', None)
        return d
    
    class Config:
        @staticmethod
        def schema_extra(schema: Dict[str, Any], model_type):
            # Customize OpenAPI schema
            schema.setdefault('examples', [
                {
                    "public_data": "This is public",
                    "sensitive_data": "This is sensitive"
                }
            ])

# Polymorphic models
from typing import Union

class BaseEvent(BaseModel):
    event_type: str
    timestamp: datetime

class UserEvent(BaseEvent):
    event_type: str = "user"
    user_id: str
    action: str

class SystemEvent(BaseEvent):
    event_type: str = "system"
    service: str
    level: str

Event = Union[UserEvent, SystemEvent]

class EventResponse(BaseModel):
    events: List[Event]
```

### Input Validation and Sanitization

```python
import re
from pydantic import validator

class SecureInput(BaseModel):
    text_content: str
    html_content: Optional[str] = None
    
    @validator('text_content')
    def sanitize_text(cls, v):
        # Remove potentially harmful characters
        sanitized = re.sub(r'[<>"\']', '', v)
        return sanitized.strip()
    
    @validator('html_content')
    def validate_html(cls, v):
        if v is not None:
            # Basic HTML validation/sanitization
            if '<script>' in v.lower() or 'javascript:' in v.lower():
                raise ValueError('HTML content contains potentially harmful elements')
        return v

class FileUpload(BaseModel):
    filename: str
    content_type: str
    size: int
    
    @validator('filename')
    def validate_filename(cls, v):
        # Check for path traversal attempts
        if '..' in v or '/' in v or '\\' in v:
            raise ValueError('Invalid filename')
        return v
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = [
            'text/plain', 'text/csv', 'application/json',
            'application/pdf', 'image/jpeg', 'image/png'
        ]
        if v not in allowed_types:
            raise ValueError(f'Content type {v} not allowed')
        return v
    
    @validator('size')
    def validate_file_size(cls, v):
        max_size = 10 * 1024 * 1024  # 10MB
        if v > max_size:
            raise ValueError('File size exceeds maximum allowed size')
        return v
```

### Response Formatting

```python
# Standardized API responses
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def success_response(cls, data: Any, metadata: Dict[str, Any] = None):
        return cls(success=True, data=data, metadata=metadata)
    
    @classmethod
    def error_response(cls, error: str, metadata: Dict[str, Any] = None):
        return cls(success=False, error=error, metadata=metadata)

# Typed response wrappers
from typing import TypeVar, Generic

T = TypeVar('T')

class TypedResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    
    class Config:
        # This allows the model to work with generics
        arbitrary_types_allowed = True

# Usage examples
EpisodeListResponse = TypedResponse[List[EpisodeResponse]]
EntitySearchResponseTyped = TypedResponse[EntitySearchResponse]
```

### Testing DTOs

```python
import pytest
from pydantic import ValidationError

def test_episode_create_validation():
    # Valid episode
    valid_episode = EpisodeCreate(
        name="Test Episode",
        content="This is test content"
    )
    assert valid_episode.name == "Test Episode"
    
    # Invalid episode - empty name
    with pytest.raises(ValidationError) as exc_info:
        EpisodeCreate(name="", content="Test content")
    
    assert "Name cannot be empty" in str(exc_info.value)
    
    # Invalid episode - content too long
    with pytest.raises(ValidationError):
        EpisodeCreate(
            name="Test",
            content="x" * 100001  # Exceeds limit
        )

def test_pagination_params():
    # Valid pagination
    pagination = PaginationParams(page=2, size=20)
    assert pagination.offset == 20
    
    # Invalid pagination - negative page
    with pytest.raises(ValidationError):
        PaginationParams(page=-1, size=10)
    
    # Invalid pagination - size too large
    with pytest.raises(ValidationError):
        PaginationParams(page=1, size=101)

def test_response_serialization():
    episode = EpisodeResponse(
        uuid="test-uuid",
        name="Test Episode",
        content="Test content",
        timestamp=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    
    # Test JSON serialization
    json_data = episode.model_dump_json()
    assert "test-uuid" in json_data
    
    # Test deserialization
    parsed = EpisodeResponse.model_validate_json(json_data)
    assert parsed.uuid == "test-uuid"
```

### Best Practices Summary

1. **Comprehensive Validation**: Use validators to ensure data integrity
2. **Clear Documentation**: Include descriptions for all fields
3. **Type Safety**: Use specific types and avoid generic Any when possible
4. **Security**: Implement input sanitization and validation
5. **Testing**: Thoroughly test DTO validation and serialization