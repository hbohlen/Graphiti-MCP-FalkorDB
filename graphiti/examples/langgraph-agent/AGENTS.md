# AGENTS.md

This file provides guidance to AI agents when working with the LangGraph agent example.

## Directory Overview

This directory demonstrates how to build AI agents using LangChain's LangGraph framework combined with Graphiti's knowledge graph capabilities for persistent memory.

## Files

- `agent.ipynb` - Jupyter notebook with complete agent implementation
- `tinybirds-jess.png` - Visual asset used in the example

## Example Features

This example shows how to:

1. **LangGraph Integration**: Build conversational agents using LangGraph workflows
2. **Persistent Memory**: Use Graphiti as the memory layer for agents
3. **Contextual Awareness**: Maintain context across conversation sessions
4. **Knowledge Retrieval**: Search and retrieve relevant information from memory
5. **Real-time Updates**: Update knowledge graph during conversations

## Prerequisites

- Python 3.9+
- Jupyter Notebook environment
- OpenAI API key
- Neo4j or FalkorDB database
- LangSmith API key (optional, for tracing)

## Agent Guidelines

### Environment Setup

```bash
# Required LLM access
export OPENAI_API_KEY=your_openai_api_key

# Database configuration
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password

# Optional: LangSmith tracing
export LANGSMITH_API_KEY=your_langsmith_key
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT="Graphiti LangGraph Tutorial"
```

### Running the Example

```bash
# Install dependencies (if not already installed)
pip install graphiti-core langgraph langchain

# Start Jupyter and open agent.ipynb
jupyter notebook agent.ipynb
```

### Key Concepts

1. **Agent Architecture**: Understanding LangGraph node and edge patterns
2. **Memory Integration**: How Graphiti serves as persistent memory
3. **Context Management**: Maintaining conversation state and history
4. **Search Strategies**: Using Graphiti's search capabilities within agent workflows
5. **Knowledge Updates**: Real-time graph updates during conversations

### LangGraph Patterns

- **State Management**: How conversation state flows through graph nodes
- **Tool Integration**: Incorporating Graphiti tools into agent workflows  
- **Conditional Logic**: Decision-making patterns in agent behavior
- **Error Handling**: Robust error handling in distributed agent systems

### Graphiti Integration Patterns

- **Episode Creation**: Converting conversations into graph episodes
- **Entity Extraction**: Automatic extraction during conversation flow
- **Relationship Modeling**: Building entity relationships from interactions
- **Temporal Tracking**: Maintaining conversation timeline and context

### Best Practices for Agents

1. **Memory First**: Always search memory before external operations
2. **Incremental Updates**: Update knowledge graph incrementally during conversations
3. **Context Preservation**: Maintain conversation context across sessions
4. **Error Recovery**: Implement graceful error handling and recovery
5. **Performance**: Consider latency implications of graph operations

### Use Cases

- **Conversational AI**: Building chatbots with long-term memory
- **Customer Support**: Agents that remember customer history and preferences
- **Personal Assistants**: AI assistants with persistent knowledge about users
- **Knowledge Workers**: Agents that accumulate domain expertise over time

### Advanced Patterns

- **Multi-turn Conversations**: Handling complex conversation flows
- **Context Switching**: Managing multiple conversation threads
- **Knowledge Synthesis**: Combining information from multiple sources
- **Personalization**: Adapting agent behavior based on user history