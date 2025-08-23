# AGENTS.md

This file provides guidance to AI agents when working with edge model components.

## Directory Overview

This directory contains edge (relationship) data models, database query implementations, and related utilities for managing relationships in Graphiti knowledge graphs.

## Files

- `edge_db_queries.py` - Database query implementations for edge operations
- `__init__.py` - Module initialization and model exports

## Edge Model Architecture

### Relationship Edges

Edges represent relationships between entities with these characteristics:

1. **Directional Connections**: Source and target node references
2. **Relationship Semantics**: Typed relationships with descriptive summaries
3. **Temporal Awareness**: Valid time and creation timestamps
4. **Rich Context**: Episodes and metadata providing relationship context
5. **Confidence Scoring**: Relationship strength and confidence measures

### Core Edge Fields

Standard fields in relationship edges:

1. **uuid**: Unique identifier for the edge
2. **source_node_uuid**: UUID of the source entity
3. **target_node_uuid**: UUID of the target entity
4. **relationship_type**: Type/category of the relationship
5. **summary**: Descriptive summary of the relationship
6. **valid_at**: When the relationship was valid
7. **created_at**: When the edge was created in the system
8. **metadata**: Additional relationship-specific attributes

## Agent Guidelines

### Creating Edges

```python
from graphiti_core.models.edges import RelationshipEdge
from datetime import datetime

# Create a basic relationship edge
edge = RelationshipEdge(
    source_node_uuid="person-uuid-123",
    target_node_uuid="organization-uuid-456",
    relationship_type="WORKS_FOR",
    summary="John Doe works as a senior engineer at TechCorp",
    valid_at=datetime.utcnow(),
    metadata={
        "position": "Senior Software Engineer",
        "start_date": "2020-01-15",
        "department": "Engineering",
        "employment_type": "Full-time"
    }
)
```

### Relationship Types

Common relationship types and their semantics:

#### Employment Relationships
```python
employment_edge = RelationshipEdge(
    source_node_uuid=person_uuid,
    target_node_uuid=company_uuid,
    relationship_type="WORKS_FOR",
    summary="Employment relationship",
    metadata={
        "role": "Software Engineer",
        "start_date": "2020-01-01",
        "salary_range": "100k-150k",
        "remote": True
    }
)
```

#### Geographical Relationships
```python
location_edge = RelationshipEdge(
    source_node_uuid=person_uuid,
    target_node_uuid=location_uuid,
    relationship_type="LOCATED_IN",
    summary="Person lives in this location",
    metadata={
        "residence_type": "Primary",
        "duration": "5 years",
        "address_type": "Home"
    }
)
```

#### Collaboration Relationships
```python
collaboration_edge = RelationshipEdge(
    source_node_uuid=person1_uuid,
    target_node_uuid=person2_uuid,
    relationship_type="COLLABORATES_WITH",
    summary="Professional collaboration on projects",
    metadata={
        "projects": ["Project A", "Project B"],
        "collaboration_type": "Technical",
        "frequency": "Daily"
    }
)
```

#### Hierarchical Relationships
```python
management_edge = RelationshipEdge(
    source_node_uuid=manager_uuid,
    target_node_uuid=employee_uuid,
    relationship_type="MANAGES",
    summary="Management relationship",
    metadata={
        "team": "Engineering Team",
        "direct_report": True,
        "management_style": "Collaborative"
    }
)
```

### Best Practices for Agents

1. **Semantic Clarity**: Use clear, meaningful relationship types
2. **Directional Awareness**: Consider the direction of relationships
3. **Rich Context**: Provide comprehensive summaries and metadata
4. **Temporal Accuracy**: Ensure temporal information is correct
5. **Relationship Strength**: Include confidence or strength measures

### Database Operations

The `edge_db_queries.py` file provides database-specific operations:

```python
from graphiti_core.models.edges.edge_db_queries import EdgeQueries

# Initialize edge queries for your driver
edge_queries = EdgeQueries(driver)

# Create edge in database
await edge_queries.create_edge(edge)

# Retrieve edge by UUID
retrieved_edge = await edge_queries.get_edge_by_uuid(edge.uuid)

# Find edges by source node
source_edges = await edge_queries.get_edges_by_source(source_node_uuid)

# Find edges by target node
target_edges = await edge_queries.get_edges_by_target(target_node_uuid)

# Update edge information
updated_edge = await edge_queries.update_edge(edge.uuid, updates)

# Delete edge
await edge_queries.delete_edge(edge.uuid)
```

### Bidirectional Relationships

```python
# Create bidirectional relationships when semantically appropriate
friendship_edge1 = RelationshipEdge(
    source_node_uuid=person1_uuid,
    target_node_uuid=person2_uuid,
    relationship_type="FRIEND_OF",
    summary="Friendship relationship"
)

friendship_edge2 = RelationshipEdge(
    source_node_uuid=person2_uuid,
    target_node_uuid=person1_uuid,
    relationship_type="FRIEND_OF",
    summary="Friendship relationship"
)
```

### Relationship Traversal

```python
# Find all relationships for a node
all_relationships = await graphiti.get_node_relationships(node_uuid)

# Find specific relationship types
work_relationships = await graphiti.get_relationships_by_type(
    node_uuid=person_uuid,
    relationship_types=["WORKS_FOR", "COLLABORATES_WITH"]
)

# Traverse relationship paths
path_results = await graphiti.find_relationship_paths(
    source_uuid=start_node_uuid,
    target_uuid=end_node_uuid,
    max_depth=3
)
```

