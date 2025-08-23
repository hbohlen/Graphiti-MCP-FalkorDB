# Building AI Agents with Graphiti MCP Server

This guide covers how to build AI agents that leverage Graphiti's temporally-aware knowledge graph capabilities through the Model Context Protocol (MCP) server. Graphiti enables agents to maintain persistent, contextual memory across conversations and interactions.

## Overview

The Graphiti MCP server provides AI agents with powerful memory and knowledge management capabilities through:

- **Persistent Memory**: Store and retrieve information across conversation sessions
- **Temporal Context**: Track when information was learned and how it evolves over time
- **Relationship Mapping**: Understand connections between entities, concepts, and events
- **Semantic Search**: Find relevant information using natural language queries
- **Structured Data Integration**: Work with JSON data, messages, and unstructured text

## Core Agent Capabilities

### Memory Management Tools

The MCP server exposes these key tools for agent memory:

| Tool | Purpose | Use Case |
|------|---------|----------|
| `add_memory` | Store new information as episodes | Save user preferences, facts, conversations |
| `search_memory_nodes` | Find entities and concepts | Locate people, places, topics, preferences |
| `search_memory_facts` | Find relationships and connections | Discover how entities relate to each other |
| `get_episodes` | Retrieve stored episodes | Access conversation history, past interactions |
| `delete_episode` | Remove outdated information | Clean up incorrect or obsolete data |
| `clear_graph` | Reset knowledge base | Start fresh for new contexts |

### Episode Types

Graphiti supports different types of information storage:

- **Text Episodes**: Plain text information, notes, observations
- **Message Episodes**: Conversation turns, chat logs, dialogues  
- **JSON Episodes**: Structured data, API responses, configuration

## Agent Architecture Patterns

### 1. Conversational Agent with Memory

A basic conversational agent that remembers user preferences and context:

```python
# Example agent workflow
async def handle_user_message(message: str, user_id: str):
    # 1. Search for relevant context
    context = await search_memory_nodes(
        query=message,
        group_id=user_id,
        max_results=5
    )
    
    # 2. Generate response using context
    response = await llm.generate(
        prompt=f"Context: {context}\nUser: {message}",
        system="You are a helpful assistant with memory."
    )
    
    # 3. Store the interaction
    await add_memory(
        name="Conversation Turn",
        episode_body=f"User: {message}\nAssistant: {response}",
        source="message",
        group_id=user_id
    )
    
    return response
```

### 2. Task-Oriented Agent

An agent that remembers procedures, requirements, and task-specific information:

```python
# Example task agent
class TaskAgent:
    async def process_request(self, task_description: str, project_id: str):
        # Search for existing procedures
        procedures = await search_memory_nodes(
            query=f"procedure {task_description}",
            group_id=project_id,
            entity_types=["Procedure"]
        )
        
        # Search for requirements
        requirements = await search_memory_facts(
            query=f"requirements {task_description}",
            group_id=project_id
        )
        
        # Execute task with context
        result = await self.execute_task(
            task_description, 
            procedures, 
            requirements
        )
        
        # Store the outcome
        await add_memory(
            name=f"Task Execution: {task_description}",
            episode_body=json.dumps({
                "task": task_description,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }),
            source="json",
            group_id=project_id
        )
        
        return result
```

### 3. Learning Agent

An agent that continuously learns from interactions and improves over time:

```python
class LearningAgent:
    async def learn_from_feedback(self, interaction_id: str, 
                                  feedback: str, user_id: str):
        # Store feedback
        await add_memory(
            name="User Feedback",
            episode_body=f"Interaction: {interaction_id}\nFeedback: {feedback}",
            source="text",
            group_id=f"{user_id}_feedback"
        )
        
        # Search for patterns in feedback
        similar_feedback = await search_memory_facts(
            query=feedback,
            group_id=f"{user_id}_feedback",
            max_results=10
        )
        
        # Update preferences based on patterns
        if self.detect_preference_pattern(similar_feedback):
            await self.update_user_preferences(user_id, feedback)
```

