# AGENTS.md

This file provides guidance to AI agents when working with evaluation scripts and benchmarks.

## Directory Overview

This directory contains evaluation scripts and benchmarks for assessing Graphiti's performance on various tasks, datasets, and real-world scenarios. These evaluations help measure the quality and effectiveness of knowledge graph operations.

## Evaluation Categories

### Performance Evaluations

1. **Memory Benchmarks**: Test long-term memory capabilities
2. **Search Quality**: Evaluate search relevance and accuracy
3. **Entity Extraction**: Assess entity extraction quality
4. **Relationship Discovery**: Measure relationship identification accuracy
5. **Scalability Tests**: Test performance with large datasets

### Dataset Evaluations

1. **Academic Datasets**: Evaluation on research datasets
2. **Domain-Specific**: Industry and domain-specific evaluations
3. **Synthetic Data**: Controlled evaluation scenarios
4. **Real-World Data**: Production-like data evaluations

## Agent Guidelines

### Running Evaluations

```bash
# Run all evaluations
pytest tests/evals/

# Run specific evaluation
python tests/evals/memory_benchmark.py

# Run with specific configuration
python tests/evals/search_evaluation.py --config production

# Generate evaluation report
python tests/evals/generate_report.py --output results/
```

### Evaluation Framework

```python
import asyncio
import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from graphiti_core import Graphiti

@dataclass
class EvaluationResult:
    """Standard evaluation result structure."""
    test_name: str
    metrics: Dict[str, float]
    duration: float
    success: bool
    error: str = None
    metadata: Dict[str, Any] = None

class EvaluationFramework:
    """Base framework for running evaluations."""
    
    def __init__(self, graphiti: Graphiti, config: Dict[str, Any]):
        self.graphiti = graphiti
        self.config = config
        self.results = []
    
    async def run_evaluation(self, test_name: str, test_func) -> EvaluationResult:
        """Run a single evaluation test."""
        start_time = time.time()
        
        try:
            metrics = await test_func()
            duration = time.time() - start_time
            
            result = EvaluationResult(
                test_name=test_name,
                metrics=metrics,
                duration=duration,
                success=True
            )
        except Exception as e:
            duration = time.time() - start_time
            result = EvaluationResult(
                test_name=test_name,
                metrics={},
                duration=duration,
                success=False,
                error=str(e)
            )
        
        self.results.append(result)
        return result
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report."""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.success)
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
                "total_duration": sum(r.duration for r in self.results)
            },
            "results": [
                {
                    "test_name": r.test_name,
                    "success": r.success,
                    "metrics": r.metrics,
                    "duration": r.duration,
                    "error": r.error
                }
                for r in self.results
            ]
        }
```

### Memory Evaluation

```python
class MemoryEvaluation:
    """Evaluate long-term memory capabilities."""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def evaluate_memory_retention(self, episodes: List[Dict]) -> Dict[str, float]:
        """Test memory retention across episodes."""
        # Add episodes over time
        episode_uuids = []
        for episode in episodes:
            result = await self.graphiti.add_episode(**episode)
            episode_uuids.append(result.uuid)
            await asyncio.sleep(0.1)  # Simulate time passage
        
        # Test retrieval of information from early episodes
        early_episode_queries = [
            "information from first episode",
            "early concepts mentioned",
            "initial relationships"
        ]
        
        retrieval_scores = []
        for query in early_episode_queries:
            results = await self.graphiti.search(query, limit=10)
            
            # Calculate relevance score
            relevance_score = self.calculate_relevance(query, results)
            retrieval_scores.append(relevance_score)
        
        return {
            "memory_retention_score": sum(retrieval_scores) / len(retrieval_scores),
            "episodes_processed": len(episodes),
            "average_retrieval_score": sum(retrieval_scores) / len(retrieval_scores)
        }
    
    async def evaluate_memory_consolidation(self) -> Dict[str, float]:
        """Test how well information is consolidated over time."""
        # Add related episodes
        related_episodes = [
            {"name": "ML Basics", "content": "Machine learning uses algorithms to find patterns in data."},
            {"name": "ML Applications", "content": "Machine learning applications include recommendation systems and image recognition."},
            {"name": "ML Challenges", "content": "Machine learning challenges include overfitting and data quality issues."}
        ]
        
        for episode in related_episodes:
            await self.graphiti.add_episode(**episode)
        
        # Test consolidated knowledge retrieval
        consolidated_query = "machine learning overview"
        results = await self.graphiti.search(consolidated_query, limit=10)
        
        # Measure how well information from multiple episodes is integrated
        integration_score = self.measure_information_integration(results, related_episodes)
        
        return {
            "consolidation_score": integration_score,
            "episodes_integrated": len(related_episodes),
            "consolidated_entities": len(results)
        }
```

