# AGENTS.md

This file provides guidance to AI agents when working with evaluation data and datasets.

## Directory Overview

This directory contains datasets, test data, and evaluation materials used for benchmarking and testing Graphiti's performance across various scenarios and use cases.

## Data Categories

### Evaluation Datasets

1. **Memory Benchmarks**: Datasets for testing long-term memory capabilities
2. **Search Quality**: Test queries and expected results for search evaluation
3. **Entity Extraction**: Labeled datasets for entity extraction accuracy
4. **Performance Benchmarks**: Data for scalability and performance testing
5. **Domain-Specific**: Specialized datasets for different application domains

### Current Datasets

- `longmemeval_data/` - Long-term memory evaluation dataset

## Agent Guidelines

### Working with Evaluation Data

1. **Data Integrity**: Ensure data quality and consistency
2. **Reproducibility**: Use deterministic data for reproducible results
3. **Privacy**: Handle sensitive data appropriately
4. **Versioning**: Track dataset versions and changes
5. **Documentation**: Document dataset structure and usage

### Data Management Best Practices

#### Dataset Structure

```python
# Standard evaluation dataset structure
{
    "metadata": {
        "name": "dataset_name",
        "version": "1.0",
        "description": "Dataset description",
        "created_date": "2024-01-01",
        "total_samples": 1000,
        "data_source": "source description"
    },
    "data": [
        {
            "id": "sample_001",
            "input": "input data",
            "expected_output": "expected result",
            "metadata": {
                "category": "category",
                "difficulty": "medium",
                "tags": ["tag1", "tag2"]
            }
        }
    ]
}
```

#### Loading and Processing

```python
import json
from typing import List, Dict, Any
from pathlib import Path

class EvaluationDataLoader:
    """Load and manage evaluation datasets."""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
    
    def load_dataset(self, dataset_name: str) -> Dict[str, Any]:
        """Load evaluation dataset by name."""
        dataset_path = self.data_dir / f"{dataset_name}.json"
        
        if not dataset_path.exists():
            raise FileNotFoundError(f"Dataset {dataset_name} not found")
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_available_datasets(self) -> List[str]:
        """Get list of available datasets."""
        return [
            f.stem for f in self.data_dir.glob("*.json")
            if f.is_file()
        ]
    
    def validate_dataset(self, dataset: Dict[str, Any]) -> bool:
        """Validate dataset structure."""
        required_fields = ['metadata', 'data']
        
        for field in required_fields:
            if field not in dataset:
                return False
        
        # Validate metadata
        metadata = dataset['metadata']
        required_metadata = ['name', 'version', 'description']
        
        for field in required_metadata:
            if field not in metadata:
                return False
        
        # Validate data samples
        data = dataset['data']
        if not isinstance(data, list) or len(data) == 0:
            return False
        
        return True
```

### Memory Evaluation Data

#### Long-term Memory Dataset

```python
class MemoryEvaluationData:
    """Handle memory evaluation datasets."""
    
    def __init__(self, data_loader: EvaluationDataLoader):
        self.data_loader = data_loader
    
    def load_longmem_dataset(self) -> Dict[str, Any]:
        """Load long-term memory evaluation dataset."""
        return self.data_loader.load_dataset("longmemeval_data")
    
    def prepare_memory_episodes(self, dataset: Dict) -> List[Dict]:
        """Prepare episodes for memory evaluation."""
        episodes = []
        
        for sample in dataset['data']:
            episode = {
                "name": f"Memory Episode {sample['id']}",
                "content": sample['input'],
                "timestamp": sample.get('timestamp'),
                "expected_recall": sample.get('expected_output'),
                "metadata": sample.get('metadata', {})
            }
            episodes.append(episode)
        
        return episodes
    
    def create_memory_queries(self, dataset: Dict) -> List[Dict]:
        """Create memory recall queries from dataset."""
        queries = []
        
        for sample in dataset['data']:
            if 'recall_queries' in sample:
                for query in sample['recall_queries']:
                    queries.append({
                        "query": query['text'],
                        "episode_id": sample['id'],
                        "expected_entities": query.get('expected_entities', []),
                        "expected_relationships": query.get('expected_relationships', [])
                    })
        
        return queries
```

