# AGENTS.md

This file provides guidance to AI agents when working with embedding tests.

## Directory Overview

This directory contains tests for various embedding providers and embedding-related functionality, ensuring that embedding operations work correctly across different providers and use cases.

## Test Coverage

### Embedding Provider Tests

Tests for different embedding providers:

1. **OpenAI Embeddings**: Test OpenAI embedding API integration
2. **Voyage AI Embeddings**: Test Voyage AI embedding functionality
3. **Azure OpenAI Embeddings**: Test Azure OpenAI embedding service
4. **Google Gemini Embeddings**: Test Google Gemini embedding capabilities

### Test Categories

1. **Unit Tests**: Test embedding client functionality in isolation
2. **Integration Tests**: Test embedding operations with real APIs
3. **Performance Tests**: Test embedding generation speed and efficiency
4. **Quality Tests**: Test embedding quality and consistency

## Agent Guidelines

### Running Embedding Tests

```bash
# Run all embedding tests
pytest tests/embedder/

# Run specific provider tests
pytest tests/embedder/test_openai_embedder.py
pytest tests/embedder/test_voyage_embedder.py

# Run with real API keys (integration tests)
OPENAI_API_KEY=real_key pytest tests/embedder/ -k "integration"

# Run performance tests
pytest tests/embedder/ -k "performance"
```

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch
from graphiti_core.embedder import OpenAIEmbedder
import numpy as np

