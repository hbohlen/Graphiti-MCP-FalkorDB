# AGENTS.md

This file provides guidance to AI agents when working with the test suite.

## Directory Overview

This directory contains the comprehensive test suite for Graphiti, including unit tests, integration tests, and evaluation scripts. The tests ensure code quality, functionality, and performance across all components.

## Test Structure

### Test Categories

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions and database operations
3. **Evaluation Tests**: End-to-end evaluation scripts and benchmarks
4. **Performance Tests**: Load testing and performance benchmarks
5. **Component Tests**: Tests for specific modules and subdirectories

### Test Organization

Tests are organized by component:
- `embedder/` - Embedding provider tests
- `llm_client/` - LLM provider tests
- `driver/` - Database driver tests
- `utils/` - Utility function tests
- `cross_encoder/` - Cross-encoder and reranking tests
- `evals/` - Evaluation scripts and benchmarks

## Agent Guidelines

### Running Tests

```bash
# Run all tests
make test

# Run specific test files
pytest tests/test_specific_file.py

# Run tests with coverage
pytest --cov=graphiti_core tests/

# Run only unit tests (exclude integration)
pytest tests/ -k "not _int"

# Run only integration tests
pytest tests/ -k "_int"

# Run tests in parallel
pytest -n auto tests/
```

### Test Environment Setup

```bash
# Install test dependencies
uv sync --extra dev

# Set up test environment variables
export OPENAI_API_KEY=test_key
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=test_password

# For integration tests, ensure database is running
docker run -d --name neo4j-test -p 7687:7687 -p 7474:7474 \
  --env NEO4J_AUTH=neo4j/test_password \
  neo4j:5.22.0
```

### Best Practices for Agents

1. **Test Isolation**: Each test should be independent and repeatable
2. **Mock External Dependencies**: Use mocks for external APIs and services
3. **Database Testing**: Use test databases, never production data
4. **Test Data**: Create minimal, focused test data for each test case
5. **Error Testing**: Test both success and failure scenarios

### Writing Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, patch
from graphiti_core import Graphiti
from graphiti_core.models.nodes import EntityNode

class TestEntityOperations:
    @pytest.fixture
    def mock_driver(self):
        driver = AsyncMock()
        driver.create_node.return_value = EntityNode(
            uuid="test-uuid",
            name="Test Entity",
            type="TestType",
            summary="Test summary"
        )
        return driver
    
    @pytest.fixture
    def graphiti_instance(self, mock_driver):
        return Graphiti(driver=mock_driver)
    
    @pytest.mark.asyncio
    async def test_create_entity(self, graphiti_instance, mock_driver):
        # Test entity creation
        entity_data = {
            "name": "Test Entity",
            "type": "TestType",
            "summary": "Test summary"
        }
        
        result = await graphiti_instance.create_entity(**entity_data)
        
        # Assertions
        assert result.name == "Test Entity"
        assert result.type == "TestType"
        mock_driver.create_node.assert_called_once()
    
    def test_entity_validation(self):
        # Test data validation
        with pytest.raises(ValidationError):
            EntityNode(name="", type="TestType")  # Empty name should fail
```

### Integration Testing

```python
import pytest
from graphiti_core import Graphiti
from graphiti_core.driver import Neo4jDriver

@pytest.mark.integration
class TestGraphitiIntegration:
    @pytest.fixture(scope="class")
    async def graphiti_instance(self):
        # Setup real database connection for integration tests
        driver = Neo4jDriver(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="test_password",
            database="test_db"
        )
        
        graphiti = Graphiti(driver=driver)
        await graphiti.initialize()
        
        yield graphiti
        
        # Cleanup after tests
        await graphiti.clear_graph()
        await graphiti.close()
    
    @pytest.mark.asyncio
    async def test_end_to_end_episode_processing(self, graphiti_instance):
        # Test complete episode processing workflow
        episode_data = {
            "name": "Integration Test Episode",
            "content": "This is a test episode with entities like John Doe and TechCorp.",
            "timestamp": datetime.utcnow()
        }
        
        # Add episode
        episode = await graphiti_instance.add_episode(**episode_data)
        assert episode.uuid is not None
        
        # Search for extracted entities
        search_results = await graphiti_instance.search_nodes(
            query="John Doe",
            limit=10
        )
        
        # Verify entities were extracted
        assert len(search_results) > 0
        entity_names = [entity.name for entity in search_results]
        assert any("John" in name for name in entity_names)
```

### Mock Strategies

```python
# Mock external API calls
@patch('graphiti_core.llm_client.openai_client.OpenAI')
async def test_llm_integration(mock_openai):
    # Setup mock response
    mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = json.dumps({
        "entities": [{"name": "Test Entity", "type": "Person"}]
    })
    
    # Test LLM client
    client = OpenAIClient(api_key="test_key")
    result = await client.extract_entities("Test text")
    
    assert len(result.entities) == 1
    assert result.entities[0].name == "Test Entity"