## Integration Patterns

### LangChain/LangGraph Integration

```python
from langchain.tools import Tool
from langgraph.graph import StateGraph

```python
# Create MCP tools as LangChain tools
def create_graphiti_tools(mcp_client):
    return [
        Tool(
            name="store_memory",
            description="Store information in long-term memory",
            func=lambda x: mcp_client.add_memory(
                name="Agent Memory", 
                episode_body=x, 
                source="text"
            )
        ),
        Tool(
            name="search_memory",
            description="Search for relevant information in memory",
            func=lambda x: mcp_client.search_memory_nodes(query=x)
        )
    ]

```python
# Build agent graph
def build_agent_graph():
    graph = StateGraph()
    graph.add_node("search_memory", search_memory_node)
    graph.add_node("generate_response", generate_response_node)
    graph.add_node("store_interaction", store_interaction_node)
    # ... define edges and logic
    return graph.compile()
```

### Cursor IDE Integration

For Cursor IDE agents, follow the [cursor_rules.md](cursor_rules.md) guidelines:

1. **Always search first** before taking actions
2. **Store immediately** when learning new information
3. **Use specific queries** for better retrieval
4. **Respect user preferences** found in memory

### Claude Desktop Integration

Configure Claude Desktop to use the MCP server for persistent memory across sessions.

## Best Practices

### Memory Organization

1. **Use Group IDs**: Organize information by user, project, or context
   ```python
   # Per-user memory
   group_id = f"user_{user_id}"
   
   # Per-project memory  
   group_id = f"project_{project_id}"
   
   # Per-session memory
   group_id = f"session_{session_id}"
   ```

2. **Descriptive Naming**: Use clear, descriptive names for episodes
   ```python
   # Good
   await add_memory(
       name="User Preference: Communication Style",
       episode_body="User prefers brief, direct responses without examples"
   )
   
   # Better
   await add_memory(
       name="Sarah's Communication Preference", 
       episode_body="Sarah Johnson prefers brief, direct responses..."
   )
   ```

3. **Structured Storage**: Use JSON for complex, structured information
   ```python
   await add_memory(
       name="Project Requirements",
       episode_body=json.dumps({
           "project": "E-commerce Platform",
           "requirements": [
               {"id": "REQ-001", "description": "User authentication"},
               {"id": "REQ-002", "description": "Shopping cart functionality"}
           ],
           "priority": "high"
       }),
       source="json"
   )
   ```

### Search Strategies

1. **Combine Search Types**: Use both node and fact searches
   ```python
   # Search for entities
   entities = await search_memory_nodes(query="user preferences")
   
   # Search for relationships
   relationships = await search_memory_facts(query="user prefers")
   ```

2. **Use Filters**: Narrow down results with entity types
   ```python
   preferences = await search_memory_nodes(
       query="communication style",
       entity_types=["Preference"],
       max_results=5
   )
   ```

3. **Center Searches**: Use center_node_uuid for related information
   ```python
   related_info = await search_memory_nodes(
       query="related topics",
       center_node_uuid=main_topic_uuid
   )
   ```

### Error Handling

```python
async def safe_memory_operation(operation, **kwargs):
    try:
        result = await operation(**kwargs)
        if hasattr(result, 'success') and not result.success:
            logger.error(f"Memory operation failed: {result.error}")
            return None
        return result
    except Exception as e:
        logger.error(f"Memory operation exception: {e}")
        return None
```

### Performance Optimization

1. **Batch Operations**: Group related memory operations
2. **Use Appropriate Limits**: Set reasonable max_results for searches
3. **Cache Frequently Used Data**: Store common queries in local cache
4. **Clean Up Regularly**: Remove outdated or irrelevant information

## Agent Memory Lifecycle

