# AGENTS.md

This file provides guidance to AI agents when working with signature and type definition files.

## Directory Overview

This directory contains signature files and type definitions that provide type information for external tools, IDEs, and static analysis tools.

## Signatures Purpose

### Type Information

Signature files provide:

1. **Type Definitions**: External type information for libraries
2. **Interface Specifications**: API contracts and interfaces
3. **Static Analysis**: Support for type checkers and linters
4. **IDE Support**: Enhanced autocomplete and error detection
5. **Documentation**: Type-based documentation generation

### Version Management

- `version1/` - Type signatures for API version 1
- Future versions can be added as needed

## Agent Guidelines

### Working with Signatures

1. **Type Safety**: Use signatures to understand expected types
2. **API Contracts**: Reference signatures for API compatibility
3. **Version Compatibility**: Check signature versions for compatibility
4. **IDE Integration**: Leverage signatures for better development experience
5. **Documentation**: Use signatures to understand interfaces

### Type Definition Patterns

#### Function Signatures

```python
# Example function signature
def process_episode(
    name: str,
    content: str,
    timestamp: Optional[datetime] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> EpisodeResult:
    """Process an episode and return result."""
    ...

# Async function signature
async def search_entities(
    query: str,
    entity_types: Optional[List[str]] = None,
    limit: int = 10
) -> List[EntityNode]:
    """Search for entities matching query."""
    ...
```

#### Class Signatures

```python
# Example class signature
class GraphitiClient:
    """Client for interacting with Graphiti API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = 30
    ) -> None:
        """Initialize client."""
        ...
    
    async def add_episode(
        self,
        episode: EpisodeCreate
    ) -> EpisodeResponse:
        """Add new episode."""
        ...
    
    async def search_nodes(
        self,
        query: str,
        filters: Optional[SearchFilters] = None
    ) -> List[EntityNode]:
        """Search nodes."""
        ...
```

#### Protocol Definitions

```python
# Example protocol signature
from typing import Protocol

class EmbedderProtocol(Protocol):
    """Protocol for embedding providers."""
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        ...
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        ...
    
    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        ...
```

### Best Practices for Agents

1. **Type Checking**: Use type checkers (mypy, pyright) with signatures
2. **Version Awareness**: Check signature versions for compatibility
3. **Documentation**: Reference signatures for understanding APIs
4. **IDE Configuration**: Configure IDEs to use signature files
5. **Validation**: Validate code against signature contracts

### Signature File Structure

#### Module Signatures

```python
# graphiti_client.pyi
from typing import Optional, List, Dict, Any
from datetime import datetime

class Graphiti:
    def __init__(
        self,
        driver: DatabaseDriver,
        llm_client: Optional[LLMClient] = None,
        embedder: Optional[Embedder] = None
    ) -> None: ...
    
    async def add_episode(
        self,
        name: str,
        content: str,
        timestamp: Optional[datetime] = None
    ) -> Episode: ...
    
    async def search_nodes(
        self,
        query: str,
        entity_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[EntityNode]: ...
```

#### Data Model Signatures

```python
# models.pyi
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class EntityNode:
    uuid: str
    name: str
    type: str
    summary: Optional[str]
    created_at: datetime
    metadata: Optional[Dict[str, Any]]
    
    def __init__(
        self,
        name: str,
        type: str,
        summary: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None: ...

class RelationshipEdge:
    uuid: str
    source_uuid: str
    target_uuid: str
    relationship_type: str
    summary: Optional[str]
    created_at: datetime
    
    def __init__(
        self,
        source_uuid: str,
        target_uuid: str,
        relationship_type: str,
        summary: Optional[str] = None
    ) -> None: ...
```

### IDE Integration

#### VS Code Configuration

```json
// .vscode/settings.json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.stubPath": "./signatures",
    "python.analysis.typeshedPaths": [
        "./signatures"
    ]
}
```

#### PyCharm Configuration

```python
# Configure PyCharm to use signature files
# File -> Settings -> Project -> Python Interpreter
# Add signature directory to interpreter paths
```

### Type Checking

#### MyPy Configuration

```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# Use signature files
mypy_path = signatures/version1
```

#### Pyright Configuration

```json
// pyrightconfig.json
{
    "pythonVersion": "3.11",
    "typeCheckingMode": "basic",
    "stubPath": "signatures/version1",
    "reportMissingTypeStubs": false
}
```

### Version Management

#### Version 1 Signatures

Current stable API signatures:

```python
# version1/__init__.pyi
"""Type signatures for Graphiti API version 1."""

from .client import Graphiti
from .models import EntityNode, RelationshipEdge
from .search import SearchConfig, SearchFilters

__all__ = [
    "Graphiti",
    "EntityNode", 
    "RelationshipEdge",
    "SearchConfig",
    "SearchFilters"
]
```

#### Version Compatibility

```python
# Check version compatibility
def check_signature_compatibility(required_version: str) -> bool:
    """Check if signature version is compatible."""
    current_version = "1.0.0"
    # Version compatibility logic
    return compare_versions(current_version, required_version)
```

### Documentation Generation

#### Sphinx Integration

```python
# docs/conf.py
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints'
]

# Use signature files for type hints
autodoc_type_aliases = {
    'EntityNode': 'graphiti.models.EntityNode',
    'RelationshipEdge': 'graphiti.models.RelationshipEdge'
}
```

#### API Documentation

```python
# Generate API docs from signatures
def generate_api_docs():
    """Generate API documentation from signature files."""
    # Parse signature files
    # Generate markdown/HTML documentation
    # Include type information and examples
    pass
```

### Testing Signatures

#### Type Validation Tests

```python
# test_signatures.py
import mypy.api

def test_signature_validity():
    """Test that signature files are valid."""
    result = mypy.api.run([
        '--config-file', 'mypy.ini',
        'signatures/version1/'
    ])
    
    assert result[2] == 0, "Signature files contain type errors"

def test_api_compatibility():
    """Test that implementation matches signatures."""
    # Compare actual implementation with signatures
    # Ensure API compatibility
    pass
```

#### Runtime Type Checking

```python
from typing import get_type_hints
import inspect

def validate_function_signature(func, signature_func):
    """Validate that function matches its signature."""
    actual_hints = get_type_hints(func)
    expected_hints = get_type_hints(signature_func)
    
    assert actual_hints == expected_hints, f"Signature mismatch for {func.__name__}"
```

### Signature Maintenance

#### Updating Signatures

```python
# When updating API:
# 1. Update implementation
# 2. Update corresponding signature files
# 3. Run type checking tests
# 4. Update version if breaking changes
```

#### Automated Generation

```python
# Generate signatures from implementation
def generate_signatures_from_code():
    """Auto-generate signature files from implementation."""
    # Parse Python code
    # Extract type information
    # Generate .pyi files
    pass
```

### Error Handling

#### Type Error Resolution

```python
# Common type errors and solutions:

# Missing type annotations
def process_data(data):  # Error: missing types
    pass

def process_data(data: Dict[str, Any]) -> None:  # Fixed
    pass

# Incorrect return types
def get_entities() -> EntityNode:  # Error: returns List
    return [entity1, entity2]

def get_entities() -> List[EntityNode]:  # Fixed
    return [entity1, entity2]
```

### Best Practices Summary

1. **Consistency**: Maintain consistent type signatures across versions
2. **Documentation**: Use signatures to document API contracts
3. **Validation**: Regular validation of signatures against implementation
4. **Version Management**: Proper versioning for API changes
5. **Tool Integration**: Configure development tools to use signatures effectively