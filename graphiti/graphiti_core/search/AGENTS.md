# AGENTS.md

This file provides guidance to AI agents when working with search components.

## Directory Overview

This directory contains Graphiti's hybrid search implementation that combines semantic embeddings, keyword search (BM25), and graph traversal to provide powerful and flexible search capabilities.

## Files

- `search.py` - Main search implementation and orchestration
- `search_config.py` - Search configuration classes and settings
- `search_config_recipes.py` - Predefined search configurations for common use cases
- `search_filters.py` - Search filtering and criteria classes
- `search_helpers.py` - Helper functions for search operations
- `search_utils.py` - Utility functions for search processing

## Search Architecture

### Hybrid Search Approach

Graphiti's search combines three complementary approaches:

1. **Semantic Search**: Vector similarity using embeddings
2. **Keyword Search**: BM25-based full-text search
3. **Graph Search**: Graph traversal and relationship-based search

### Search Types

1. **Edge Search**: Find relationships/facts between entities
2. **Node Search**: Find specific entities or concepts
3. **Hybrid Search**: Combine multiple search strategies
4. **Graph-Based Reranking**: Use graph distance to improve relevance

## Agent Guidelines

### Search Configuration

```python
from graphiti_core.search import SearchConfig, SearchType

# Basic search configuration
config = SearchConfig(
    search_type=SearchType.HYBRID,
    limit=10,
    embedding_weight=0.7,
    bm25_weight=0.3,
    graph_weight=0.0
)

# Use predefined recipes
from graphiti_core.search.search_config_recipes import DEFAULT_EDGE_SEARCH_CONFIG
config = DEFAULT_EDGE_SEARCH_CONFIG
```

### Search Operations

```python
# Search for edges/relationships
edge_results = await graphiti.search(
    query="relationship between entities",
    config=edge_search_config
)

# Search for nodes/entities
node_results = await graphiti.search_nodes(
    query="specific entity",
    config=node_search_config
)

# Graph-based reranking
reranked_results = await graphiti.search_rerank(
    query="search query",
    center_node_uuid="node-uuid",
    config=search_config
)
```

### Best Practices for Agents

1. **Query Optimization**: Craft specific, well-structured queries
2. **Configuration Tuning**: Adjust weights based on your use case
3. **Result Filtering**: Use filters to narrow down results
4. **Performance Monitoring**: Monitor search performance and adjust accordingly
5. **Relevance Validation**: Validate search results for your specific domain

### Search Strategies

#### Semantic Search
- **Best For**: Conceptual similarity, fuzzy matching, multilingual search
- **Configuration**: High embedding weight, low keyword weight
- **Use Cases**: "Find similar concepts", "Related topics"

#### Keyword Search (BM25)
- **Best For**: Exact term matching, specific entities, precise queries
- **Configuration**: High BM25 weight, low embedding weight
- **Use Cases**: "Find specific names", "Exact phrase matching"

#### Graph Search
- **Best For**: Relationship discovery, connected entities, contextual search
- **Configuration**: Graph traversal with relationship weights
- **Use Cases**: "Find connected entities", "Discover relationships"

#### Hybrid Search
- **Best For**: Most general-purpose searches, balanced relevance
- **Configuration**: Balanced weights across all search types
- **Use Cases**: Most real-world search scenarios

### Search Filtering

```python
from graphiti_core.search import SearchFilters

# Apply filters to search
filters = SearchFilters(
    entity_types=["Person", "Organization"],
    date_range=(start_date, end_date),
    confidence_threshold=0.8
)

results = await graphiti.search(
    query="search query",
    config=search_config,
    filters=filters
)
```

### Performance Optimization

1. **Index Optimization**: Ensure proper database indices for search fields
2. **Query Specificity**: More specific queries generally perform better
3. **Result Limiting**: Use appropriate limits to balance thoroughness vs. speed
4. **Caching**: Cache frequent search results when appropriate
5. **Batch Operations**: Combine multiple searches when possible

### Search Configuration Recipes

The system provides predefined configurations for common scenarios:

1. **DEFAULT_EDGE_SEARCH_CONFIG**: Optimized for finding relationships
2. **DEFAULT_NODE_SEARCH_CONFIG**: Optimized for finding entities
3. **SEMANTIC_HEAVY_CONFIG**: Emphasizes semantic similarity
4. **KEYWORD_HEAVY_CONFIG**: Emphasizes exact matching
5. **GRAPH_HEAVY_CONFIG**: Emphasizes relationship traversal

### Common Search Patterns

#### Entity Discovery
```python
# Find entities related to a concept
results = await graphiti.search_nodes(
    query="artificial intelligence researchers",
    config=DEFAULT_NODE_SEARCH_CONFIG
)
```

#### Relationship Exploration
```python
# Find relationships involving specific entities
results = await graphiti.search(
    query="collaboration between universities and companies",
    config=DEFAULT_EDGE_SEARCH_CONFIG
)
```

#### Contextual Search
```python
# Search with context from a specific node
results = await graphiti.search_rerank(
    query="machine learning projects",
    center_node_uuid="university-node-uuid",
    config=search_config
)
```

### Advanced Features

1. **Multi-modal Search**: Combine text with other data types
2. **Temporal Search**: Search with time-based constraints
3. **Confidence Scoring**: Relevance scores for search results
4. **Explain Functionality**: Understanding why results were returned
5. **Custom Scoring**: Implement custom relevance scoring

### Troubleshooting Search Issues

1. **Poor Results**: Adjust search weights, check query specificity
2. **Slow Performance**: Check indices, reduce result limits, optimize queries
3. **Missing Results**: Verify data exists, check filters, broaden search criteria
4. **Irrelevant Results**: Increase specificity, adjust configuration weights
5. **Inconsistent Results**: Check data quality, validate embedding consistency

### Extension Points

- **Custom Search Strategies**: Implement new search algorithms
- **Custom Scoring**: Add domain-specific relevance scoring
- **Search Analytics**: Enhanced search result analytics and monitoring
- **Query Enhancement**: Automatic query expansion and refinement
- **Performance Optimization**: Search-specific performance improvements