### Initialization
```python
async def initialize_agent(user_id: str):
    # Search for existing user context
    user_context = await search_memory_nodes(
        query="user profile preferences",
        group_id=user_id,
        max_results=10
    )
    
    if not user_context:
        # First-time user - create initial profile
        await add_memory(
            name="New User Profile",
            episode_body=f"New user {user_id} started session",
            group_id=user_id
        )
```

### Interaction Processing
```python
async def process_interaction(user_input: str, user_id: str):
    # 1. Retrieve relevant context
    context = await get_relevant_context(user_input, user_id)
    
    # 2. Generate contextual response
    response = await generate_response(user_input, context)
    
    # 3. Store interaction
    await store_interaction(user_input, response, user_id)
    
    # 4. Update learned patterns
    await update_patterns(user_input, response, user_id)
    
    return response
```

### Session Management
```python
async def end_session(user_id: str, session_summary: str):
    # Store session summary
    await add_memory(
        name="Session Summary",
        episode_body=session_summary,
        group_id=user_id,
        source="text"
    )
    
    # Update user model based on session
    await update_user_model(user_id, session_summary)
```

## Example: Customer Service Agent

```python
class CustomerServiceAgent:
    def __init__(self, mcp_client):
        self.mcp = mcp_client
    
    async def handle_inquiry(self, customer_id: str, inquiry: str):
        # Search for customer history
        history = await self.mcp.search_memory_nodes(
            query="customer history support tickets",
            group_id=f"customer_{customer_id}",
            max_results=5
        )
        
        # Search for similar issues
        similar_issues = await self.mcp.search_memory_facts(
            query=inquiry,
            group_id="support_knowledge"
        )
        
        # Generate contextual response
        response = await self.generate_support_response(
            inquiry, history, similar_issues
        )
        
        # Store the interaction
        await self.mcp.add_memory(
            name=f"Support Ticket: {inquiry[:50]}...",
            episode_body=json.dumps({
                "customer_id": customer_id,
                "inquiry": inquiry,
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "status": "resolved"
            }),
            source="json",
            group_id=f"customer_{customer_id}"
        )
        
        return response
```

## Advanced Patterns

### Multi-Agent Collaboration
```python
```python
# Agents can share knowledge through group_ids
shared_group = "project_alpha_shared"

# Agent A stores information
await agent_a.mcp.add_memory(
    name="Research Findings",
    episode_body=research_data,
    group_id=shared_group
)

```python
# Agent B retrieves the information
findings = await agent_b.mcp.search_memory_nodes(
    query="research findings",
    group_id=shared_group
)
```

### Hierarchical Memory
```python
# Global knowledge base
global_group = "global_knowledge"

# Domain-specific knowledge
domain_group = f"domain_{domain_name}"

# User-specific knowledge  
user_group = f"user_{user_id}"

# Search across hierarchies
all_context = []
for group in [user_group, domain_group, global_group]:
    context = await search_memory_nodes(query=query, group_id=group)
    all_context.extend(context)
```

## Troubleshooting

### Common Issues

1. **Memory Not Found**: Check group_id and search terms
2. **Slow Searches**: Use more specific queries and appropriate limits
3. **Context Overflow**: Implement context summarization for large results
4. **Inconsistent Behavior**: Ensure proper error handling and fallbacks

### Debugging Tips

```python
# Enable detailed logging
import logging
logging.getLogger('graphiti').setLevel(logging.DEBUG)

# Check memory contents
episodes = await get_episodes(group_id=user_id, limit=10)
print(f"Found {len(episodes)} episodes for user {user_id}")

# Validate search results
results = await search_memory_nodes(query="test", group_id=user_id)
for result in results:
    print(f"Found: {result.name} - {result.summary}")
```

## Next Steps

1. Review the [README.md](README.md) for installation and setup
2. Check [cursor_rules.md](cursor_rules.md) for specific IDE integration
3. Explore the [examples](../examples/) directory for complete implementations
4. Consider your agent's specific memory requirements and design patterns accordingly

For more advanced usage and API details, refer to the [Graphiti documentation](https://help.getzep.com/graphiti).