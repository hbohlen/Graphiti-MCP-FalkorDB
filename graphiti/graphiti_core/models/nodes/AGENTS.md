# AGENTS.md

This file provides guidance to AI agents when working with node model components.

## Directory Overview

This directory contains node (entity) data models, database query implementations, and related utilities for managing entities in Graphiti knowledge graphs.

## Files

- `node_db_queries.py` - Database query implementations for node operations
- `__init__.py` - Module initialization and model exports

## Node Model Architecture

### Entity Nodes

Nodes represent entities in the knowledge graph with the following characteristics:

1. **Unique Identification**: Each node has a unique UUID
2. **Entity Information**: Name, type, and descriptive summary
3. **Temporal Awareness**: Valid time and creation timestamps
4. **Rich Metadata**: Extensible metadata for domain-specific attributes
5. **Graph Context**: References to related episodes and relationships

### Core Node Fields

Standard fields in entity nodes:

1. **uuid**: Unique identifier for the node
2. **name**: Human-readable name of the entity
3. **type**: Category or classification of the entity
4. **summary**: Descriptive summary of the entity
5. **valid_at**: When the entity information was valid
6. **created_at**: When the node was created in the system
7. **metadata**: Additional domain-specific attributes

## Agent Guidelines

### Creating Nodes

```python
from graphiti_core.models.nodes import EntityNode
from datetime import datetime

# Create a basic entity node
node = EntityNode(
    name="Dr. Jane Smith",
    type="Person",
    summary="Research scientist specializing in machine learning",
    valid_at=datetime.utcnow(),
    metadata={
        "affiliation": "MIT",
        "research_area": "Machine Learning",
        "position": "Professor"
    }
)
```

### Node Types

Common entity types and their characteristics:

#### Person Entities
```python
person_node = EntityNode(
    name="John Doe",
    type="Person",
    summary="Software engineer with 10 years experience",
    metadata={
        "age": 35,
        "skills": ["Python", "JavaScript", "Machine Learning"],
        "location": "San Francisco, CA"
    }
)
```

#### Organization Entities
```python
org_node = EntityNode(
    name="TechCorp Inc.",
    type="Organization",
    summary="Technology company focused on AI solutions",
    metadata={
        "industry": "Technology",
        "founded": 2010,
        "headquarters": "Silicon Valley",
        "employee_count": 500
    }
)
```

#### Location Entities
```python
location_node = EntityNode(
    name="San Francisco",
    type="Location",
    summary="Major city in Northern California",
    metadata={
        "country": "United States",
        "state": "California",
        "population": 873965,
        "coordinates": {"lat": 37.7749, "lng": -122.4194}
    }
)
```

### Best Practices for Agents

1. **Descriptive Names**: Use clear, unambiguous names for entities
2. **Specific Types**: Use specific entity types rather than generic ones
3. **Rich Summaries**: Provide comprehensive but concise summaries
4. **Structured Metadata**: Use consistent metadata structures
5. **Temporal Accuracy**: Ensure temporal information reflects reality

### Database Operations

The `node_db_queries.py` file provides database-specific operations:

```python
from graphiti_core.models.nodes.node_db_queries import NodeQueries

# Initialize node queries for your driver
node_queries = NodeQueries(driver)

# Create node in database
await node_queries.create_node(node)

# Retrieve node by UUID
retrieved_node = await node_queries.get_node_by_uuid(node.uuid)

# Update node information
updated_node = await node_queries.update_node(node.uuid, updates)

# Delete node
await node_queries.delete_node(node.uuid)
```

### Node Relationships

Nodes are connected through edges, but nodes also maintain context:

```python
# Nodes can reference their episodes
node_with_episodes = EntityNode(
    name="Meeting Discussion",
    type="Event",
    summary="Weekly team meeting on project status",
    metadata={
        "episode_uuids": ["episode-1", "episode-2"],
        "participants": ["John", "Jane", "Bob"]
    }
)
```

### Search and Retrieval

