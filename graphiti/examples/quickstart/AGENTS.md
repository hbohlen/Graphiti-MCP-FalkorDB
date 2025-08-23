# AGENTS.md

This file provides guidance to AI agents when working with the quickstart example.

## Directory Overview

This directory contains the Graphiti quickstart example that demonstrates basic functionality including database connection, episode management, and search capabilities.

## Files

- `quickstart_neo4j.py` - Neo4j database implementation example
- `quickstart_falkordb.py` - FalkorDB database implementation example  
- `requirements.txt` - Python dependencies for the example
- `README.md` - Detailed setup and running instructions

## Example Features

1. **Database Connection**: Shows how to connect to Neo4j or FalkorDB
2. **Graphiti Initialization**: Demonstrates proper setup of indices and constraints
3. **Episode Management**: Adding episodes (text and structured JSON) to the graph
4. **Search Operations**: 
   - Hybrid search for relationships (edges) using semantic and keyword matching
   - Graph-based search with reranking using source node UUIDs
   - Node search using predefined search recipes

## Prerequisites

- Python 3.9+
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- **For Neo4j**: Neo4j Desktop installed and running with local DBMS
- **For FalkorDB**: FalkorDB server running

## Agent Guidelines

### Environment Setup

```bash
# Required for LLM and embedding
export OPENAI_API_KEY=your_openai_api_key

# Optional Neo4j connection parameters (defaults shown)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# Optional FalkorDB connection parameters (defaults shown)
export FALKORDB_URI=falkor://localhost:6379
```

### Running the Example

```bash
# Install dependencies
pip install -r requirements.txt

# Run Neo4j version
python quickstart_neo4j.py

# Or run FalkorDB version  
python quickstart_falkordb.py
```

### Learning Objectives

1. **Basic Setup**: Understand how to initialize Graphiti with database drivers
2. **Data Ingestion**: Learn patterns for adding different types of episodes
3. **Search Patterns**: Practice various search strategies and understand their use cases
4. **Graph Operations**: See how graph relationships enhance search results

### Key Concepts Demonstrated

- **Temporal Awareness**: Episodes have temporal context and relationships
- **Hybrid Search**: Combining semantic embeddings with keyword and graph-based search
- **Entity Extraction**: Automatic extraction of entities and relationships from text
- **Search Reranking**: Using graph distance to improve search relevance

### Best Practices for Agents

- Always check database connectivity before operations
- Use appropriate search strategies based on query type
- Consider temporal aspects when working with episodes
- Validate search results and handle edge cases
- Follow established patterns for error handling

### Common Use Cases

- **Getting Started**: Perfect introduction to Graphiti concepts
- **Proof of Concept**: Template for building initial prototypes
- **Testing Setup**: Validate your environment configuration
- **Learning Search**: Understand different search capabilities