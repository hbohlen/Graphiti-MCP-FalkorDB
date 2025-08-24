# AGENTS.md

This file provides guidance to AI agents when working with the database driver components.

## Directory Overview

This directory contains database driver implementations that provide abstraction over different graph database backends, enabling Graphiti to work with multiple database systems.

## Files

- `driver.py` - Abstract base driver class defining the interface
- `neo4j_driver.py` - Neo4j database driver implementation
- `falkordb_driver.py` - FalkorDB database driver implementation
- `__init__.py` - Module initialization and exports

## Driver Architecture

### Base Driver (`driver.py`)

Defines the abstract interface that all database drivers must implement:

- Connection management
- Query execution
- Transaction handling
- Index and constraint management
- Graph operations (CRUD for nodes and edges)

### Neo4j Driver (`neo4j_driver.py`)

Production-ready driver for Neo4j databases:

- Uses official Neo4j Python driver
- Supports Neo4j 5.26+ 
- Optimized for enterprise deployments
- Advanced indexing and constraint support

### FalkorDB Driver (`falkordb_driver.py`)

Alternative driver for FalkorDB:

- **Redis-based**: Built on Redis infrastructure with graph capabilities
- **Version**: Compatible with FalkorDB 1.1.2+
- **Protocol**: Uses Redis protocol (RESP) for communication
- **Performance**: Fast for smaller datasets and simple queries
- **Setup**: Minimal configuration, no authentication required by default
- **Ideal for**: Development, testing, lightweight deployments
- **Cloud Support**: Compatible with FalkorDB Cloud service
- **Memory**: In-memory graph operations with Redis persistence options

## Agent Guidelines

### Choosing a Driver

1. **Neo4j**: For production environments, large datasets, enterprise features
2. **FalkorDB**: For development, testing, lightweight deployments, Redis compatibility

### Driver Usage Patterns

#### Neo4j Setup
```python
from graphiti_core.driver import Neo4jDriver

driver = Neo4jDriver(
    uri="bolt://localhost:7687",
    user="neo4j", 
    password="password",
    database="neo4j"  # optional, defaults to "neo4j"
)
```

#### FalkorDB Setup
```python
from graphiti_core.driver import FalkorDBDriver

# Basic setup (no authentication)
driver = FalkorDBDriver(
    host="localhost",         # default
    port=6379,               # default
    database="default_db"    # optional, defaults to "default_db"
)

# With authentication (if configured)
driver = FalkorDBDriver(
    host="localhost",
    port=6379,
    username="your_username",  # optional
    password="your_password",  # optional
    database="my_graph_db"
)

# Using URI format (alternative)
driver = FalkorDBDriver(
    uri="falkor://localhost:6379",
    database="my_graph_db"
)
```

### Best Practices for Agents

1. **Connection Management**: Always properly close connections
2. **Error Handling**: Handle database-specific exceptions appropriately
3. **Transaction Management**: Use transactions for atomic operations
4. **Performance**: Understand each driver's performance characteristics
5. **Configuration**: Set appropriate timeouts and connection pools

### Common Operations

All drivers support these core operations:

1. **Node Operations**: Create, read, update, delete nodes
2. **Edge Operations**: Create, read, update, delete relationships
3. **Search Operations**: Query nodes and edges with various criteria
4. **Index Management**: Create and manage database indices
5. **Constraint Management**: Define and enforce data constraints

### Driver-Specific Considerations

#### Neo4j Driver

- **Enterprise Features**: Supports advanced Neo4j enterprise features
- **Performance**: Optimized for large-scale operations
- **APOC Support**: Can leverage APOC procedures when available
- **Clustering**: Supports Neo4j cluster deployments
- **Memory Management**: Efficient handling of large result sets

#### FalkorDB Driver

- **Redis Integration**: Leverages Redis infrastructure and protocol
- **Speed**: Fast for smaller datasets and simple queries
- **Simplicity**: Easier setup and configuration than Neo4j
- **Development**: Ideal for development and testing environments
- **No Authentication**: Works without authentication by default
- **Memory Efficiency**: In-memory operations with optional persistence
- **Query Language**: Supports Cypher-like queries through OpenCypher
- **Limitations**: 
  - Smaller ecosystem compared to Neo4j
  - Less advanced indexing options
  - Limited enterprise features
  - Performance may degrade with very large datasets
- **Docker Support**: Easy deployment with `docker run falkordb/falkordb`
- **Cloud Options**: Available as managed service through FalkorDB Cloud

### Development Guidelines

1. **Interface Compliance**: New drivers must implement the base driver interface
2. **Error Mapping**: Map database-specific errors to common exceptions
3. **Testing**: Comprehensive tests for all driver operations
4. **Documentation**: Clear documentation of driver-specific features
5. **Performance**: Benchmark and optimize driver performance

### Troubleshooting

Common issues and solutions:

1. **Connection Problems**: Check URI format, credentials, and database availability
2. **Version Compatibility**: Ensure database version meets minimum requirements
3. **Permission Issues**: Verify user has necessary database permissions
4. **Performance Issues**: Check indices, query optimization, connection pooling
5. **Transaction Conflicts**: Handle concurrent access and transaction isolation

### Extension Points

- **Custom Drivers**: Implement new drivers for other graph databases
- **Driver Configuration**: Extend configuration options for specific needs
- **Performance Optimizations**: Add database-specific optimizations
- **Feature Support**: Add support for database-specific features
- **Monitoring**: Integrate monitoring and metrics collection