# AGENTS.md

This file provides guidance to AI agents when working with utility components.

## Directory Overview

This directory contains utility functions and tools for various Graphiti operations including bulk processing, datetime handling, maintenance operations, and ontology management.

## Files and Subdirectories

- `bulk_utils.py` - Utilities for bulk operations and batch processing
- `datetime_utils.py` - Date and time handling utilities
- `maintenance/` - Graph maintenance and cleanup operations
- `ontology_utils/` - Ontology and schema management utilities

## Utility Categories

### Bulk Operations (`bulk_utils.py`)

Provides utilities for efficient batch processing:

1. **Batch Episode Processing**: Process multiple episodes efficiently
2. **Bulk Entity Operations**: Batch create/update entities
3. **Relationship Batch Processing**: Efficiently manage relationship operations
4. **Performance Optimization**: Optimize large-scale operations
5. **Memory Management**: Handle large datasets efficiently

### DateTime Utilities (`datetime_utils.py`)

Handles temporal aspects of the knowledge graph:

1. **Timestamp Management**: Consistent datetime handling across the system
2. **Temporal Queries**: Time-based query utilities
3. **Date Parsing**: Parse various date formats
4. **Timezone Handling**: Manage timezones and UTC conversion
5. **Temporal Relationships**: Handle time-based relationships

## Agent Guidelines

### Bulk Operations

```python
from graphiti_core.utils.bulk_utils import BulkProcessor

# Process multiple episodes efficiently
processor = BulkProcessor(graphiti_instance)
await processor.process_episodes_batch(episodes_list)

# Bulk entity operations
await processor.bulk_create_entities(entities_data)
await processor.bulk_update_relationships(relationships_data)
```

### DateTime Handling

```python
from graphiti_core.utils.datetime_utils import (
    normalize_datetime,
    parse_flexible_date,
    get_utc_now
)

# Normalize datetime for storage
normalized_dt = normalize_datetime(input_datetime)

# Parse flexible date formats
parsed_date = parse_flexible_date("2023-12-25")

# Get current UTC timestamp
current_time = get_utc_now()
```

### Best Practices for Agents

1. **Batch Processing**: Use bulk utilities for large-scale operations
2. **DateTime Consistency**: Always use provided datetime utilities
3. **Memory Efficiency**: Monitor memory usage during bulk operations
4. **Error Handling**: Implement proper error handling for bulk operations
5. **Progress Monitoring**: Track progress of long-running operations

### Performance Optimization

#### Bulk Operations
- **Batch Size**: Optimize batch sizes for your specific use case
- **Memory Management**: Monitor memory usage during processing
- **Parallel Processing**: Use async operations for concurrency
- **Transaction Management**: Group operations in appropriate transactions
- **Progress Tracking**: Implement progress tracking for long operations

#### DateTime Operations
- **UTC Normalization**: Always normalize to UTC for storage
- **Timezone Awareness**: Handle timezone conversions properly
- **Caching**: Cache parsed datetime objects when appropriate
- **Validation**: Validate datetime inputs before processing
- **Performance**: Use efficient datetime libraries and operations

### Common Patterns

#### Bulk Episode Processing
```python
# Process large numbers of episodes efficiently
episodes = [
    {"name": "Episode 1", "content": "...", "timestamp": dt1},
    {"name": "Episode 2", "content": "...", "timestamp": dt2},
    # ... many more episodes
]

# Use bulk processor for efficiency
await bulk_processor.process_episodes_batch(
    episodes,
    batch_size=100,
    progress_callback=progress_handler
)
```

#### DateTime Normalization
```python
# Normalize various datetime formats
input_dates = [
    "2023-12-25",
    "December 25, 2023",
    "2023-12-25T15:30:00Z",
    datetime.now()
]

normalized_dates = [
    normalize_datetime(date) for date in input_dates
]
```

### Maintenance Operations

The `maintenance/` subdirectory provides tools for:

1. **Graph Cleanup**: Remove orphaned nodes and edges
2. **Index Optimization**: Optimize database indices
3. **Data Validation**: Validate graph integrity
4. **Performance Tuning**: Optimize graph performance
5. **Backup Operations**: Backup and restore functionality

### Ontology Management

The `ontology_utils/` subdirectory provides:

1. **Schema Management**: Define and manage entity schemas
2. **Ontology Validation**: Validate entities against schemas
3. **Schema Evolution**: Handle schema changes over time
4. **Custom Types**: Define custom entity and relationship types
5. **Validation Rules**: Implement custom validation rules

### Error Handling

```python
from graphiti_core.utils.errors import BulkOperationError

try:
    await bulk_processor.process_batch(data)
except BulkOperationError as e:
    # Handle bulk operation errors
    logger.error(f"Bulk operation failed: {e}")
    # Implement recovery logic
```

### Integration Considerations

1. **Memory Efficiency**: Utilities are designed for large-scale operations
2. **Database Optimization**: Work efficiently with database drivers
3. **Async Operations**: Support for concurrent processing
4. **Error Recovery**: Robust error handling and recovery
5. **Monitoring**: Built-in monitoring and logging capabilities

### Configuration Options

Many utilities support configuration for different use cases:

```python
# Configure bulk processor
config = BulkProcessorConfig(
    batch_size=100,
    max_concurrent=10,
    retry_attempts=3,
    progress_reporting=True
)

processor = BulkProcessor(graphiti, config)
```

### Testing Utilities

The utils directory also provides testing utilities:

1. **Mock Objects**: Mock utilities for testing
2. **Test Data**: Generate test data for various scenarios
3. **Performance Testing**: Utilities for performance testing
4. **Validation Testing**: Test data validation and integrity
5. **Integration Testing**: Support for integration test scenarios

### Extension Guidelines

- **New Utilities**: Follow established patterns for new utility functions
- **Performance**: Optimize for large-scale operations
- **Compatibility**: Maintain compatibility with existing code
- **Documentation**: Provide clear documentation and examples
- **Testing**: Include comprehensive tests for all utilities

### Common Use Cases

1. **Data Migration**: Migrate large datasets into Graphiti
2. **Regular Maintenance**: Scheduled graph maintenance operations
3. **Performance Optimization**: Optimize existing graph operations
4. **Data Validation**: Validate and clean existing graph data
5. **Backup and Restore**: Backup and restore graph data