# Mock database operations
@pytest.fixture
def mock_neo4j_session():
    session = AsyncMock()
    session.run.return_value.single.return_value = {"count": 1}
    return session

async def test_database_query(mock_neo4j_session):
    # Test database operations with mocked session
    query = "MATCH (n) RETURN count(n) as count"
    result = await mock_neo4j_session.run(query).single()
    
    assert result["count"] == 1
```

### Performance Testing

```python
import time
import asyncio
from memory_profiler import profile

class TestPerformance:
    @pytest.mark.performance
    async def test_batch_episode_processing_performance(self, graphiti_instance):
        # Test performance of batch operations
        episodes = [
            {
                "name": f"Episode {i}",
                "content": f"Test content for episode {i}",
                "timestamp": datetime.utcnow()
            }
            for i in range(100)
        ]
        
        start_time = time.time()
        
        # Process episodes in batch
        tasks = [
            graphiti_instance.add_episode(**episode)
            for episode in episodes
        ]
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Performance assertions
        assert len(results) == 100
        assert processing_time < 60  # Should complete within 60 seconds
        
        # Calculate throughput
        throughput = len(episodes) / processing_time
        assert throughput > 1  # At least 1 episode per second
    
    @profile
    def test_memory_usage(self):
        # Test memory usage patterns
        entities = []
        for i in range(1000):
            entity = EntityNode(
                name=f"Entity {i}",
                type="TestType",
                summary=f"Summary for entity {i}"
            )
            entities.append(entity)
        
        # Memory usage should be reasonable
        assert len(entities) == 1000
```

### Test Data Management

```python
@pytest.fixture
def sample_episode_data():
    return {
        "name": "Sample Episode",
        "content": "This episode contains information about Alice working at TechCorp on ML projects.",
        "timestamp": datetime(2024, 1, 1, 12, 0, 0)
    }

@pytest.fixture
def sample_entities():
    return [
        EntityNode(name="Alice", type="Person", summary="Software engineer"),
        EntityNode(name="TechCorp", type="Organization", summary="Technology company"),
        EntityNode(name="ML Projects", type="Project", summary="Machine learning initiatives")
    ]

@pytest.fixture
def sample_relationships():
    return [
        {
            "source_name": "Alice",
            "target_name": "TechCorp", 
            "relationship_type": "WORKS_FOR",
            "summary": "Alice is employed by TechCorp"
        },
        {
            "source_name": "Alice",
            "target_name": "ML Projects",
            "relationship_type": "WORKS_ON",
            "summary": "Alice contributes to ML projects"
        }
    ]

# Use fixtures in tests
async def test_entity_creation_with_fixtures(sample_entities, graphiti_instance):
    for entity in sample_entities:
        created_entity = await graphiti_instance.create_entity(
            name=entity.name,
            type=entity.type,
            summary=entity.summary
        )
        assert created_entity.name == entity.name
```

### Test Configuration

```python
# conftest.py - pytest configuration
import pytest
import asyncio
from graphiti_core import Graphiti
from graphiti_core.driver import Neo4jDriver

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_database():
    """Setup test database for integration tests."""
    driver = Neo4jDriver(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="test_password",
        database="test_db"
    )
    
    # Initialize test database
    await driver.initialize()
    
    yield driver
    
    # Cleanup test database
    await driver.clear_database()
    await driver.close()

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
```

### Continuous Integration

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      neo4j:
        image: neo4j:5.22.0
        env:
          NEO4J_AUTH: neo4j/test_password
        ports:
          - 7687:7687
          - 7474:7474
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install uv
        uv sync --extra dev
    
    - name: Run tests
      run: |
        pytest tests/ --cov=graphiti_core --cov-report=xml
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        NEO4J_URI: bolt://localhost:7687
        NEO4J_USER: neo4j
        NEO4J_PASSWORD: test_password
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Test Documentation

```python
"""
Test Module: Entity Operations

This module tests the core entity operations in Graphiti including:
- Entity creation and validation
- Entity search and retrieval  
- Entity relationships
- Entity metadata handling

Test Categories:
- Unit tests: Test individual entity operations
- Integration tests: Test entity operations with real database
- Performance tests: Test entity operation performance

Prerequisites:
- Neo4j test database running on localhost:7687
- Test environment variables set
- Test data fixtures available
"""

class TestEntityOperations:
    """Test suite for entity operations."""
    
    async def test_create_entity_success(self):
        """Test successful entity creation with valid data."""
        pass
    
    async def test_create_entity_validation_error(self):
        """Test entity creation with invalid data raises ValidationError."""
        pass
    
    async def test_search_entities_by_type(self):
        """Test entity search filtered by entity type."""
        pass
```

### Best Practices Summary

1. **Test Organization**: Organize tests by component and functionality
2. **Test Isolation**: Ensure tests are independent and don't affect each other
3. **Comprehensive Coverage**: Test both success and failure scenarios
4. **Performance Testing**: Include performance and load tests
5. **Documentation**: Document test purposes and requirements clearly