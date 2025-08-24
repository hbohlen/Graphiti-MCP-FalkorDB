# AGENTS.md

This file provides guidance to AI agents when working with code in this repository.

## Project Overview

Graphiti is a Python framework for building temporally-aware knowledge graphs designed for AI agents. It enables real-time incremental updates to knowledge graphs without batch recomputation, making it suitable for dynamic environments.

Key features:

- Bi-temporal data model with explicit tracking of event occurrence times
- Hybrid retrieval combining semantic embeddings, keyword search (BM25), and graph traversal
- Support for custom entity definitions via Pydantic models
- Integration with Neo4j and FalkorDB as graph storage backends

## Development Commands

### Main Development Commands (run from project root)

```bash
# Install dependencies
uv sync --extra dev

# Format code (ruff import sorting + formatting)
make format

# Lint code (ruff + pyright type checking)
make lint

# Run tests
make test

# Run all checks (format, lint, test)
make check
```

### Server Development (run from server/ directory)

```bash
cd server/
# Install server dependencies
uv sync --extra dev

# Run server in development mode
uvicorn graph_service.main:app --reload

# Format, lint, test server code
make format
make lint
make test
```

### MCP Server Development (run from mcp_server/ directory)

```bash
cd mcp_server/
# Install MCP server dependencies
uv sync

# Run with Docker Compose
docker-compose up
```

## Code Architecture

### Core Library (`graphiti_core/`)

- **Main Entry Point**: `graphiti.py` - Contains the main `Graphiti` class that orchestrates all functionality
- **Graph Storage**: `driver/` - Database drivers for Neo4j and FalkorDB
- **LLM Integration**: `llm_client/` - Clients for OpenAI, Anthropic, Gemini, Groq
- **Embeddings**: `embedder/` - Embedding clients for various providers
- **Graph Elements**: `nodes.py`, `edges.py` - Core graph data structures
- **Search**: `search/` - Hybrid search implementation with configurable strategies
- **Prompts**: `prompts/` - LLM prompts for entity extraction, deduplication, summarization
- **Utilities**: `utils/` - Maintenance operations, bulk processing, datetime handling

### Server (`server/`)

- **FastAPI Service**: `graph_service/main.py` - REST API server
- **Routers**: `routers/` - API endpoints for ingestion and retrieval
- **DTOs**: `dto/` - Data transfer objects for API contracts

### MCP Server (`mcp_server/`)

- **MCP Implementation**: `graphiti_mcp_server.py` - Model Context Protocol server for AI assistants
- **Docker Support**: Containerized deployment with Neo4j

## Testing

- **Unit Tests**: `tests/` - Comprehensive test suite using pytest
- **Integration Tests**: Tests marked with `_int` suffix require database connections
- **Evaluation**: `tests/evals/` - End-to-end evaluation scripts

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Required for LLM inference and embeddings
- `USE_PARALLEL_RUNTIME` - Optional boolean for Neo4j parallel runtime (enterprise only)
- Provider-specific keys: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`, `VOYAGE_API_KEY`

#### Neo4j Environment Variables
```bash
export NEO4J_URI=bolt://localhost:7687    # default
export NEO4J_USER=neo4j                   # default
export NEO4J_PASSWORD=password            # required
export NEO4J_DATABASE=neo4j               # optional, defaults to "neo4j"
```

#### FalkorDB Environment Variables
```bash
export FALKORDB_HOST=localhost             # default
export FALKORDB_PORT=6379                  # default  
export FALKORDB_USERNAME=                  # optional, no auth by default
export FALKORDB_PASSWORD=                  # optional, no auth by default
export FALKORDB_DATABASE=default_db        # optional, defaults to "default_db"
# Alternative URI format:
export FALKORDB_URI=falkor://localhost:6379
```

### Database Setup

#### Neo4j Setup
- **Version**: 5.26+ required, available via Neo4j Desktop
- **Database**: Name defaults to `neo4j` (hardcoded in Neo4jDriver)
- **Override**: Pass `database` parameter to driver constructor
- **Installation**: Download from https://neo4j.com/download/
- **Configuration**: Requires authentication (username/password)

#### FalkorDB Setup
- **Version**: 1.1.2+ required as alternative backend
- **Database**: Name defaults to `default_db` (hardcoded in FalkorDriver)
- **Override**: Pass `database` parameter to driver constructor
- **Installation Options**:
  - **Docker**: `docker run -p 6379:6379 falkordb/falkordb:latest`
  - **Source**: Build from https://github.com/FalkorDB/FalkorDB
  - **Cloud**: FalkorDB Cloud service available
- **Advantages**: 
  - Redis-compatible protocol
  - Lightweight setup
  - Fast for development and testing
  - No authentication required by default
- **Environment Variables**:
  ```bash
  export FALKORDB_HOST=localhost      # default
  export FALKORDB_PORT=6379          # default
  export FALKORDB_USERNAME=          # optional
  export FALKORDB_PASSWORD=          # optional
  export FALKORDB_DATABASE=default_db # optional
  ```

## Development Guidelines

### Code Style

- Use Ruff for formatting and linting (configured in pyproject.toml)
- Line length: 100 characters
- Quote style: single quotes
- Type checking with Pyright is enforced
- Main project uses `typeCheckingMode = "basic"`, server uses `typeCheckingMode = "standard"`

### Testing Requirements

- Run tests with `make test` or `pytest`
- Integration tests require database connections and are marked with `_int` suffix
- Use `pytest-xdist` for parallel test execution
- Run specific test files: `pytest tests/test_specific_file.py`
- Run specific test methods: `pytest tests/test_file.py::test_method_name`
- Run only integration tests: `pytest tests/ -k "_int"`
- Run only unit tests: `pytest tests/ -k "not _int"`

### LLM Provider Support

The codebase supports multiple LLM providers but works best with services supporting structured output (OpenAI, Gemini). Other providers may cause schema validation issues, especially with smaller models.

### MCP Server Usage Guidelines

When working with the MCP server, follow the patterns established in `mcp_server/cursor_rules.md`:

- Always search for existing knowledge before adding new information
- Use specific entity type filters (`Preference`, `Procedure`, `Requirement`)
- Store new information immediately using `add_memory`
- Follow discovered procedures and respect established preferences

## Agent-Specific Guidance

### Working with Knowledge Graphs

- Understand the bi-temporal nature of the data model
- Use hybrid search combining semantic, keyword, and graph traversal
- Consider temporal aspects when querying or updating the graph
- Respect entity relationships and maintain graph consistency

### Integration Patterns

- Follow the established patterns for LLM provider integration
- Use the appropriate driver for your database backend (Neo4j/FalkorDB)
- Implement proper error handling and logging
- Consider performance implications of graph operations

#### Database Driver Selection Guidelines

**Choose Neo4j when:**
- Working with production environments
- Handling large datasets (>1M nodes)
- Need enterprise features (clustering, backup, security)
- Require APOC procedures or advanced Cypher features
- Performance is critical for complex queries

**Choose FalkorDB when:**
- Development and testing environments
- Prototyping and proof-of-concepts
- Small to medium datasets (<100k nodes)
- Need Redis ecosystem compatibility
- Want simplified deployment and maintenance
- Cost-conscious deployments

### Best Practices

- Always validate data before adding to the graph
- Use appropriate search strategies for different use cases
- Maintain consistent entity naming and relationships
- Document any custom entity types or extensions