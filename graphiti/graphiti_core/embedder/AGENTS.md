# AGENTS.md

This file provides guidance to AI agents when working with embedding client components.

## Directory Overview

This directory contains embedding client implementations that enable Graphiti to generate vector embeddings for semantic search and similarity operations using various embedding providers.

## Files

- `client.py` - Abstract base embedding client interface
- `openai.py` - OpenAI embedding models client
- `azure_openai.py` - Azure OpenAI embedding service client
- `gemini.py` - Google Gemini embedding models client
- `voyage.py` - Voyage AI embedding models client

## Embedding Architecture

### Base Client (`client.py`)

Defines the abstract interface for all embedding clients:

- Text embedding generation
- Batch embedding operations
- Embedding dimensionality handling
- Rate limiting and error handling
- Cost estimation and monitoring

### Provider Implementations

Each provider offers different embedding models with varying characteristics:

1. **OpenAI**: High-quality general-purpose embeddings
2. **Azure OpenAI**: Enterprise OpenAI embeddings with Azure integration
3. **Google Gemini**: Multimodal embeddings with strong performance
4. **Voyage AI**: Specialized embeddings optimized for retrieval tasks

## Agent Guidelines

### Choosing an Embedding Provider

1. **OpenAI**: Best general-purpose choice, reliable and well-tested
2. **Voyage AI**: Optimized for retrieval tasks, excellent for search applications
3. **Gemini**: Good performance with potential multimodal capabilities
4. **Azure OpenAI**: For enterprise environments requiring Azure compliance

### Client Configuration

```python
from graphiti_core.embedder import OpenAIEmbedder, VoyageEmbedder

# OpenAI setup
openai_embedder = OpenAIEmbedder(
    api_key="your-api-key",
    model="text-embedding-3-large",  # or text-embedding-3-small
    dimensions=1536  # optional, model-dependent
)

# Voyage AI setup
voyage_embedder = VoyageEmbedder(
    api_key="your-api-key",
    model="voyage-large-2",
    dimensions=1024
)
```

### Best Practices for Agents

1. **Model Selection**: Choose models based on your performance and cost requirements
2. **Batch Processing**: Use batch operations for multiple texts to improve efficiency
3. **Caching**: Cache embeddings for frequently used texts
4. **Dimensionality**: Consider embedding dimensions vs. performance trade-offs
5. **Error Handling**: Implement robust retry logic for API failures

### Common Operations

All embedding clients support these operations:

1. **Single Text Embedding**: Generate embedding for individual text
2. **Batch Embedding**: Generate embeddings for multiple texts efficiently
3. **Similarity Calculation**: Compare embeddings for semantic similarity
4. **Dimension Management**: Handle different embedding dimensions
5. **Rate Limiting**: Manage API rate limits and costs

### Provider-Specific Features

#### OpenAI Embeddings
- **Model Variety**: Multiple models with different performance/cost trade-offs
- **Quality**: High-quality embeddings for general tasks
- **Reliability**: Consistent performance and high availability
- **Integration**: Seamless integration with OpenAI ecosystem

#### Voyage AI Embeddings
- **Retrieval Optimization**: Specifically optimized for retrieval tasks
- **Performance**: Excellent performance on search benchmarks
- **Efficiency**: Good balance of quality and computational efficiency
- **Specialization**: Focused on embedding quality for search applications

#### Google Gemini Embeddings
- **Multimodal Potential**: Support for text and potentially other modalities
- **Performance**: Competitive embedding quality
- **Integration**: Integration with Google Cloud services
- **Scaling**: Good scaling characteristics

#### Azure OpenAI Embeddings
- **Enterprise Features**: Enterprise-grade security and compliance
- **Geographic Distribution**: Multiple regions for data residency
- **Integration**: Deep integration with Azure services
- **Governance**: Enterprise governance and monitoring capabilities

### Performance Considerations

1. **Batch Size**: Optimize batch sizes for your provider and use case
2. **Caching Strategy**: Implement intelligent caching to reduce API calls
3. **Model Selection**: Balance embedding quality vs. cost and latency
4. **Rate Limiting**: Implement proper rate limiting to avoid API throttling
5. **Parallel Processing**: Use async operations for concurrent embedding generation

### Integration with Graphiti

Embeddings are used throughout Graphiti for:

1. **Semantic Search**: Finding semantically similar content
2. **Entity Similarity**: Comparing entities for deduplication
3. **Content Clustering**: Grouping related content together
4. **Recommendation**: Finding related entities and content
5. **Hybrid Search**: Combining with keyword and graph-based search

### Development Patterns

```python
# Basic embedding usage
embedder = OpenAIEmbedder(api_key="your-key")

# Single embedding
embedding = await embedder.embed_text("Your text here")

# Batch embeddings
texts = ["Text 1", "Text 2", "Text 3"]
embeddings = await embedder.embed_texts(texts)

# Calculate similarity
from graphiti_core.embedder.utils import cosine_similarity
similarity = cosine_similarity(embedding1, embedding2)
```

### Error Handling

```python
from graphiti_core.embedder.errors import EmbeddingError

try:
    embeddings = await embedder.embed_texts(texts)
except EmbeddingError as e:
    # Handle embedding-specific errors
    logger.error(f"Embedding error: {e}")
    # Implement fallback or retry logic
```

### Cost Optimization

1. **Model Selection**: Use smaller/cheaper models when quality requirements allow
2. **Caching**: Cache embeddings to avoid redundant API calls
3. **Batch Operations**: Use batch APIs for better cost efficiency
4. **Text Preprocessing**: Clean and optimize text before embedding
5. **Monitoring**: Track embedding costs and usage patterns

### Extension Guidelines

- **New Providers**: Implement new embedding providers following the base interface
- **Custom Models**: Support for custom or fine-tuned embedding models
- **Performance Optimization**: Provider-specific optimizations
- **Monitoring**: Enhanced monitoring and cost tracking
- **Caching**: Advanced caching strategies for different use cases