```python
# Search for nodes by type
person_nodes = await graphiti.search_nodes(
    query="machine learning researchers",
    entity_types=["Person"]
)

# Search with metadata filters
tech_companies = await graphiti.search_nodes(
    query="technology companies",
    entity_types=["Organization"],
    metadata_filters={"industry": "Technology"}
)
```

### Node Validation

```python
from pydantic import ValidationError

def validate_node_data(node_data):
    try:
        node = EntityNode(**node_data)
        return node, None
    except ValidationError as e:
        return None, e.errors()

# Example usage
node_data = {
    "name": "Test Entity",
    "type": "TestType",
    "summary": "A test entity"
    # Missing required fields
}

node, errors = validate_node_data(node_data)
if errors:
    print(f"Validation errors: {errors}")
```

### Node Lifecycle Management

```python
# Create node
new_node = await graphiti.create_entity(
    name="New Product",
    type="Product",
    summary="Innovative AI-powered software tool"
)

# Update node
updated_node = await graphiti.update_entity(
    node_uuid=new_node.uuid,
    updates={
        "summary": "Updated product description",
        "metadata": {"version": "2.0", "release_date": "2024-01-01"}
    }
)

# Archive/soft delete node
await graphiti.archive_entity(new_node.uuid)
```

### Performance Considerations

1. **Batch Operations**: Use batch operations for multiple nodes
2. **Indexing**: Ensure appropriate database indices for frequently queried fields
3. **Metadata Size**: Monitor metadata size to avoid performance issues
4. **Query Optimization**: Optimize queries based on access patterns
5. **Caching**: Cache frequently accessed nodes

### Node Deduplication

```python
# Check for duplicate nodes before creation
potential_duplicates = await graphiti.find_similar_entities(
    name="Jane Smith",
    type="Person",
    similarity_threshold=0.8
)

if potential_duplicates:
    # Handle duplicates - merge or skip
    await graphiti.merge_entities(
        primary_uuid=existing_node.uuid,
        duplicate_uuid=new_node.uuid
    )
```

### Node Aggregation

```python
# Aggregate nodes for analytics
node_stats = await graphiti.get_node_statistics()
print(f"Total nodes: {node_stats.total_count}")
print(f"Nodes by type: {node_stats.type_distribution}")

# Time-based aggregation
daily_node_counts = await graphiti.get_node_counts_by_date(
    start_date=start_date,
    end_date=end_date,
    group_by="day"
)
```

### Testing Node Operations

```python
def test_node_creation():
    node_data = {
        "name": "Test Node",
        "type": "TestType",
        "summary": "A node for testing",
        "valid_at": datetime.utcnow()
    }
    
    node = EntityNode(**node_data)
    assert node.name == "Test Node"
    assert node.type == "TestType"

async def test_node_database_operations():
    # Test create
    node = EntityNode(name="DB Test", type="Test", summary="Test node")
    created_node = await node_queries.create_node(node)
    assert created_node.uuid is not None
    
    # Test retrieve
    retrieved_node = await node_queries.get_node_by_uuid(created_node.uuid)
    assert retrieved_node.name == "DB Test"
    
    # Test update
    updates = {"summary": "Updated test node"}
    updated_node = await node_queries.update_node(created_node.uuid, updates)
    assert updated_node.summary == "Updated test node"
    
    # Test delete
    await node_queries.delete_node(created_node.uuid)
```

### Integration Patterns

Node operations integrate with various Graphiti components:

1. **Entity Extraction**: LLMs extract entities and create nodes
2. **Search Operations**: Search returns node collections
3. **Graph Traversal**: Nodes are starting points for graph exploration
4. **Analytics**: Nodes provide data for graph analytics
5. **Visualization**: Nodes are rendered in graph visualizations

### Best Practices Summary

1. **Consistent Modeling**: Use consistent patterns for similar entity types
2. **Rich Context**: Include comprehensive summaries and metadata
3. **Proper Typing**: Use specific, meaningful entity types
4. **Temporal Awareness**: Include accurate temporal information
5. **Performance**: Consider performance implications of node operations