### Search Quality Data

```python
class SearchEvaluationData:
    """Handle search quality evaluation datasets."""
    
    def load_search_queries(self) -> List[Dict]:
        """Load search quality test queries."""
        dataset = self.data_loader.load_dataset("search_quality")
        
        queries = []
        for sample in dataset['data']:
            query = {
                "query_text": sample['query'],
                "expected_entities": sample.get('expected_entities', []),
                "expected_relationships": sample.get('expected_relationships', []),
                "relevance_threshold": sample.get('relevance_threshold', 0.8),
                "category": sample.get('metadata', {}).get('category', 'general')
            }
            queries.append(query)
        
        return queries
    
    def create_relevance_judgments(self, queries: List[Dict]) -> Dict:
        """Create relevance judgments for search evaluation."""
        judgments = {}
        
        for query in queries:
            query_id = query['query_text']
            judgments[query_id] = {
                "relevant_entities": query['expected_entities'],
                "relevant_relationships": query['expected_relationships'],
                "threshold": query['relevance_threshold']
            }
        
        return judgments
```

### Entity Extraction Data

```python
class EntityExtractionData:
    """Handle entity extraction evaluation datasets."""
    
    def load_extraction_samples(self) -> List[Dict]:
        """Load entity extraction test samples."""
        dataset = self.data_loader.load_dataset("entity_extraction")
        
        samples = []
        for sample in dataset['data']:
            extraction_sample = {
                "text": sample['input'],
                "expected_entities": sample['expected_entities'],
                "expected_relationships": sample.get('expected_relationships', []),
                "domain": sample.get('metadata', {}).get('domain', 'general'),
                "difficulty": sample.get('metadata', {}).get('difficulty', 'medium')
            }
            samples.append(extraction_sample)
        
        return samples
    
    def validate_entity_annotations(self, sample: Dict) -> bool:
        """Validate entity annotation format."""
        required_fields = ['text', 'expected_entities']
        
        for field in required_fields:
            if field not in sample:
                return False
        
        # Validate entity format
        for entity in sample['expected_entities']:
            entity_fields = ['name', 'type', 'start_pos', 'end_pos']
            for field in entity_fields:
                if field not in entity:
                    return False
        
        return True
```

### Performance Benchmarks

```python
class PerformanceBenchmarkData:
    """Handle performance benchmark datasets."""
    
    def generate_scalability_data(self, sizes: List[int]) -> Dict[int, List[Dict]]:
        """Generate data for scalability testing."""
        scalability_data = {}
        
        for size in sizes:
            episodes = []
            for i in range(size):
                episode = {
                    "name": f"Scalability Episode {i}",
                    "content": self.generate_sample_content(i),
                    "timestamp": self.generate_timestamp(i),
                    "metadata": {"test_size": size, "episode_index": i}
                }
                episodes.append(episode)
            
            scalability_data[size] = episodes
        
        return scalability_data
    
    def generate_sample_content(self, index: int) -> str:
        """Generate sample content for testing."""
        templates = [
            "Person {index} works at Company {company} on Project {project}.",
            "Research by Scientist {index} shows correlation between Factor A and Factor B.",
            "Meeting on {date} discussed Strategy {index} with Team {team}.",
            "Product {index} launched by Organization {org} in Market {market}."
        ]
        
        template = templates[index % len(templates)]
        return template.format(
            index=index,
            company=f"Company_{index % 10}",
            project=f"Project_{index % 5}",
            date=f"2024-{(index % 12) + 1:02d}-01",
            team=f"Team_{index % 3}",
            org=f"Org_{index % 8}",
            market=f"Market_{index % 4}"
        )
    
    def generate_timestamp(self, index: int) -> str:
        """Generate timestamp for testing."""
        from datetime import datetime, timedelta
        
        base_date = datetime(2024, 1, 1)
        offset = timedelta(hours=index)
        return (base_date + offset).isoformat()
```

### Data Quality Assurance

