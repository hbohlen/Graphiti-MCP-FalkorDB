# AGENTS.md

This file provides guidance to AI agents when working with cross-encoder components.

## Directory Overview

This directory contains cross-encoder implementations for reranking search results and improving relevance scoring in Graphiti's search operations.

## Files

- `client.py` - Abstract base cross-encoder client interface
- `openai_reranker_client.py` - OpenAI-based reranking client
- `gemini_reranker_client.py` - Google Gemini reranking client
- `bge_reranker_client.py` - BGE (BAAI General Embedding) reranker client

## Cross-Encoder Architecture

### Purpose and Function

Cross-encoders improve search result relevance by:

1. **Relevance Scoring**: Calculate relevance scores between queries and documents
2. **Result Reranking**: Reorder search results based on computed relevance
3. **Quality Improvement**: Enhance search quality beyond initial retrieval
4. **Multi-modal Support**: Support different types of content and queries
5. **Provider Flexibility**: Multiple implementation options for different needs

### Reranking Process

1. **Initial Retrieval**: Get candidate results from primary search
2. **Relevance Scoring**: Calculate query-document relevance scores
3. **Result Reordering**: Sort results by relevance scores
4. **Final Results**: Return reranked, more relevant results

## Agent Guidelines

### Choosing a Reranker

1. **OpenAI**: Good general-purpose reranking with API convenience
2. **Gemini**: Google's reranking with potential multimodal capabilities
3. **BGE**: High-performance local reranking model, good for privacy/cost
4. **Custom**: Implement domain-specific reranking logic

### Reranker Configuration

```python
from graphiti_core.cross_encoder import OpenAIRerankerClient, BGERerankerClient

# OpenAI reranker setup
openai_reranker = OpenAIRerankerClient(
    api_key="your-api-key",
    model="text-similarity-curie-001",
    max_documents=100
)

# BGE reranker setup (local model)
bge_reranker = BGERerankerClient(
    model_name="BAAI/bge-reranker-large",
    device="cuda",  # or "cpu"
    max_length=512
)
```

### Using Rerankers in Search

```python
# Search with reranking
initial_results = await graphiti.search(
    query="machine learning research",
    limit=50  # Get more initial results
)

# Rerank results for better relevance
reranked_results = await reranker.rerank(
    query="machine learning research",
    documents=initial_results,
    top_k=10  # Return top 10 after reranking
)
```

### Best Practices for Agents

1. **Initial Retrieval Size**: Retrieve more candidates than final needed results
2. **Query Optimization**: Use clear, specific queries for better reranking
3. **Performance Balance**: Balance reranking quality vs. latency
4. **Result Validation**: Validate that reranking improves relevance
5. **Error Handling**: Handle reranking failures gracefully

### Provider-Specific Features

#### OpenAI Reranker
- **API-Based**: Cloud-based reranking service
- **General Purpose**: Good for most text reranking tasks
- **Scalability**: Handles varying loads through API
- **Cost**: Pay-per-use pricing model

#### Gemini Reranker
- **Multimodal Potential**: Support for text and other modalities
- **Integration**: Integration with Google services
- **Performance**: Competitive reranking quality
- **Global**: Worldwide availability

#### BGE Reranker
- **Local Deployment**: Runs locally for privacy and control
- **High Performance**: Excellent reranking quality
- **Cost Effective**: No API costs after initial setup
- **Customizable**: Can fine-tune for domain-specific tasks

### Performance Optimization

```python
# Optimize reranking performance
reranker_config = {
    "batch_size": 32,           # Process documents in batches
    "max_documents": 100,       # Limit documents to rerank
    "cache_results": True,      # Cache frequent queries
    "parallel_processing": True # Use parallel processing
}

# Use with search pipeline
optimized_results = await graphiti.search_with_reranking(
    query="research query",
    initial_limit=50,
    final_limit=10,
    reranker_config=reranker_config
)
```

### Integration with Search Pipeline

```python
from graphiti_core.search import SearchConfig
from graphiti_core.cross_encoder import OpenAIRerankerClient

# Configure search with reranking
search_config = SearchConfig(
    enable_reranking=True,
    reranker=OpenAIRerankerClient(api_key="your-key"),
    initial_results_limit=50,
    final_results_limit=10
)

# Execute search with automatic reranking
results = await graphiti.search(
    query="artificial intelligence applications",
    config=search_config
)
```

