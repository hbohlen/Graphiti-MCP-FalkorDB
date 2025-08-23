# OpenCode Configuration for Cognitive-Copilot

This repository includes a comprehensive OpenCode configuration (`opencode.jsonc`) that provides AI agents with powerful MCP (Model Context Protocol) servers and specialized tools for working with the Graphiti knowledge graph framework.

## Quick Start

1. **Install Dependencies**
   ```bash
   cd graphiti
   uv sync --extra dev
   ```

2. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export BRAVE_API_KEY="your-brave-api-key"  # Optional for web search
   ```

3. **Start Neo4j Database**
   ```bash
   # Using Docker (recommended)
   cd graphiti/mcp_server
   docker compose up -d neo4j
   ```

4. **Start MCP Servers**
   ```bash
   # Start the Graphiti MCP server
   cd graphiti/mcp_server
   docker compose up -d
   ```

## MCP Servers Included

### Core Knowledge Management
- **graphiti-memory**: Provides persistent knowledge graph storage, semantic search, and entity management
  - Tools: `add_memory`, `search_nodes`, `search_facts`, `clear_graph`
  - Supports entity types: Person, Concept, Preference, Procedure, Requirement, etc.

### Enhanced Capabilities  
- **sequential-thinking**: Provides step-by-step reasoning for complex analysis
- **brave-search**: Web search capabilities for research and fact-checking
- **filesystem**: Enhanced file operations with MCP protocol
- **git**: Version control operations through MCP

## Specialized Agents

### Graphiti Knowledge Engineer
Expert in building and managing temporally-aware knowledge graphs
- **Primary Tools**: graphiti-memory, sequential-thinking
- **Specializations**: Schema design, temporal data modeling, hybrid search optimization
- **Best Practices**: Always search before adding, use entity type filters, store immediately

### Research Assistant  
Web search and knowledge synthesis specialist
- **Primary Tools**: brave-search, graphiti-memory, sequential-thinking
- **Workflow**: Search existing knowledge → Web research → Store findings → Create summaries
- **Strengths**: Multi-source verification, citation tracking, research organization

### Full Stack Developer
Framework development with established patterns
- **Primary Tools**: All MCP servers for comprehensive development
- **Expertise**: Python/FastAPI, Neo4j/FalkorDB, LLM integrations, testing
- **Focus**: Following Graphiti development patterns and best practices

### Documentation Specialist
Technical documentation with knowledge integration
- **Primary Tools**: graphiti-memory, brave-search, filesystem
- **Capabilities**: API docs, tutorials, troubleshooting guides, cross-references
- **Process**: Research accuracy, maintain consistency, store style patterns

### DevOps Engineer
Infrastructure and deployment specialist  
- **Primary Tools**: graphiti-memory, filesystem, git
- **Expertise**: Docker, CI/CD, database administration, monitoring
- **Focus**: Deployment procedures, infrastructure patterns, troubleshooting

## Quick Commands

The configuration includes convenient commands for common tasks:

```bash
# Development setup
opencode setup          # Install dependencies

# Code quality
opencode format         # Format code with ruff
opencode lint           # Run linting and type checking
opencode test           # Run test suite
opencode check          # Run all quality checks

# MCP server management
opencode start-mcp      # Start MCP server stack
opencode stop-mcp       # Stop MCP server stack
```

## Development Workflow

### Using the Knowledge Graph
1. **Search First**: Always search existing knowledge before adding new information
   ```python
   # Search for existing procedures
   results = await search_nodes(
       query="development workflow procedures",
       entity_types=["Procedure"]
   )
   ```

2. **Store Immediately**: Add new knowledge as soon as discovered
   ```python
   # Store new procedure
   await add_memory(
       content="Code review process: 1) Check tests, 2) Verify docs, 3) Test locally",
       entity_types=["Procedure"]
   )
   ```

3. **Use Context**: Leverage relationships and temporal aspects
   ```python
   # Context-aware search
   team_context = await search_nodes(
       query="team preferences",
       center_node_uuid="engineering-team-uuid",
       entity_types=["Preference"]
   )
   ```

### Research Integration
1. **Check Existing Knowledge**: Search the knowledge graph first
2. **Web Research**: Use brave-search for current information
3. **Verify Sources**: Cross-reference multiple sources
4. **Store Findings**: Add to knowledge graph with proper entity types
5. **Create Summaries**: Synthesize and establish relationships

### Development Patterns
1. **Follow AGENTS.md**: Comprehensive guidance in `graphiti/AGENTS.md` and `graphiti/mcp_server/AGENTS.md`
2. **Use Make Commands**: Standard development workflow with `make` commands
3. **Test Integration**: Run both unit and integration tests (`_int` suffix)
4. **Code Quality**: Enforce ruff formatting, pyright type checking
5. **Document Procedures**: Store development patterns in knowledge graph

## Environment Variables

Required:
- `OPENAI_API_KEY`: OpenAI API key for LLM operations

Optional:
- `BRAVE_API_KEY`: Brave Search API key for web search capabilities
- `NEO4J_URI`: Neo4j database URI (default: bolt://localhost:7687)
- `NEO4J_USER`: Neo4j username (default: neo4j)
- `NEO4J_PASSWORD`: Neo4j password (default: password)
- `MODEL_NAME`: OpenAI model for main operations (default: gpt-4o-mini)
- `SMALL_MODEL_NAME`: OpenAI model for smaller operations (default: gpt-4o-mini)

## Troubleshooting

### MCP Server Issues
1. Check Docker containers: `docker compose ps`
2. View logs: `docker compose logs graphiti-mcp`
3. Restart services: `docker compose restart`

### Database Connection
1. Verify Neo4j is running: `docker compose ps neo4j`
2. Check connection: `neo4j://localhost:7474` in browser
3. Verify credentials match environment variables

### Development Environment
1. Check uv installation: `uv --version`
2. Sync dependencies: `uv sync --extra dev`
3. Run health checks: `make check`

## Learning Resources

- **Main Documentation**: `graphiti/README.md`
- **Agent Guidelines**: `graphiti/AGENTS.md` and `graphiti/mcp_server/AGENTS.md`
- **MCP Server Details**: `graphiti/mcp_server/README.md`
- **API Documentation**: Generated from FastAPI server
- **Examples**: `graphiti/examples/` directory

For detailed technical guidance, always refer to the comprehensive AGENTS.md files which contain extensive patterns, examples, and best practices for working with the Graphiti framework.