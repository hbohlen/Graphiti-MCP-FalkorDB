# AGENTS.md

This file provides guidance to AI agents when working with the MCP (Model Context Protocol) server.

## Directory Overview

This directory contains the Model Context Protocol server implementation that allows AI assistants (like Claude, Cursor, and other MCP clients) to interact with Graphiti's knowledge graph capabilities through the MCP protocol. The server uses FalkorDB as the database backend.

## Key Features

The Graphiti MCP server provides:

1. **Episode Management**: Add, retrieve, and delete episodes (text, messages, or JSON data)
2. **Entity Management**: Search and manage entity nodes and relationships in the knowledge graph
3. **Search Capabilities**: Search for facts (edges) and node summaries using semantic and hybrid search
4. **Group Management**: Organize and manage groups of related data with group_id filtering
5. **Graph Maintenance**: Clear the graph and rebuild indices

## MCP Server Architecture

### Server Implementation

The MCP server exposes Graphiti functionality through standardized MCP tools:

- **Memory Tools**: `add_memory`, `search_memory_nodes`, `search_memory_facts` for episode and entity management
- **Entity Tools**: `get_entity_edge`, `delete_entity_edge` for entity relationship management
- **Episode Tools**: `get_episodes`, `delete_episode` for episode operations
- **Maintenance Tools**: `clear_graph` for graph operations

### Integration Patterns

Common integration patterns:

1. **AI Assistant Memory**: Persistent memory for conversational AI
2. **Knowledge Base**: Searchable knowledge repository
3. **Context Management**: Maintaining context across sessions
4. **Information Retrieval**: Semantic search and fact discovery

## MCP Client Configuration

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8001/sse"
      ]
    }
  }
}
```

### Cursor IDE Configuration

Set up the MCP server endpoint in your Cursor settings:
- Server URL: `http://localhost:8001/sse`
- Protocol: Server-Sent Events (SSE)

## Server Configuration

### Database Configuration

The Graphiti MCP server uses FalkorDB as its graph database backend.

#### FalkorDB Configuration

- `DATABASE_TYPE`: Set to `falkordb`
- `FALKORDB_HOST`: FalkorDB host (default: `localhost` or `falkordb` in Docker)
- `FALKORDB_PORT`: FalkorDB port (default: `6379`)
- `FALKORDB_USERNAME`: FalkorDB username (optional)
- `FALKORDB_PASSWORD`: FalkorDB password (optional)

### LLM and Embedding Provider Configuration

The Graphiti MCP server supports using different API providers for LLM operations and embeddings. This is particularly useful when your primary LLM provider doesn't offer embedding models.

#### Single Provider Setup (Default)

When using a provider that offers both LLM and embedding capabilities (e.g., OpenAI):