### Edge Validation

```python
from pydantic import ValidationError

def validate_edge_data(edge_data):
    try:
        edge = RelationshipEdge(**edge_data)
        return edge, None
    except ValidationError as e:
        return None, e.errors()

# Example usage
edge_data = {
    "source_node_uuid": "source-uuid",
    "target_node_uuid": "target-uuid",
    "relationship_type": "RELATED_TO"
    # Missing required fields
}

edge, errors = validate_edge_data(edge_data)
if errors:
    print(f"Validation errors: {errors}")
```

### Relationship Strength and Confidence

```python
# Include confidence scores in metadata
confident_edge = RelationshipEdge(
    source_node_uuid=source_uuid,
    target_node_uuid=target_uuid,
    relationship_type="WORKS_FOR",
    summary="High-confidence employment relationship",
    metadata={
        "confidence_score": 0.95,
        "evidence_sources": ["LinkedIn", "Company Directory"],
        "verification_date": "2024-01-01"
    }
)
```

### Temporal Relationships

```python
# Handle relationships that change over time
historical_edge = RelationshipEdge(
    source_node_uuid=person_uuid,
    target_node_uuid=old_company_uuid,
    relationship_type="WORKED_FOR",
    summary="Previous employment relationship",
    valid_at=datetime(2020, 1, 1),  # When relationship was valid
    metadata={
        "start_date": "2018-01-01",
        "end_date": "2020-12-31",
        "reason_for_leaving": "Career advancement"
    }
)
```

### Performance Considerations

1. **Index Optimization**: Index source and target node UUIDs
2. **Batch Operations**: Use batch operations for multiple edges
3. **Query Patterns**: Optimize for common traversal patterns
4. **Relationship Density**: Monitor graph density and performance
5. **Caching**: Cache frequently traversed relationships

### Edge Deduplication

```python
# Check for duplicate relationships
potential_duplicates = await graphiti.find_similar_relationships(
    source_uuid=source_uuid,
    target_uuid=target_uuid,
    relationship_type="WORKS_FOR"
)

if potential_duplicates:
    # Merge or consolidate duplicate relationships
    await graphiti.merge_relationships(
        primary_uuid=existing_edge.uuid,
        duplicate_uuid=new_edge.uuid
    )
```

### Relationship Analytics

```python
# Analyze relationship patterns
relationship_stats = await graphiti.get_relationship_statistics()
print(f"Total relationships: {relationship_stats.total_count}")
print(f"Most common types: {relationship_stats.type_distribution}")

# Find highly connected nodes
hub_nodes = await graphiti.find_hub_nodes(
    min_connections=10,
    relationship_types=["COLLABORATES_WITH", "WORKS_FOR"]
)
```

### Search and Filtering

```python
# Search for specific relationships
collaboration_edges = await graphiti.search_relationships(
    query="collaboration projects",
    relationship_types=["COLLABORATES_WITH"],
    metadata_filters={"project_type": "Technical"}
)

# Find relationships in time range
recent_relationships = await graphiti.get_relationships_in_time_range(
    start_time=last_month,
    end_time=datetime.utcnow(),
    relationship_types=["WORKS_FOR", "JOINS"]
)
```

### Testing Edge Operations

```python
def test_edge_creation():
    edge_data = {
        "source_node_uuid": "source-123",
        "target_node_uuid": "target-456",
        "relationship_type": "TEST_RELATIONSHIP",
        "summary": "A test relationship",
        "valid_at": datetime.utcnow()
    }
    
    edge = RelationshipEdge(**edge_data)
    assert edge.source_node_uuid == "source-123"
    assert edge.relationship_type == "TEST_RELATIONSHIP"

async def test_edge_database_operations():
    # Test create
    edge = RelationshipEdge(
        source_node_uuid="src-uuid",
        target_node_uuid="tgt-uuid",
        relationship_type="TEST_REL",
        summary="Test relationship"
    )
    created_edge = await edge_queries.create_edge(edge)
    assert created_edge.uuid is not None
    
    # Test retrieve
    retrieved_edge = await edge_queries.get_edge_by_uuid(created_edge.uuid)
    assert retrieved_edge.relationship_type == "TEST_REL"
    
    # Test update
    updates = {"summary": "Updated test relationship"}
    updated_edge = await edge_queries.update_edge(created_edge.uuid, updates)
    assert updated_edge.summary == "Updated test relationship"
    
    # Test delete
    await edge_queries.delete_edge(created_edge.uuid)
```

### Integration Patterns

Edge operations integrate with various Graphiti components:

1. **Relationship Extraction**: LLMs extract relationships and create edges
2. **Graph Traversal**: Edges enable navigation through the graph
3. **Search Operations**: Relationship search returns edge collections
4. **Analytics**: Edges provide data for network analysis
5. **Visualization**: Edges are rendered as connections in graph visualizations

### Best Practices Summary

1. **Semantic Relationships**: Use meaningful, specific relationship types
2. **Rich Context**: Include comprehensive summaries and metadata
3. **Directional Clarity**: Be explicit about relationship direction
4. **Temporal Accuracy**: Include accurate temporal information
5. **Performance**: Consider performance implications of relationship density