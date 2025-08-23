# AGENTS.md

This file provides guidance to AI agents when working with the MCP (Model Context Protocol) server.

## Directory Overview

This directory contains the Model Context Protocol server implementation that allows AI assistants (like Claude, Cursor, and other MCP clients) to interact with Graphiti's knowledge graph capabilities through the MCP protocol.

## Key Features

The Graphiti MCP server provides:

1. **Episode Management**: Add, retrieve, and delete episodes (text, messages, or JSON data)
2. **Entity Management**: Search and manage entity nodes and relationships in the knowledge graph
3. **Search Capabilities**: Search for facts (edges) and node summaries using semantic and hybrid search
4. **Group Management**: Organize and manage groups of related data with group_id filtering
5. **Graph Maintenance**: Clear the graph and rebuild indices

## MCP Server Architecture

### Server Implementation

The MCP server exposes Graphiti functionality through standardized MCP tools:

- **Memory Tools**: `add_memory`, `search_memories` for episode management
- **Entity Tools**: `search_nodes`, `search_facts` for entity and relationship queries
- **Maintenance Tools**: `clear_graph` for graph operations
- **Group Tools**: Group-based filtering and organization

### Integration Patterns

Common integration patterns:

1. **AI Assistant Memory**: Persistent memory for conversational AI
2. **Knowledge Base**: Searchable knowledge repository
3. **Context Management**: Maintaining context across sessions
4. **Information Retrieval**: Semantic search and fact discovery

## Agent Guidelines

### Basic Usage

The MCP server follows the patterns established in `cursor_rules.md`:

1. **Always search first**: Use search tools before adding new information
2. **Use specific filters**: Apply entity type filters (`Preference`, `Procedure`, `Requirement`)
3. **Store immediately**: Use `add_memory` to store new information right away
4. **Follow procedures**: Respect discovered procedures and established preferences

### MCP Client Configuration

#### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8000/sse"
      ]
    }
  }
}
```

#### Cursor IDE Configuration

Set up the MCP server endpoint in your Cursor settings:
- Server URL: `http://localhost:8000/sse`
- Protocol: Server-Sent Events (SSE)

### Server Setup and Deployment

#### Docker Deployment

```bash
cd mcp_server/
docker compose up
```

This starts:
- Graphiti MCP server on port 8000
- Neo4j database for graph storage
- Automatic MCP server registration

#### Local Development

```bash
cd mcp_server/
# Install dependencies
uv sync

# Set environment variables
export OPENAI_API_KEY=your_key
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# Run server
python graphiti_mcp_server.py
```

### Best Practices for Agents

#### Memory Management

1. **Search Before Adding**: Always search existing knowledge before creating new entries
2. **Specific Queries**: Use specific, well-structured search queries
3. **Entity Type Filtering**: Use entity type filters for targeted searches
4. **Immediate Storage**: Store new information as soon as it's discovered

#### Information Organization

```python
# Good: Specific entity type search
search_nodes(
    query="user preferences for notification settings",
    entity_types=["Preference"]
)

# Good: Contextual fact search
search_facts(
    query="collaboration between engineering teams",
    entity_types=["Team", "Project"]
)

# Good: Immediate storage of new information
add_memory(
    content="User prefers email notifications over push notifications",
    entity_types=["Preference"]
)
```

#### Context Preservation

1. **Group Management**: Use group_id for organizing related information
2. **Temporal Context**: Include temporal information in memories
3. **Relationship Tracking**: Store relationships between entities
4. **Procedure Documentation**: Document established procedures

### Common MCP Operations

#### Adding Memory

```python
# Add structured information
await add_memory(
    content="John Doe prefers morning meetings and uses VS Code for development",
    entity_types=["Person", "Preference", "Tool"]
)

# Add procedural information
await add_memory(
    content="For code reviews: 1) Check tests, 2) Verify documentation, 3) Test locally",
    entity_types=["Procedure"]
)
```

#### Searching Information

```python
# Search for specific entity types
preferences = await search_nodes(
    query="development environment preferences",
    entity_types=["Preference"],
    limit=10
)

# Search for relationships
collaborations = await search_facts(
    query="team collaboration patterns",
    entity_types=["Team", "Person"],
    limit=20
)
```

#### Context-Aware Search

```python
# Use center node for contextual search
team_context = await search_nodes(
    query="development practices",
    center_node_uuid="engineering-team-uuid",
    entity_types=["Procedure", "Requirement"]
)
```

### Advanced Usage Patterns

#### Workflow Integration

```python
# Example workflow: Project planning assistance
async def project_planning_workflow():
    # 1. Search for existing procedures
    procedures = await search_nodes(
        query="project planning procedures",
        entity_types=["Procedure"]
    )
    
    # 2. Search for team preferences
    preferences = await search_nodes(
        query="team planning preferences",
        entity_types=["Preference"]
    )
    
    # 3. Store new project information
    await add_memory(
        content="New project: AI assistant with requirements for scalability and performance",
        entity_types=["Project", "Requirement"]
    )
    
    # 4. Find related teams and expertise
    expertise = await search_facts(
        query="AI development expertise",
        entity_types=["Person", "Skill"]
    )
```

#### Knowledge Synthesis

```python
# Combine information from multiple searches
async def synthesize_knowledge(topic):
    # Search multiple entity types
    entities = await search_nodes(
        query=topic,
        entity_types=["Concept", "Procedure", "Requirement"]
    )
    
    # Search for relationships
    relationships = await search_facts(
        query=f"{topic} relationships",
        limit=50
    )
    
    # Synthesize findings
    synthesis = analyze_and_combine(entities, relationships)
    
    # Store synthesis as new knowledge
    await add_memory(
        content=f"Knowledge synthesis for {topic}: {synthesis}",
        entity_types=["Analysis", "Concept"]
    )
```