class TestOpenAIEmbedder:
    @pytest.fixture
    def mock_openai_client(self):
        client = AsyncMock()
        # Mock embedding response
        client.embeddings.create.return_value.data = [
            type('obj', (object,), {'embedding': [0.1, 0.2, 0.3] * 512})()
        ]
        return client
    
    @pytest.fixture
    def embedder(self, mock_openai_client):
        with patch('openai.AsyncOpenAI', return_value=mock_openai_client):
            return OpenAIEmbedder(api_key="test_key")
    
    @pytest.mark.asyncio
    async def test_embed_single_text(self, embedder):
        """Test embedding generation for single text."""
        text = "This is a test sentence."
        embedding = await embedder.embed_text(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 1536  # OpenAI embedding dimension
        assert all(isinstance(x, float) for x in embedding)
    
    @pytest.mark.asyncio
    async def test_embed_batch_texts(self, embedder):
        """Test batch embedding generation."""
        texts = ["First text", "Second text", "Third text"]
        embeddings = await embedder.embed_texts(texts)
        
        assert len(embeddings) == 3
        assert all(len(emb) == 1536 for emb in embeddings)
    
    def test_embedding_dimensions(self, embedder):
        """Test that embedder reports correct dimensions."""
        assert embedder.dimensions == 1536
    
    @pytest.mark.asyncio
    async def test_error_handling(self, embedder):
        """Test error handling for API failures."""
        with patch.object(embedder, '_client') as mock_client:
            mock_client.embeddings.create.side_effect = Exception("API Error")
            
            with pytest.raises(EmbeddingError):
                await embedder.embed_text("test text")
```

### Integration Testing

```python
@pytest.mark.integration
class TestEmbedderIntegration:
    @pytest.fixture
    def real_embedder(self):
        """Create embedder with real API key for integration tests."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        return OpenAIEmbedder(api_key=api_key)
    
    @pytest.mark.asyncio
    async def test_real_embedding_generation(self, real_embedder):
        """Test embedding generation with real API."""
        text = "Machine learning is a subset of artificial intelligence."
        embedding = await real_embedder.embed_text(text)
        
        assert isinstance(embedding, list)
        assert len(embedding) == 1536
        assert all(-1 <= x <= 1 for x in embedding)  # Normalized embeddings
    
    @pytest.mark.asyncio
    async def test_semantic_similarity(self, real_embedder):
        """Test that similar texts have similar embeddings."""
        text1 = "The cat sat on the mat."
        text2 = "A cat was sitting on a mat."
        text3 = "The dog ran in the park."
        
        emb1 = await real_embedder.embed_text(text1)
        emb2 = await real_embedder.embed_text(text2)
        emb3 = await real_embedder.embed_text(text3)
        
        # Calculate cosine similarity
        sim_12 = cosine_similarity(emb1, emb2)
        sim_13 = cosine_similarity(emb1, emb3)
        
        # Similar texts should be more similar
        assert sim_12 > sim_13
        assert sim_12 > 0.8  # High similarity threshold
```

### Performance Testing

```python
@pytest.mark.performance
class TestEmbedderPerformance:
    @pytest.mark.asyncio
    async def test_batch_embedding_performance(self, real_embedder):
        """Test performance of batch embedding operations."""
        texts = [f"Test sentence number {i}" for i in range(100)]
        
        # Test individual embeddings
        start_time = time.time()
        individual_embeddings = []
        for text in texts:
            emb = await real_embedder.embed_text(text)
            individual_embeddings.append(emb)
        individual_time = time.time() - start_time
        
        # Test batch embeddings
        start_time = time.time()
        batch_embeddings = await real_embedder.embed_texts(texts)
        batch_time = time.time() - start_time
        
        # Batch should be significantly faster
        assert batch_time < individual_time * 0.5
        assert len(batch_embeddings) == len(texts)
        
        # Results should be identical
        for i, (ind_emb, batch_emb) in enumerate(zip(individual_embeddings, batch_embeddings)):
            similarity = cosine_similarity(ind_emb, batch_emb)
            assert similarity > 0.99, f"Embedding {i} differs between individual and batch"
    
    @pytest.mark.asyncio
    async def test_concurrent_embedding_generation(self, real_embedder):
        """Test concurrent embedding generation."""
        texts = [f"Concurrent test {i}" for i in range(20)]
        
        # Generate embeddings concurrently
        tasks = [real_embedder.embed_text(text) for text in texts]
        start_time = time.time()
        embeddings = await asyncio.gather(*tasks)
        concurrent_time = time.time() - start_time
        
        assert len(embeddings) == 20
        assert concurrent_time < 30  # Should complete within 30 seconds
```

### Quality Testing

```python
class TestEmbeddingQuality:
    @pytest.mark.asyncio
    async def test_embedding_consistency(self, real_embedder):
        """Test that same text produces consistent embeddings."""
        text = "Consistency test sentence."
        
        # Generate embedding multiple times
        embeddings = []
        for _ in range(3):
            emb = await real_embedder.embed_text(text)
            embeddings.append(emb)
        
        # All embeddings should be identical (deterministic)
        for emb in embeddings[1:]:
            similarity = cosine_similarity(embeddings[0], emb)
            assert similarity > 0.999, "Embeddings should be deterministic"
    
    @pytest.mark.asyncio
    async def test_embedding_normalization(self, real_embedder):
        """Test that embeddings are properly normalized."""
        text = "Normalization test."
        embedding = await real_embedder.embed_text(text)
        
        # Calculate L2 norm
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.001, "Embedding should be normalized"
    
    @pytest.mark.asyncio
    async def test_empty_text_handling(self, real_embedder):
        """Test handling of empty or whitespace text."""
        empty_texts = ["", "   ", "\n\t  "]
        
        for text in empty_texts:
            with pytest.raises(ValueError):
                await real_embedder.embed_text(text)
```

### Cross-Provider Testing

```python
class TestCrossProviderCompatibility:
    @pytest.fixture
    def all_embedders(self):
        """Create embedders for all available providers."""
        embedders = {}
        
        if os.getenv("OPENAI_API_KEY"):
            embedders["openai"] = OpenAIEmbedder(api_key=os.getenv("OPENAI_API_KEY"))
        
        if os.getenv("VOYAGE_API_KEY"):
            embedders["voyage"] = VoyageEmbedder(api_key=os.getenv("VOYAGE_API_KEY"))
        
        return embedders
    
    @pytest.mark.asyncio
    async def test_cross_provider_similarity(self, all_embedders):
        """Test that different providers produce reasonable similarities."""
        if len(all_embedders) < 2:
            pytest.skip("Need at least 2 embedding providers")
        
        text = "Cross-provider similarity test."
        embeddings = {}
        
        for provider, embedder in all_embedders.items():
            embeddings[provider] = await embedder.embed_text(text)
        
        # Compare embeddings across providers
        providers = list(embeddings.keys())
        for i in range(len(providers)):
            for j in range(i + 1, len(providers)):
                provider1, provider2 = providers[i], providers[j]
                
                # Normalize embeddings to same dimension if needed
                emb1 = normalize_embedding(embeddings[provider1])
                emb2 = normalize_embedding(embeddings[provider2])
                
                similarity = cosine_similarity(emb1, emb2)
                
                # Different providers should still show some correlation
                assert similarity > 0.3, f"Low similarity between {provider1} and {provider2}"
```

### Utility Functions for Testing

```python
def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)

def normalize_embedding(embedding, target_dim=None):
    """Normalize embedding vector."""
    embedding = np.array(embedding)
    if target_dim and len(embedding) != target_dim:
        # Truncate or pad to target dimension
        if len(embedding) > target_dim:
            embedding = embedding[:target_dim]
        else:
            embedding = np.pad(embedding, (0, target_dim - len(embedding)))
    
    # L2 normalize
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding.tolist()

@pytest.fixture
def sample_texts():
    """Sample texts for embedding tests."""
    return [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning algorithms require large datasets.",
        "Python is a popular programming language for data science.",
        "Natural language processing enables computers to understand text.",
        "Graph databases store data as nodes and relationships."
    ]
```

### Test Configuration

```python
# conftest.py for embedder tests
import pytest
import os

def pytest_configure(config):
    """Configure embedding tests."""
    config.addinivalue_line(
        "markers", "integration: require real API keys"
    )
    config.addinivalue_line(
        "markers", "performance: performance benchmarks"
    )

@pytest.fixture(scope="session")
def check_api_keys():
    """Check if required API keys are available."""
    required_keys = ["OPENAI_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        pytest.skip(f"Missing API keys: {missing_keys}")

def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle API key requirements."""
    for item in items:
        if "integration" in item.keywords:
            if not os.getenv("OPENAI_API_KEY"):
                item.add_marker(pytest.mark.skip(reason="API key required"))
```

### Best Practices Summary

1. **Provider Coverage**: Test all supported embedding providers
2. **Quality Validation**: Verify embedding quality and consistency
3. **Performance Testing**: Test batch operations and concurrent processing
4. **Error Handling**: Test error scenarios and recovery
5. **Cross-Provider Compatibility**: Ensure reasonable behavior across providers