- `OPENAI_API_KEY`: Your API key
- `OPENAI_BASE_URL`: Optional custom base URL (defaults to OpenAI's API)
- `MODEL_NAME`: The LLM model to use (e.g., `gpt-4`)

#### Dual Provider Setup

When using different providers for LLM and embeddings (e.g., OpenRouter for LLM, OpenAI for embeddings):

##### LLM Configuration:
- `OPENAI_API_KEY`: Your LLM provider's API key
- `OPENAI_BASE_URL`: Your LLM provider's base URL (e.g., `https://openrouter.ai/api/v1`)
- `MODEL_NAME`: The LLM model to use (e.g., `moonshotai/kimi-k2:free`)

##### Embedding Configuration:
- `EMBEDDING_API_KEY`: Your embedding provider's API key
- `EMBEDDING_BASE_URL`: Your embedding provider's base URL (e.g., `https://api.openai.com/v1`)
- `EMBEDDING_MODEL`: The embedding model to use (default: `text-embedding-3-small`)

#### Example .env Configuration for Dual Providers:

```env
# Database Configuration
DATABASE_TYPE=falkordb
FALKORDB_HOST=falkordb
FALKORDB_PORT=6379

# LLM Provider (OpenRouter)
OPENAI_API_KEY=sk-or-v1-your-openrouter-key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=moonshotai/kimi-k2:free

# Embedding Provider (OpenAI)
EMBEDDING_API_KEY=sk-proj-your-openai-key
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-small

# Other settings
GROUP_ID=cognitive_copilot
SEMAPHORE_LIMIT=10
```

#### Common Provider Combinations:

1. **OpenRouter (LLM) + OpenAI (Embeddings)**:
   - Use when you want to leverage OpenRouter's diverse model selection
   - OpenRouter doesn't provide embedding models, so OpenAI handles embeddings

2. **Anthropic (LLM) + OpenAI (Embeddings)**:
   - Use Claude models for LLM operations
   - OpenAI for embedding generation

3. **Local LLM + OpenAI (Embeddings)**:
   - Use a locally hosted LLM (via Ollama, vLLM, etc.)
   - Cloud-based embeddings for better quality

#### Troubleshooting Dual Provider Setup:

1. **Embeddings failing with "model not found"**:
   - Ensure `EMBEDDING_BASE_URL` is set to the correct embedding provider
   - Verify `EMBEDDING_API_KEY` is valid for the embedding provider

2. **Docker containers not picking up environment variables**:
   - Ensure your `.env` file is in the `mcp_server/` directory
   - Rebuild containers after updating `.env`: `docker compose --profile falkordb up -d --build`
   - Verify variables are loaded: `docker exec mcp_server-graphiti-mcp-falkordb-1 printenv | grep -E "EMBEDDING|OPENAI"`

3. **VS Code MCP client connection issues after restart**:
   - Reload the VS Code window after restarting Docker containers
   - The MCP client needs to reconnect to the new server instance

### Code Modifications for Dual Provider Support

If your `graphiti_mcp_server.py` doesn't support separate embedding providers out of the box, you'll need to modify it. Here are the required changes:

**1. Add support for separate embedding API key (around line 408):**

```python
# Original code - only uses OPENAI_API_KEY for everything
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Modified code - check for separate embedding key
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Check for separate embedding API key
embedding_api_key = os.environ.get('EMBEDDING_API_KEY') or api_key
```

**2. Add support for separate embedding base URL (around line 444-456):**

```python
# Original embedder configuration
embedder_config = OpenAIEmbedderConfig(
    api_key=self.api_key,
    embedding_model=self.model
)

# Modified configuration with base_url support
# Check for separate embedding base URL
embedding_base_url = os.environ.get('EMBEDDING_BASE_URL')

embedder_config = OpenAIEmbedderConfig(
    api_key=embedding_api_key,  # Use the separate embedding key from step 1
    embedding_model=self.model,
    base_url=embedding_base_url  # This will be None if not set, which is fine
)
```

**3. After making these changes:**

1. Rebuild the Docker image:
   ```bash
   docker compose --profile falkordb up -d --build
   ```

2. Verify the environment variables are loaded:
   ```bash
   docker exec mcp_server-graphiti-mcp-falkordb-1 printenv | grep -E "EMBEDDING|OPENAI"
   ```

3. Test by adding a memory - embeddings should now go to the correct provider

**Note:** The exact line numbers may vary depending on your version of the code. Look for the sections where `OpenAIEmbedderConfig` is instantiated and where API keys are retrieved from environment variables.

## Docker Deployment

### Start FalkorDB and MCP Server:

```bash
cd mcp_server/
docker compose --profile falkordb up -d
```

This starts:
- Graphiti MCP server on port 8001
- FalkorDB database on port 6379
- FalkorDB browser UI on port 3000

### Stop Services:

```bash
docker compose --profile falkordb down
```

### Rebuild After Changes:

```bash
docker compose --profile falkordb up -d --build
```

## Local Development

### Install Dependencies and Run Locally:

```bash
cd mcp_server/
# Install dependencies with FalkorDB support
uv sync --extra falkordb

# Set environment variables
export OPENAI_API_KEY=your_key
export DATABASE_TYPE=falkordb
export FALKORDB_HOST=localhost
export FALKORDB_PORT=6379

# Run server
python graphiti_mcp_server.py --database-type falkordb
```

## MCP Tools Reference

### add_memory

Add an episode to memory. This is the primary way to add information to the graph.

**Parameters:**
- `name` (str): Name of the episode
- `episode_body` (str): The content of the episode (text, JSON, or message format)
- `group_id` (str, optional): A unique ID for this graph
- `source` (str, optional): Source type - "text", "json", or "message"
- `source_description` (str, optional): Description of the source
- `uuid` (str, optional): Optional UUID for the episode

**Examples:**

```json
// Adding plain text
{
  "name": "User Profile",
  "episode_body": "John prefers morning meetings",
  "source": "text",
  "group_id": "user_data"
}

// Adding JSON data
{
  "name": "Customer Data",
  "episode_body": "{\"company\": \"Acme Corp\", \"size\": \"enterprise\"}",
  "source": "json",
  "source_description": "CRM export"
}
```

### search_memory_nodes

Search the graph memory for relevant node summaries.

**Parameters:**
- `query` (str): The search query
- `group_ids` (list, optional): List of group IDs to filter results
- `max_nodes` (int, optional): Maximum number of nodes to return (default: 10)
- `center_node_uuid` (str, optional): UUID of a node to center the search around
- `entity` (str, optional): Entity type filter ("Preference", "Procedure")

### search_memory_facts

Search the graph memory for relevant facts (relationships between entities).

**Parameters:**
- `query` (str): The search query
- `group_ids` (list, optional): List of group IDs to filter results
- `max_facts` (int, optional): Maximum number of facts to return (default: 10)
- `center_node_uuid` (str, optional): UUID of a node to center the search around

### get_episodes

Get the most recent memory episodes for a specific group.

**Parameters:**
- `group_id` (str, optional): ID of the group to retrieve episodes from
- `last_n` (int, optional): Number of most recent episodes to retrieve (default: 10)

### delete_episode

Delete an episode from the graph memory.

**Parameters:**
- `uuid` (str): UUID of the episode to delete

### delete_entity_edge

Delete an entity edge from the graph memory.

**Parameters:**
- `uuid` (str): UUID of the entity edge to delete

### get_entity_edge

Get an entity edge from the graph memory by its UUID.

**Parameters:**
- `uuid` (str): UUID of the entity edge to retrieve

### clear_graph

Clear all data from the graph memory and rebuild indices. Use with caution.

## Agent Workflow Guidelines

These guidelines help AI agents effectively use Graphiti's MCP tools for memory management and knowledge retrieval.

### Before Starting Any Task

- **Always search first:** Use the `search_memory_nodes` tool to look for relevant preferences and procedures before beginning work.
- **Search for facts too:** Use the `search_memory_facts` tool to discover relationships and factual information that may be relevant to your task.
- **Filter by entity type:** Specify `Preference`, `Procedure`, or `Requirement` in your node search to get targeted results.
- **Review all matches:** Carefully examine any preferences, procedures, or facts that match your current task.

### Always Save New or Updated Information

- **Capture requirements and preferences immediately:** When a user expresses a requirement or preference, use `add_memory` to store it right away.
  - _Best practice:_ Split very long requirements into shorter, logical chunks.
- **Be explicit if something is an update to existing knowledge.** Only add what's changed or new to the graph.
- **Document procedures clearly:** When you discover how a user wants things done, record it as a procedure.
- **Record factual relationships:** When you learn about connections between entities, store these as facts.
- **Be specific with categories:** Label preferences and procedures with clear categories for better retrieval later.

### During Your Work

- **Respect discovered preferences:** Align your work with any preferences you've found.
- **Follow procedures exactly:** If you find a procedure for your current task, follow it step by step.
- **Apply relevant facts:** Use factual information to inform your decisions and recommendations.
- **Stay consistent:** Maintain consistency with previously identified preferences, procedures, and facts.

### Workflow Best Practices

- **Search before suggesting:** Always check if there's established knowledge before making recommendations.
- **Combine node and fact searches:** For complex tasks, search both nodes and facts to build a complete picture.
- **Use `center_node_uuid`:** When exploring related information, center your search around a specific node.
- **Prioritize specific matches:** More specific information takes precedence over general information.
- **Be proactive:** If you notice patterns in user behavior, consider storing them as preferences or procedures.

**Remember:** The knowledge graph is your memory. Use it consistently to provide personalized assistance that respects the user's established preferences, procedures, and factual context.

## Best Practices

1. **Search First**: Always search existing knowledge before adding new information
2. **Use Group IDs**: Organize related information using group_id for better management
3. **Specific Queries**: Use targeted queries with appropriate filters
4. **Entity Type Filtering**: Use entity filters ("Preference", "Procedure", "Requirement") for targeted searches
5. **Immediate Storage**: Store new information as soon as it's discovered
6. **Source Types**: Use appropriate source types (text, json, message) for different content
7. **Error Handling**: Check for connection issues and retry if needed
8. **Container Management**: Remember to rebuild containers after environment variable changes
9. **Chunk Long Content**: When storing very long requirements or procedures, split them into logical chunks
10. **Maintain Consistency**: Ensure new information aligns with existing preferences and procedures