### Error Handling and Recovery

```python
# Robust MCP operations
async def safe_memory_operation(content, entity_types):
    try:
        # Try to add memory
        result = await add_memory(content, entity_types)
        return result
    except ConnectionError:
        # Handle connection issues
        logger.warning("MCP server connection lost, retrying...")
        await asyncio.sleep(1)
        return await add_memory(content, entity_types)
    except ValidationError as e:
        # Handle validation errors
        logger.error(f"Invalid memory content: {e}")
        # Attempt to fix and retry
        cleaned_content = clean_content(content)
        return await add_memory(cleaned_content, entity_types)
```

### Performance Optimization

#### Batch Operations

```python
# Batch multiple related memories
async def batch_add_memories(memory_items):
    tasks = []
    for item in memory_items:
        task = add_memory(
            content=item["content"],
            entity_types=item["entity_types"]
        )
        tasks.append(task)
    
    # Execute in parallel with semaphore for rate limiting
    semaphore = asyncio.Semaphore(5)  # Limit concurrent operations
    
    async def controlled_add(task):
        async with semaphore:
            return await task
    
    results = await asyncio.gather(
        *[controlled_add(task) for task in tasks],
        return_exceptions=True
    )
    
    return results
```

#### Smart Caching

```python
# Cache frequent searches
from functools import lru_cache
import time

class MCPCache:
    def __init__(self, ttl=300):  # 5 minute TTL
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key):
        if key in self.cache:
            result, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return result
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = (value, time.time())

cache = MCPCache()

async def cached_search_nodes(query, entity_types=None):
    cache_key = f"{query}:{entity_types}"
    cached_result = cache.get(cache_key)
    
    if cached_result:
        return cached_result
    
    result = await search_nodes(query, entity_types)
    cache.set(cache_key, result)
    return result
```

### Security and Privacy

#### Data Sanitization

```python
import re

def sanitize_content(content):
    """Remove sensitive information before storage"""
    # Remove potential PII patterns
    patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',  # Credit card
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    ]
    
    sanitized = content
    for pattern in patterns:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized)
    
    return sanitized

# Use in memory operations
async def safe_add_memory(content, entity_types):
    sanitized_content = sanitize_content(content)
    return await add_memory(sanitized_content, entity_types)
```

### Monitoring and Debugging

#### Operation Logging

```python
import logging

logger = logging.getLogger("mcp_operations")

class MCPLogger:
    @staticmethod
    async def log_operation(operation, **kwargs):
        logger.info(f"MCP Operation: {operation}", extra=kwargs)
    
    @staticmethod
    async def log_search(query, entity_types, results_count):
        await MCPLogger.log_operation(
            "search",
            query=query,
            entity_types=entity_types,
            results_count=results_count
        )
    
    @staticmethod
    async def log_memory_add(content_length, entity_types):
        await MCPLogger.log_operation(
            "add_memory",
            content_length=content_length,
            entity_types=entity_types
        )

# Usage in operations
async def logged_search_nodes(query, entity_types=None):
    results = await search_nodes(query, entity_types)
    await MCPLogger.log_search(query, entity_types, len(results))
    return results
```

### Testing MCP Integration

```python
import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_mcp_client():
    client = AsyncMock()
    client.search_nodes.return_value = [
        {"uuid": "test-uuid", "name": "Test Entity", "type": "Concept"}
    ]
    client.add_memory.return_value = {"uuid": "memory-uuid", "status": "created"}
    return client

@pytest.mark.asyncio
async def test_knowledge_workflow(mock_mcp_client):
    # Test complete workflow
    workflow = KnowledgeWorkflow(mock_mcp_client)
    
    # Test search
    results = await workflow.search_knowledge("test query")
    assert len(results) > 0
    
    # Test memory addition
    memory_result = await workflow.add_knowledge("test content", ["Concept"])
    assert memory_result["status"] == "created"
    
    # Verify calls
    mock_mcp_client.search_nodes.assert_called()
    mock_mcp_client.add_memory.assert_called()
```

### Best Practices Summary

1. **Search First**: Always search existing knowledge before adding new information
2. **Specific Queries**: Use targeted queries with appropriate entity type filters
3. **Immediate Storage**: Store new information as soon as it's discovered
4. **Context Awareness**: Use contextual search and maintain conversation context
5. **Error Handling**: Implement robust error handling and recovery mechanisms

## OpenCode Integration

The project includes a comprehensive `opencode.jsonc` configuration that integrates the Graphiti MCP server with other useful MCP servers:

### MCP Server Stack
- **graphiti-memory**: This MCP server providing knowledge graph capabilities
- **sequential-thinking**: Enhanced reasoning for complex analysis
- **brave-search**: Web search for research and fact-checking
- **filesystem**: Enhanced file operations
- **git**: Version control integration

### Agent Specializations
The configuration includes specialized agents that leverage these MCP servers:

- **Graphiti Knowledge Engineer**: Focuses on knowledge graph operations using graphiti-memory
- **Research Assistant**: Combines brave-search with graphiti-memory for research workflows
- **Full Stack Developer**: Uses all tools for comprehensive development tasks
- **Documentation Specialist**: Leverages search and knowledge storage for documentation
- **DevOps Engineer**: Infrastructure management with procedure storage

### Integration Patterns
Each agent follows the core MCP patterns established in this documentation:
- Search existing knowledge first using graphiti-memory
- Use appropriate entity type filters for targeted queries
- Store new procedures and knowledge immediately
- Maintain context across operations
- Follow established procedures from the knowledge graph

See the root `opencode.jsonc` file for complete configuration and usage instructions.