# AGENTS.md

This file provides guidance to AI agents when working with the core Graphiti library.

## Directory Overview

This directory contains the core Graphiti library implementation with all fundamental components for building and managing temporally-aware knowledge graphs.

## Core Components

### Main Files

- `graphiti.py` - Main Graphiti class that orchestrates all functionality
- `nodes.py` - Core graph node data structures and models
- `edges.py` - Core graph edge data structures and relationships
- `errors.py` - Custom exception classes for error handling
- `graph_queries.py` - Database query templates and graph operations
- `graphiti_types.py` - Type definitions and data models
- `helpers.py` - Utility functions and helper methods

### Subdirectories

- `driver/` - Database drivers for Neo4j and FalkorDB
- `llm_client/` - LLM integration for OpenAI, Anthropic, Gemini, Groq
- `embedder/` - Embedding clients for various providers
- `search/` - Hybrid search implementation with configurable strategies
- `prompts/` - LLM prompts for entity extraction and processing
- `utils/` - Maintenance operations and utility functions
- `models/` - Data models for nodes and edges
- `cross_encoder/` - Cross-encoder models for relevance scoring
- `telemetry/` - Telemetry and monitoring functionality

## Agent Guidelines

### Working with Core Components

1. **Entry Point**: Start with `graphiti.py` to understand the main API
2. **Data Models**: Study `nodes.py` and `edges.py` for graph structures
3. **Database Integration**: Use appropriate drivers from `driver/` directory
4. **LLM Operations**: Leverage `llm_client/` for AI-powered features
5. **Search Capabilities**: Utilize `search/` for advanced retrieval

### Key Concepts

1. **Bi-temporal Model**: Understanding how time is tracked in the graph
2. **Entity Extraction**: How LLMs extract entities and relationships
3. **Hybrid Search**: Combination of semantic, keyword, and graph-based search
4. **Graph Operations**: CRUD operations on nodes and edges
5. **Provider Abstraction**: How different backends are abstracted

### Development Patterns

```python
# Basic usage pattern
from graphiti_core import Graphiti
from graphiti_core.driver import Neo4jDriver

# Initialize with driver
driver = Neo4jDriver(uri="bolt://localhost:7687", user="neo4j", password="password")
graphiti = Graphiti(driver=driver)

# Add episode
await graphiti.add_episode(
    name="Episode Name",
    content="Episode content...",
    timestamp=datetime.utcnow()
)

# Search for information
results = await graphiti.search(query="search query")
```

### Best Practices for Agents

1. **Async Operations**: Most operations are async, use proper await patterns
2. **Error Handling**: Use custom exceptions from `errors.py`
3. **Type Safety**: Leverage type definitions from `graphiti_types.py`
4. **Resource Management**: Properly manage database connections and resources
5. **Testing**: Use test utilities and mock objects for unit testing

### Core Architecture Principles

- **Modularity**: Each component has a specific responsibility
- **Extensibility**: Easy to add new drivers, LLM clients, or search strategies
- **Type Safety**: Strong typing throughout the codebase
- **Performance**: Optimized for large-scale graph operations
- **Reliability**: Robust error handling and edge case management

### Integration Points

1. **Database Layer**: `driver/` provides abstraction over different graph databases
   - **Neo4j Driver**: Production-ready, enterprise features, complex queries
   - **FalkorDB Driver**: Lightweight, Redis-based, development-friendly
2. **AI Layer**: `llm_client/` and `embedder/` handle AI operations
3. **Search Layer**: `search/` combines multiple search strategies
4. **Data Layer**: `models/` define the structure of graph elements
5. **Utility Layer**: `utils/` provide common operations and maintenance

### Performance Considerations

- **Batch Operations**: Use bulk operations when possible
- **Connection Pooling**: Manage database connections efficiently
- **Caching**: Leverage caching for frequently accessed data
- **Parallel Processing**: Use async operations for concurrent tasks
- **Memory Management**: Monitor memory usage with large graphs

#### Database-Specific Performance

**Neo4j Performance:**
- Optimize Cypher queries for large datasets
- Use appropriate indexes and constraints
- Consider parallel runtime for enterprise deployments
- Monitor memory usage and heap settings

**FalkorDB Performance:**
- Leverage in-memory operations for speed
- Consider Redis persistence settings
- Monitor Redis memory usage
- Use connection pooling for high throughput

### Testing and Debugging

- Use test utilities in the test directories
- Enable logging for debugging operations
- Monitor telemetry data for performance insights
- Validate data integrity after operations
- Test with different database backends

### Extension Guidelines

- Follow existing patterns when adding new components
- Maintain compatibility with existing interfaces
- Add proper type annotations and documentation
- Include comprehensive tests for new functionality
- Consider performance implications of new features