```python
class DataQualityChecker:
    """Check and validate evaluation data quality."""
    
    def __init__(self):
        self.quality_rules = self.define_quality_rules()
    
    def define_quality_rules(self) -> Dict:
        """Define data quality rules."""
        return {
            "text_length": {"min": 10, "max": 10000},
            "entity_overlap": {"max_percentage": 0.8},
            "required_fields": ["id", "input"],
            "encoding": "utf-8"
        }
    
    def check_dataset_quality(self, dataset: Dict) -> Dict:
        """Comprehensive data quality check."""
        quality_report = {
            "total_samples": len(dataset.get('data', [])),
            "errors": [],
            "warnings": [],
            "quality_score": 0.0
        }
        
        for sample in dataset.get('data', []):
            # Check required fields
            self.check_required_fields(sample, quality_report)
            
            # Check text quality
            self.check_text_quality(sample, quality_report)
            
            # Check annotation quality
            self.check_annotation_quality(sample, quality_report)
        
        # Calculate quality score
        total_checks = quality_report["total_samples"] * 3
        error_count = len(quality_report["errors"])
        quality_report["quality_score"] = max(0, (total_checks - error_count) / total_checks)
        
        return quality_report
    
    def check_required_fields(self, sample: Dict, report: Dict) -> None:
        """Check if sample has required fields."""
        for field in self.quality_rules["required_fields"]:
            if field not in sample:
                report["errors"].append(f"Missing required field: {field}")
    
    def check_text_quality(self, sample: Dict, report: Dict) -> None:
        """Check text quality."""
        if 'input' in sample:
            text = sample['input']
            length = len(text)
            
            if length < self.quality_rules["text_length"]["min"]:
                report["warnings"].append(f"Text too short: {length} chars")
            elif length > self.quality_rules["text_length"]["max"]:
                report["warnings"].append(f"Text too long: {length} chars")
    
    def check_annotation_quality(self, sample: Dict, report: Dict) -> None:
        """Check annotation quality."""
        if 'expected_entities' in sample:
            entities = sample['expected_entities']
            
            # Check for overlapping entities
            overlaps = self.find_entity_overlaps(entities)
            if overlaps:
                report["warnings"].append(f"Overlapping entities: {overlaps}")
    
    def find_entity_overlaps(self, entities: List[Dict]) -> List[Dict]:
        """Find overlapping entity annotations."""
        overlaps = []
        
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities[i+1:], i+1):
                if self.entities_overlap(entity1, entity2):
                    overlaps.append({"entity1": entity1, "entity2": entity2})
        
        return overlaps
    
    def entities_overlap(self, entity1: Dict, entity2: Dict) -> bool:
        """Check if two entities overlap."""
        start1, end1 = entity1.get('start_pos', 0), entity1.get('end_pos', 0)
        start2, end2 = entity2.get('start_pos', 0), entity2.get('end_pos', 0)
        
        return not (end1 <= start2 or end2 <= start1)
```

### Data Usage Examples

```python
# Example: Using evaluation data in tests
async def run_memory_evaluation():
    """Run memory evaluation using test data."""
    loader = EvaluationDataLoader("tests/evals/data")
    memory_data = MemoryEvaluationData(loader)
    
    # Load dataset
    dataset = memory_data.load_longmem_dataset()
    
    # Prepare episodes
    episodes = memory_data.prepare_memory_episodes(dataset)
    
    # Add episodes to Graphiti
    for episode in episodes:
        await graphiti.add_episode(**episode)
    
    # Create and run recall queries
    queries = memory_data.create_memory_queries(dataset)
    
    results = []
    for query in queries:
        search_results = await graphiti.search_nodes(query['query'])
        results.append({
            "query": query,
            "results": search_results,
            "success": evaluate_recall_success(query, search_results)
        })
    
    return results
```

### Best Practices Summary

1. **Data Quality**: Maintain high-quality, well-annotated evaluation datasets
2. **Versioning**: Track dataset versions and document changes
3. **Reproducibility**: Ensure datasets enable reproducible evaluation results
4. **Coverage**: Include diverse scenarios and edge cases in evaluation data
5. **Documentation**: Thoroughly document dataset structure, usage, and provenance