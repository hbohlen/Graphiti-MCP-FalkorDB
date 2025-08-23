# AGENTS.md

This file provides guidance to AI agents when working with data model components.

## Directory Overview

This directory contains the data models that define the structure of nodes and edges in Graphiti knowledge graphs, providing the foundation for all graph operations.

## Subdirectories

- `nodes/` - Node (entity) data models and schemas
- `edges/` - Edge (relationship) data models and schemas

## Data Model Architecture

### Core Concepts

1. **Nodes**: Represent entities in the knowledge graph (people, places, concepts, etc.)
2. **Edges**: Represent relationships between entities (connections, interactions, associations)
3. **Temporal Awareness**: Both nodes and edges include temporal information
4. **Metadata**: Rich metadata support for additional context
5. **Type Safety**: Strong typing using Pydantic models

### Bi-temporal Model

Graphiti uses a bi-temporal data model that tracks two types of time:

1. **Valid Time**: When the information was true in the real world
2. **Transaction Time**: When the information was recorded in the system

## Agent Guidelines

### Working with Data Models

1. **Type Safety**: Always use the defined models for type safety
2. **Validation**: Models automatically validate data structure
3. **Serialization**: Models handle JSON serialization/deserialization
4. **Temporal Data**: Include appropriate temporal information
5. **Metadata**: Use metadata fields for additional context

### Node Models

```python
from graphiti_core.models.nodes import EntityNode

# Create a node
node = EntityNode(
    name="John Doe",
    type="Person",
    summary="Software engineer at Tech Corp",
    valid_at=datetime.utcnow(),
    metadata={"department": "Engineering", "level": "Senior"}
)
```

### Edge Models

```python
from graphiti_core.models.edges import RelationshipEdge

# Create an edge
edge = RelationshipEdge(
    source_node_uuid="node-uuid-1",
    target_node_uuid="node-uuid-2",
    relationship_type="WORKS_FOR",
    summary="John works for Tech Corp",
    valid_at=datetime.utcnow(),
    metadata={"start_date": "2020-01-01", "position": "Senior Engineer"}
)
```

### Best Practices for Agents

1. **Consistent Modeling**: Use consistent patterns for similar entities/relationships
2. **Rich Summaries**: Provide descriptive summaries for nodes and edges
3. **Appropriate Types**: Use specific, meaningful types for entities and relationships
4. **Temporal Accuracy**: Ensure temporal information is accurate and relevant
5. **Metadata Usage**: Use metadata for domain-specific attributes

### Common Node Types

Typical entity types in knowledge graphs:

1. **Person**: Individuals, characters, authors
2. **Organization**: Companies, institutions, groups
3. **Location**: Places, addresses, geographical entities
4. **Event**: Meetings, conferences, incidents
5. **Concept**: Ideas, topics, themes
6. **Document**: Files, articles, reports
7. **Product**: Items, services, offerings

### Common Relationship Types

Typical relationship types:

1. **WORKS_FOR**: Employment relationships
2. **LOCATED_IN**: Geographical relationships
3. **PARTICIPATES_IN**: Event participation
4. **RELATED_TO**: General associations
5. **CREATED_BY**: Authorship/creation relationships
6. **BELONGS_TO**: Membership relationships
7. **DEPENDS_ON**: Dependency relationships

### Model Validation

```python
from pydantic import ValidationError

try:
    node = EntityNode(**node_data)
except ValidationError as e:
    # Handle validation errors
    for error in e.errors():
        print(f"Validation error: {error}")
```

### Custom Model Extensions

```python
from graphiti_core.models.nodes import EntityNode
from pydantic import Field

# Extend base models for domain-specific needs
class PersonNode(EntityNode):
    age: Optional[int] = Field(None, description="Person's age")
    occupation: Optional[str] = Field(None, description="Person's occupation")
    
    class Config:
        # Additional configuration if needed
        validate_assignment = True
```

### Temporal Operations

```python
# Working with temporal data
from graphiti_core.utils.datetime_utils import get_utc_now

# Create node with current timestamp
node = EntityNode(
    name="Current Event",
    type="Event",
    valid_at=get_utc_now(),
    created_at=get_utc_now()
)

# Query nodes by time range
nodes_in_range = await graphiti.get_nodes_in_time_range(
    start_time=start_date,
    end_time=end_date
)
```

### Metadata Patterns

```python
# Rich metadata for different domains
business_metadata = {
    "industry": "Technology",
    "revenue": 1000000,
    "employee_count": 100,
    "stock_symbol": "TECH"
}

academic_metadata = {
    "department": "Computer Science",
    "university": "Tech University",
    "research_areas": ["AI", "Machine Learning"],
    "h_index": 25
}

# Use metadata for filtering and search
nodes_with_metadata = await graphiti.search_nodes(
    query="technology companies",
    metadata_filters={"industry": "Technology"}
)
```

### Serialization and Storage

```python
# Models handle serialization automatically
node_json = node.model_dump_json()
node_dict = node.model_dump()

# Deserialize from JSON
node_from_json = EntityNode.model_validate_json(node_json)
node_from_dict = EntityNode.model_validate(node_dict)
```

### Performance Considerations

1. **Model Complexity**: Keep models reasonably simple for performance
2. **Validation Overhead**: Consider validation costs in high-throughput scenarios
3. **Serialization**: Optimize serialization for frequently accessed models
4. **Memory Usage**: Monitor memory usage with large numbers of model instances
5. **Indexing**: Consider which model fields need database indexing

### Integration with Graph Operations

Models are used throughout Graphiti operations:

1. **Entity Extraction**: LLMs produce model instances
2. **Graph Storage**: Models are serialized for database storage
3. **Search Results**: Search operations return model instances
4. **API Responses**: REST APIs return serialized models
5. **Validation**: Models validate data integrity throughout the system

### Testing Models

```python
def test_entity_node_creation():
    node_data = {
        "name": "Test Entity",
        "type": "TestType",
        "summary": "A test entity",
        "valid_at": datetime.utcnow()
    }
    
    node = EntityNode(**node_data)
    assert node.name == "Test Entity"
    assert node.type == "TestType"

def test_model_validation():
    # Test required fields
    with pytest.raises(ValidationError):
        EntityNode(name="Test")  # Missing required fields
    
    # Test field types
    with pytest.raises(ValidationError):
        EntityNode(
            name="Test",
            type="TestType",
            valid_at="invalid_date"  # Should be datetime
        )
```

### Migration and Evolution

```python
# Handle model evolution
class EntityNodeV2(EntityNode):
    # Add new fields with defaults for backward compatibility
    new_field: Optional[str] = Field(None, description="New field")
    
    @classmethod
    def migrate_from_v1(cls, v1_data: dict) -> "EntityNodeV2":
        # Migration logic from v1 to v2
        return cls(**v1_data, new_field=None)
```

### Best Practices Summary

1. **Use Provided Models**: Leverage existing models rather than creating custom structures
2. **Rich Metadata**: Use metadata fields for domain-specific information
3. **Temporal Awareness**: Always include appropriate temporal information
4. **Type Safety**: Leverage Pydantic validation for data integrity
5. **Consistent Patterns**: Use consistent modeling patterns across your application