### Search Quality Evaluation

```python
class SearchQualityEvaluation:
    """Evaluate search quality and relevance."""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def evaluate_search_relevance(self, test_queries: List[Dict]) -> Dict[str, float]:
        """Evaluate search result relevance."""
        relevance_scores = []
        
        for query_data in test_queries:
            query = query_data["query"]
            expected_entities = query_data.get("expected_entities", [])
            
            # Perform search
            results = await self.graphiti.search_nodes(query, limit=20)
            
            # Calculate relevance metrics
            precision = self.calculate_precision(results, expected_entities)
            recall = self.calculate_recall(results, expected_entities)
            f1_score = self.calculate_f1_score(precision, recall)
            
            relevance_scores.append({
                "query": query,
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score
            })
        
        # Aggregate scores
        avg_precision = sum(s["precision"] for s in relevance_scores) / len(relevance_scores)
        avg_recall = sum(s["recall"] for s in relevance_scores) / len(relevance_scores)
        avg_f1 = sum(s["f1_score"] for s in relevance_scores) / len(relevance_scores)
        
        return {
            "average_precision": avg_precision,
            "average_recall": avg_recall,
            "average_f1_score": avg_f1,
            "queries_evaluated": len(test_queries)
        }
    
    async def evaluate_search_latency(self, queries: List[str]) -> Dict[str, float]:
        """Evaluate search performance and latency."""
        latencies = []
        
        for query in queries:
            start_time = time.time()
            results = await self.graphiti.search_nodes(query, limit=10)
            latency = time.time() - start_time
            
            latencies.append(latency)
        
        return {
            "average_latency": sum(latencies) / len(latencies),
            "median_latency": sorted(latencies)[len(latencies) // 2],
            "max_latency": max(latencies),
            "min_latency": min(latencies),
            "queries_tested": len(queries)
        }
```

### Entity Extraction Evaluation

```python
class EntityExtractionEvaluation:
    """Evaluate entity extraction quality."""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def evaluate_entity_extraction_accuracy(self, test_texts: List[Dict]) -> Dict[str, float]:
        """Evaluate accuracy of entity extraction."""
        extraction_scores = []
        
        for text_data in test_texts:
            text = text_data["text"]
            expected_entities = text_data.get("expected_entities", [])
            
            # Add episode and extract entities
            episode = await self.graphiti.add_episode(
                name=f"Test episode",
                content=text
            )
            
            # Get extracted entities
            extracted_nodes = await self.graphiti.search_nodes(
                query="",  # Get all nodes from this episode
                limit=100
            )
            
            # Calculate extraction metrics
            precision = self.calculate_entity_precision(extracted_nodes, expected_entities)
            recall = self.calculate_entity_recall(extracted_nodes, expected_entities)
            f1_score = self.calculate_f1_score(precision, recall)
            
            extraction_scores.append({
                "text": text[:100] + "...",
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "extracted_count": len(extracted_nodes),
                "expected_count": len(expected_entities)
            })
        
        # Aggregate scores
        avg_precision = sum(s["precision"] for s in extraction_scores) / len(extraction_scores)
        avg_recall = sum(s["recall"] for s in extraction_scores) / len(extraction_scores)
        avg_f1 = sum(s["f1_score"] for s in extraction_scores) / len(extraction_scores)
        
        return {
            "extraction_precision": avg_precision,
            "extraction_recall": avg_recall,
            "extraction_f1_score": avg_f1,
            "texts_processed": len(test_texts),
            "detailed_scores": extraction_scores
        }
```

### Scalability Evaluation

