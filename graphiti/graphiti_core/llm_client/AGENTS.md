# AGENTS.md

This file provides guidance to AI agents when working with LLM client components.

## Directory Overview

This directory contains Large Language Model (LLM) client implementations that enable Graphiti to integrate with various AI providers for entity extraction, text processing, and knowledge graph operations.

## Files

- `client.py` - Abstract base LLM client interface
- `config.py` - Configuration classes for LLM clients
- `errors.py` - LLM-specific exception classes
- `utils.py` - Utility functions for LLM operations
- `openai_client.py` - OpenAI GPT models client
- `openai_base_client.py` - Base class for OpenAI-compatible clients
- `openai_generic_client.py` - Generic OpenAI-compatible API client
- `azure_openai_client.py` - Azure OpenAI service client
- `anthropic_client.py` - Anthropic Claude models client
- `gemini_client.py` - Google Gemini models client
- `groq_client.py` - Groq API client

## LLM Client Architecture

### Base Client (`client.py`)

Defines the abstract interface for all LLM clients:

- Text generation and completion
- Structured output generation
- Token counting and cost estimation
- Error handling and retry logic
- Rate limiting and throttling

### Provider Implementations

Each provider client implements the base interface with provider-specific optimizations:

1. **OpenAI**: Industry standard, excellent structured output support
2. **Anthropic**: High-quality reasoning, good for complex analysis
3. **Google Gemini**: Multimodal capabilities, competitive performance
4. **Groq**: High-speed inference, cost-effective for simple tasks
5. **Azure OpenAI**: Enterprise-grade OpenAI with Azure integration

## Agent Guidelines

### Choosing an LLM Provider

1. **OpenAI**: Best overall choice, reliable structured output
2. **Anthropic**: For complex reasoning and analysis tasks
3. **Gemini**: When multimodal capabilities are needed
4. **Groq**: For high-speed, cost-sensitive applications
5. **Azure**: For enterprise environments requiring Azure integration

### Client Configuration

```python
from graphiti_core.llm_client import OpenAIClient, AnthropicClient

# OpenAI setup
openai_client = OpenAIClient(
    api_key="your-api-key",
    model="gpt-4",
    temperature=0.1,
    max_tokens=4000
)

# Anthropic setup
anthropic_client = AnthropicClient(
    api_key="your-api-key", 
    model="claude-3-sonnet",
    temperature=0.1,
    max_tokens=4000
)
```

### Best Practices for Agents

1. **Structured Output**: Use providers that support structured output (OpenAI, Gemini)
2. **Error Handling**: Implement proper retry logic for API failures
3. **Rate Limiting**: Respect provider rate limits and implement backoff
4. **Cost Management**: Monitor token usage and costs
5. **Model Selection**: Choose appropriate models for your use case

### Common Operations

All LLM clients support these operations:

1. **Entity Extraction**: Extract entities and relationships from text
2. **Text Summarization**: Generate summaries of content
3. **Classification**: Categorize and classify content
4. **Deduplication**: Identify duplicate or similar entities
5. **Enrichment**: Add context and metadata to entities

### Provider-Specific Features

#### OpenAI
- **Function Calling**: Native support for structured outputs
- **Model Variety**: Multiple model sizes and capabilities
- **Reliability**: High uptime and consistent performance
- **Documentation**: Excellent API documentation and examples

#### Anthropic
- **Context Length**: Large context windows for long texts
- **Reasoning**: Excellent analytical and reasoning capabilities
- **Safety**: Built-in safety features and content filtering
- **Constitutional AI**: Trained with constitutional AI principles

#### Google Gemini
- **Multimodal**: Support for text, images, and other modalities
- **Integration**: Deep integration with Google services
- **Performance**: Competitive performance and pricing
- **Global**: Worldwide availability and localization

#### Groq
- **Speed**: Ultra-fast inference times
- **Cost**: Competitive pricing for simple tasks
- **Efficiency**: Optimized for high-throughput applications
- **Simplicity**: Straightforward API and usage patterns

### Development Guidelines

1. **Interface Compliance**: New clients must implement the base client interface
2. **Error Mapping**: Map provider-specific errors to common exceptions
3. **Testing**: Mock providers for unit testing, real providers for integration tests
4. **Configuration**: Support flexible configuration for different deployment environments
5. **Monitoring**: Implement logging and monitoring for API usage

### Performance Optimization

1. **Caching**: Cache results for repeated queries
2. **Batching**: Batch multiple requests when possible
3. **Parallel Processing**: Use async operations for concurrent requests
4. **Model Selection**: Use smaller models for simpler tasks
5. **Prompt Optimization**: Optimize prompts for efficiency and accuracy

### Error Handling Patterns

```python
from graphiti_core.llm_client.errors import LLMError, RateLimitError

try:
    result = await client.generate_response(prompt)
except RateLimitError:
    # Implement backoff and retry
    await asyncio.sleep(60)
    result = await client.generate_response(prompt)
except LLMError as e:
    # Handle other LLM errors
    logger.error(f"LLM error: {e}")
    raise
```

### Integration Considerations

- **Graphiti Integration**: How LLM clients work with Graphiti's graph operations
- **Prompt Management**: Centralized prompt templates and versioning
- **Output Validation**: Ensure LLM outputs meet expected schemas
- **Fallback Strategies**: Handle provider outages with fallback options
- **Cost Monitoring**: Track and optimize API usage costs