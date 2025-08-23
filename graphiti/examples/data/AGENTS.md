# AGENTS.md

This file provides guidance to AI agents when working with the data directory.

## Directory Overview

This directory contains sample data files and datasets used by various Graphiti examples. It serves as a repository for test data, reference materials, and example datasets.

## Files

- `manybirds_products.json` - Sample product catalog data for e-commerce examples

## Data Purpose

This directory provides:

1. **Example Datasets**: Real-world-like data for testing and demonstration
2. **Reference Data**: Standard formats and structures for different domains
3. **Test Materials**: Data used in example applications and tutorials
4. **Sample Formats**: Examples of how to structure data for Graphiti ingestion

## Agent Guidelines

### Working with Data Files

1. **Data Formats**: Understand the structure and format of provided datasets
2. **Example Usage**: See how data is used in corresponding example applications
3. **Data Validation**: Ensure data integrity before ingestion into Graphiti
4. **Format Consistency**: Maintain consistent data structures across examples

### Data Types

The data directory may contain:

- **JSON Files**: Structured data for products, entities, relationships
- **Text Files**: Unstructured content for text analysis examples
- **CSV Files**: Tabular data for business intelligence applications
- **Configuration Files**: Example configurations and settings

### Best Practices for Agents

1. **Data Inspection**: Always examine data structure before processing
2. **Error Handling**: Handle malformed or missing data gracefully
3. **Data Cleaning**: Prepare data for optimal Graphiti ingestion
4. **Format Validation**: Ensure data meets expected schema requirements
5. **Documentation**: Understand the context and source of each dataset

### Sample Data Usage

```python
# Example: Loading product data
import json

with open('manybirds_products.json', 'r') as f:
    products = json.load(f)

# Process products for Graphiti ingestion
for product in products:
    # Extract entities and relationships
    # Create episodes from product data
    # Build knowledge graph
```

### Data Integration Patterns

- **Batch Processing**: Loading entire datasets at once
- **Incremental Updates**: Adding new data to existing graphs
- **Data Transformation**: Converting external formats to Graphiti-compatible structures
- **Quality Assurance**: Validating data before and after ingestion

### Common Data Scenarios

1. **Product Catalogs**: E-commerce product information and hierarchies
2. **Content Libraries**: Text, audio, video content with metadata
3. **User Generated Content**: Reviews, comments, social interactions
4. **Temporal Data**: Time-series information and event sequences
5. **Relationship Data**: Entity connections and association strength

### Data Preparation Guidelines

- **Clean Data**: Remove inconsistencies and duplicate entries
- **Standardize Formats**: Consistent date formats, naming conventions
- **Enrich Metadata**: Add context and descriptive information
- **Validate Relationships**: Ensure entity relationships are meaningful
- **Optimize Structure**: Organize data for efficient graph operations