```python
class ScalabilityEvaluation:
    """Evaluate system scalability and performance."""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def evaluate_episode_processing_scalability(self, episode_counts: List[int]) -> Dict[str, Any]:
        """Test scalability of episode processing."""
        scalability_results = []
        
        for count in episode_counts:
            # Generate test episodes
            episodes = [
                {
                    "name": f"Scale Test Episode {i}",
                    "content": f"This is test episode {i} for scalability testing with various entities and relationships."
                }
                for i in range(count)
            ]
            
            # Measure processing time
            start_time = time.time()
            
            # Process episodes in batch
            tasks = [
                self.graphiti.add_episode(**episode)
                for episode in episodes
            ]
            await asyncio.gather(*tasks)
            
            processing_time = time.time() - start_time
            throughput = count / processing_time
            
            scalability_results.append({
                "episode_count": count,
                "processing_time": processing_time,
                "throughput": throughput
            })
            
            # Clear graph for next test
            await self.graphiti.clear_graph()
        
        return {
            "scalability_results": scalability_results,
            "max_throughput": max(r["throughput"] for r in scalability_results),
            "average_throughput": sum(r["throughput"] for r in scalability_results) / len(scalability_results)
        }
    
    async def evaluate_search_scalability(self, node_counts: List[int]) -> Dict[str, Any]:
        """Test search performance with varying graph sizes."""
        search_results = []
        
        for count in node_counts:
            # Create test graph with specified number of nodes
            await self.create_test_graph(count)
            
            # Test search performance
            test_queries = ["test entity", "sample relationship", "graph data"]
            search_times = []
            
            for query in test_queries:
                start_time = time.time()
                results = await self.graphiti.search_nodes(query, limit=10)
                search_time = time.time() - start_time
                search_times.append(search_time)
            
            avg_search_time = sum(search_times) / len(search_times)
            
            search_results.append({
                "node_count": count,
                "average_search_time": avg_search_time,
                "search_queries": len(test_queries)
            })
            
            # Clear graph for next test
            await self.graphiti.clear_graph()
        
        return {
            "search_scalability": search_results,
            "performance_degradation": self.calculate_performance_degradation(search_results)
        }
```

### Evaluation Utilities

```python
def calculate_precision(predicted: List, actual: List) -> float:
    """Calculate precision metric."""
    if not predicted:
        return 0.0
    
    correct = len(set(predicted) & set(actual))
    return correct / len(predicted)

def calculate_recall(predicted: List, actual: List) -> float:
    """Calculate recall metric."""
    if not actual:
        return 1.0 if not predicted else 0.0
    
    correct = len(set(predicted) & set(actual))
    return correct / len(actual)

def calculate_f1_score(precision: float, recall: float) -> float:
    """Calculate F1 score."""
    if precision + recall == 0:
        return 0.0
    
    return 2 * (precision * recall) / (precision + recall)

def load_evaluation_dataset(dataset_name: str) -> List[Dict]:
    """Load evaluation dataset from file."""
    dataset_path = f"tests/evals/data/{dataset_name}.json"
    with open(dataset_path, 'r') as f:
        return json.load(f)

async def run_comprehensive_evaluation(graphiti: Graphiti) -> Dict[str, Any]:
    """Run comprehensive evaluation suite."""
    framework = EvaluationFramework(graphiti, {})
    
    # Memory evaluation
    memory_eval = MemoryEvaluation(graphiti)
    await framework.run_evaluation(
        "memory_retention",
        lambda: memory_eval.evaluate_memory_retention(load_evaluation_dataset("memory_test"))
    )
    
    # Search evaluation
    search_eval = SearchQualityEvaluation(graphiti)
    await framework.run_evaluation(
        "search_quality",
        lambda: search_eval.evaluate_search_relevance(load_evaluation_dataset("search_test"))
    )
    
    # Entity extraction evaluation
    extraction_eval = EntityExtractionEvaluation(graphiti)
    await framework.run_evaluation(
        "entity_extraction",
        lambda: extraction_eval.evaluate_entity_extraction_accuracy(load_evaluation_dataset("extraction_test"))
    )
    
    # Scalability evaluation
    scalability_eval = ScalabilityEvaluation(graphiti)
    await framework.run_evaluation(
        "scalability",
        lambda: scalability_eval.evaluate_episode_processing_scalability([10, 50, 100])
    )
    
    return framework.generate_report()
```

### Best Practices Summary

1. **Comprehensive Coverage**: Evaluate all major functionality areas
2. **Realistic Data**: Use realistic datasets and scenarios
3. **Performance Metrics**: Include both quality and performance metrics
4. **Scalability Testing**: Test with varying data sizes and loads
5. **Reproducible Results**: Ensure evaluations are deterministic and reproducible