### Custom Reranking Logic

```python
from graphiti_core.cross_encoder.client import CrossEncoderClient

class CustomRerankerClient(CrossEncoderClient):
    def __init__(self, custom_config):
        self.config = custom_config
    
    async def rerank(self, query: str, documents: List[dict], top_k: int):
        # Implement custom reranking logic
        scores = []
        for doc in documents:
            score = self.calculate_custom_relevance(query, doc)
            scores.append((doc, score))
        
        # Sort by score and return top_k
        sorted_results = sorted(scores, key=lambda x: x[1], reverse=True)
        return [doc for doc, score in sorted_results[:top_k]]
    
    def calculate_custom_relevance(self, query: str, document: dict) -> float:
        # Domain-specific relevance calculation
        # Consider factors like:
        # - Semantic similarity
        # - Entity matching
        # - Temporal relevance
        # - Metadata alignment
        pass
```

### Evaluation and Testing

```python
# Evaluate reranking performance
async def evaluate_reranking():
    test_queries = [
        "machine learning algorithms",
        "natural language processing",
        "computer vision applications"
    ]
    
    for query in test_queries:
        # Get results without reranking
        baseline_results = await graphiti.search(query, limit=10)
        
        # Get results with reranking
        reranked_results = await graphiti.search_with_reranking(
            query, initial_limit=50, final_limit=10
        )
        
        # Compare relevance metrics
        baseline_relevance = calculate_relevance_score(query, baseline_results)
        reranked_relevance = calculate_relevance_score(query, reranked_results)
        
        improvement = reranked_relevance - baseline_relevance
        print(f"Query: {query}, Improvement: {improvement:.3f}")
```

### Error Handling

```python
from graphiti_core.cross_encoder.errors import RerankerError

async def safe_reranking(query, documents, reranker):
    try:
        reranked_results = await reranker.rerank(query, documents)
        return reranked_results
    except RerankerError as e:
        # Handle reranking errors
        logger.warning(f"Reranking failed: {e}, falling back to original order")
        return documents  # Return original order as fallback
    except Exception as e:
        logger.error(f"Unexpected reranking error: {e}")
        return documents
```

### Monitoring and Analytics

```python
# Monitor reranking performance
class RerankerMonitor:
    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "successful_reranks": 0,
            "failed_reranks": 0,
            "average_latency": 0,
            "relevance_improvements": []
        }
    
    async def track_reranking(self, query, documents, reranker):
        start_time = time.time()
        self.metrics["total_queries"] += 1
        
        try:
            results = await reranker.rerank(query, documents)
            self.metrics["successful_reranks"] += 1
            
            # Track latency
            latency = time.time() - start_time
            self.update_average_latency(latency)
            
            return results
        except Exception as e:
            self.metrics["failed_reranks"] += 1
            raise
```

### Cost Optimization

```python
# Optimize reranking costs
class CostOptimizedReranker:
    def __init__(self, primary_reranker, fallback_reranker):
        self.primary = primary_reranker      # High-quality, higher cost
        self.fallback = fallback_reranker    # Lower cost alternative
    
    async def rerank(self, query, documents, top_k):
        # Use different strategies based on criteria
        if len(documents) <= 20:
            # Small set: use high-quality reranker
            return await self.primary.rerank(query, documents, top_k)
        else:
            # Large set: use cost-effective approach
            # First pass with fallback reranker
            initial_results = await self.fallback.rerank(
                query, documents, top_k * 2
            )
            # Second pass with primary reranker
            final_results = await self.primary.rerank(
                query, initial_results, top_k
            )
            return final_results
```

### Best Practices Summary

1. **Provider Selection**: Choose reranker based on quality, cost, and latency requirements
2. **Result Size**: Retrieve more initial results than final needed count
3. **Performance Monitoring**: Track reranking effectiveness and performance
4. **Error Handling**: Implement graceful fallbacks for reranking failures
5. **Cost Management**: Balance reranking quality with computational costs