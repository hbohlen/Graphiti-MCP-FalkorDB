# AGENTS.md

This file provides guidance to AI agents when working with the examples directory.

## Directory Overview

This directory contains various examples demonstrating how to use Graphiti in different scenarios and applications. Each subdirectory showcases specific use cases and integration patterns.

## Examples Structure

### `quickstart/`
- Basic Graphiti functionality demonstration
- Shows database connection, episode management, and search capabilities
- Good starting point for understanding core concepts

### `langgraph-agent/`
- Integration example with LangChain's LangGraph
- Demonstrates building AI agents with Graphiti memory
- Shows how to combine LangGraph workflows with knowledge graphs

### `ecommerce/`
- E-commerce specific use case
- Demonstrates customer behavior tracking and product relationships
- Shows business-specific entity modeling

### `podcast/`
- Podcast content management example
- Audio/text content processing and relationship modeling
- Temporal content organization patterns

### `wizard_of_oz/`
- Specific domain example implementation
- Demonstrates custom entity types and relationships
- Shows domain-specific knowledge modeling

### `data/`
- Sample data files used by examples
- Test datasets and reference materials
- Data format examples

## Agent Guidelines

### Working with Examples

1. **Start with Quickstart**: Always begin with the quickstart example to understand basic patterns
2. **Environment Setup**: Ensure all required environment variables are set (see individual README files)
3. **Database Requirements**: Most examples require a running Neo4j or FalkorDB instance
4. **Dependencies**: Install example-specific dependencies as documented

### Running Examples

```bash
# Navigate to specific example directory
cd examples/[example_name]

# Follow the README.md instructions for setup
# Most examples require:
export OPENAI_API_KEY=your_key

# For Neo4j (default)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password

# For FalkorDB (alternative)
export FALKORDB_HOST=localhost
export FALKORDB_PORT=6379
export FALKORDB_USERNAME=your_username  # optional
export FALKORDB_PASSWORD=your_password  # optional

# Run the example (varies by example)
python example_script.py
# or
jupyter notebook example.ipynb
```

### Best Practices

- **Read README First**: Each example has specific setup instructions
- **Database Isolation**: Use separate databases for different examples to avoid conflicts
- **Environment Variables**: Set up proper environment configuration before running
- **Understanding Patterns**: Study the code patterns for your specific use case
- **Adaptation**: Use examples as templates for your own implementations
- **Database Choice**: Consider FalkorDB for development/testing, Neo4j for production
- **Performance Testing**: Test with both databases to understand performance characteristics

### Common Patterns

- Database initialization and connection setup
- Episode creation and management
- Entity extraction and relationship modeling
- Search and retrieval operations
- Integration with external systems and frameworks

### Integration Examples

- **LangGraph**: Shows how to integrate with agent frameworks
- **Domain-Specific**: Demonstrates industry-specific implementations
- **Data Processing**: Examples of handling different data types and formats