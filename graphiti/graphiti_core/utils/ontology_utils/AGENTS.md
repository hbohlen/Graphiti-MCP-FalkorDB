# AGENTS.md

This file provides guidance to AI agents when working with ontology utilities.

## Directory Overview

This directory contains utilities for managing entity types, schemas, and ontological structures within Graphiti knowledge graphs.

## Files

- `entity_types_utils.py` - Utilities for managing custom entity types and schemas

## Ontology Management

### Entity Types (`entity_types_utils.py`)

Provides utilities for defining and managing custom entity types:

1. **Entity Type Definition**: Define custom entity types with specific attributes
2. **Schema Validation**: Validate entities against defined schemas
3. **Type Inheritance**: Support for entity type hierarchies
4. **Custom Attributes**: Define domain-specific entity attributes
5. **Type Evolution**: Handle changes to entity types over time

## Agent Guidelines

### Defining Custom Entity Types

```python
from graphiti_core.utils.ontology_utils import EntityTypeManager
from pydantic import BaseModel, Field

# Define custom entity type
class Organization(BaseModel):
    name: str = Field(description="Organization name")
    industry: str = Field(description="Industry sector")
    founded_year: int = Field(description="Year founded")
    headquarters: str = Field(description="Headquarters location")

# Register entity type
entity_manager = EntityTypeManager()
entity_manager.register_type("Organization", Organization)
```

### Using Custom Entity Types

```python
# Extract entities with custom types
custom_entities = await graphiti.extract_entities(
    text="Apple Inc. is a technology company founded in 1976",
    entity_types=["Organization", "Person", "Location"]
)

# Validate entity data
validated_entity = entity_manager.validate_entity(
    entity_type="Organization",
    entity_data={
        "name": "Apple Inc.",
        "industry": "Technology",
        "founded_year": 1976,
        "headquarters": "Cupertino, CA"
    }
)
```

### Best Practices for Agents

1. **Schema Design**: Design clear, well-defined entity schemas
2. **Validation**: Always validate entities against schemas
3. **Evolution**: Plan for schema evolution and backward compatibility
4. **Documentation**: Document entity types and their purposes
5. **Consistency**: Maintain consistent naming and attribute conventions

### Entity Type Patterns

#### Domain-Specific Types
```python
# Academic domain types
class ResearchPaper(BaseModel):
    title: str
    authors: List[str]
    publication_year: int
    journal: str
    doi: Optional[str] = None

class University(BaseModel):
    name: str
    location: str
    established_year: int
    ranking: Optional[int] = None

# Business domain types
class Company(BaseModel):
    name: str
    industry: str
    revenue: Optional[float] = None
    employee_count: Optional[int] = None

class Product(BaseModel):
    name: str
    category: str
    price: Optional[float] = None
    manufacturer: str
```

#### Hierarchical Types
```python
# Base type
class Entity(BaseModel):
    name: str
    description: Optional[str] = None

# Specialized types inheriting from base
class Person(Entity):
    age: Optional[int] = None
    occupation: Optional[str] = None

class Organization(Entity):
    industry: str
    founded_year: Optional[int] = None
```

### Schema Validation

```python
from graphiti_core.utils.ontology_utils.validation import EntityValidator

# Create validator
validator = EntityValidator(entity_manager)

# Validate entity data
validation_result = validator.validate(
    entity_type="Organization",
    data=organization_data
)

if not validation_result.is_valid:
    for error in validation_result.errors:
        logger.error(f"Validation error: {error}")
```

### Type Evolution

```python
# Handle schema changes
class OrganizationV1(BaseModel):
    name: str
    industry: str

class OrganizationV2(BaseModel):
    name: str
    industry: str
    founded_year: Optional[int] = None  # New field
    headquarters: Optional[str] = None  # New field

# Register migration
entity_manager.register_migration(
    from_type="OrganizationV1",
    to_type="OrganizationV2",
    migration_function=migrate_organization_v1_to_v2
)
```

### Custom Attributes

```python
# Define custom attribute types
from enum import Enum

class IndustryType(str, Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"

class Organization(BaseModel):
    name: str
    industry: IndustryType  # Use enum for validation
    website: Optional[AnyUrl] = None  # URL validation
    description: Optional[str] = Field(None, max_length=1000)
```

### Integration with Graph Operations

```python
# Use custom types in graph operations
async def add_organization_episode(graphiti, org_data):
    # Validate organization data
    validated_org = entity_manager.validate_entity(
        "Organization", 
        org_data
    )
    
    # Create episode with validated data
    episode = await graphiti.add_episode(
        name=f"Organization: {validated_org.name}",
        content=f"Added organization {validated_org.name} in {validated_org.industry}",
        metadata={"entity_type": "Organization", "validated": True}
    )
    
    return episode
```

### Type-Aware Search

```python
# Search for specific entity types
organizations = await graphiti.search_nodes(
    query="technology companies",
    entity_types=["Organization"],
    filters={"industry": "Technology"}
)

# Type-specific queries
tech_companies = await graphiti.search_entities_by_type(
    entity_type="Organization",
    criteria={"industry": IndustryType.TECHNOLOGY}
)
```

### Configuration Management

```python
# Configure entity type settings
type_config = EntityTypeConfig(
    strict_validation=True,
    allow_additional_fields=False,
    auto_migration=True,
    validation_on_read=True
)

entity_manager.configure(type_config)
```

### Performance Considerations

1. **Schema Complexity**: Keep schemas reasonably simple for performance
2. **Validation Overhead**: Consider validation overhead in high-throughput scenarios
3. **Index Optimization**: Create indices for frequently queried type attributes
4. **Caching**: Cache type definitions and validation results
5. **Batch Operations**: Use batch validation for large datasets

### Error Handling

```python
from graphiti_core.utils.ontology_utils.errors import (
    SchemaValidationError,
    TypeNotFoundError,
    MigrationError
)

try:
    validated_entity = entity_manager.validate_entity(type_name, data)
except SchemaValidationError as e:
    logger.error(f"Schema validation failed: {e.errors}")
except TypeNotFoundError as e:
    logger.error(f"Entity type not found: {e.type_name}")
```

### Testing Custom Types

```python
# Test entity type definitions
def test_organization_type():
    org_data = {
        "name": "Test Corp",
        "industry": "Technology",
        "founded_year": 2020
    }
    
    # Should validate successfully
    validated = entity_manager.validate_entity("Organization", org_data)
    assert validated.name == "Test Corp"
    
    # Should fail validation
    invalid_data = {"name": "Test Corp"}  # Missing required fields
    with pytest.raises(SchemaValidationError):
        entity_manager.validate_entity("Organization", invalid_data)
```

### Best Practices Summary

1. **Clear Schemas**: Define clear, well-documented entity schemas
2. **Validation**: Always validate entity data against schemas
3. **Evolution**: Plan for schema evolution and backward compatibility
4. **Performance**: Consider performance implications of complex schemas
5. **Testing**: Thoroughly test entity type definitions and validations