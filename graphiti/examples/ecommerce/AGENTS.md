# AGENTS.md

This file provides guidance to AI agents when working with the e-commerce example.

## Directory Overview

This directory contains an e-commerce specific implementation demonstrating how to use Graphiti for tracking customer behavior, product relationships, and business intelligence in retail/commerce applications.

## Files

- `runner.py` - Python script implementation of the e-commerce example
- `runner.ipynb` - Jupyter notebook version with interactive exploration

## Example Features

This example demonstrates:

1. **Customer Behavior Tracking**: Modeling customer interactions and purchase patterns
2. **Product Relationships**: Building product catalogs with hierarchical and associative relationships
3. **Business Intelligence**: Extracting insights from customer and product data
4. **Recommendation Systems**: Using graph relationships for product recommendations
5. **Temporal Commerce Data**: Tracking changes in customer preferences and product availability over time

## Prerequisites

- Python 3.9+
- OpenAI API key for LLM operations
- Neo4j or FalkorDB database
- Jupyter environment (for notebook version)

## Agent Guidelines

### Environment Setup

```bash
# Required for LLM operations
export OPENAI_API_KEY=your_openai_api_key

# Database configuration (Neo4j)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password

# Alternative: Database configuration (FalkorDB)
export FALKORDB_HOST=localhost
export FALKORDB_PORT=6379
export FALKORDB_USERNAME=your_username  # optional
export FALKORDB_PASSWORD=your_password  # optional
export DATABASE_TYPE=falkordb
```

### Running the Example

```bash
# Script version
python runner.py

# Notebook version
jupyter notebook runner.ipynb
```

### Key E-commerce Concepts

1. **Customer Entities**: Representing customers, their preferences, and behavior patterns
2. **Product Catalog**: Hierarchical product organization with categories and attributes
3. **Transaction Modeling**: Purchase events, order history, and payment patterns
4. **Inventory Management**: Product availability and stock level tracking
5. **Customer Journey**: Mapping customer interactions across touchpoints

### Graph Modeling Patterns

- **Customer-Product Relationships**: Purchase history, wishlists, reviews
- **Product Hierarchies**: Categories, subcategories, product variants
- **Behavioral Patterns**: Browsing patterns, seasonal preferences, loyalty indicators
- **Recommendation Graphs**: Similar products, frequently bought together, collaborative filtering

### Business Use Cases

1. **Personalized Recommendations**: Using graph relationships for product suggestions
2. **Customer Segmentation**: Identifying customer groups based on behavior patterns
3. **Inventory Optimization**: Understanding product demand and relationships
4. **Marketing Campaigns**: Targeting based on customer preferences and history
5. **Customer Support**: Access to complete customer context and history

### Best Practices for Agents

1. **Privacy Considerations**: Handle customer data with appropriate privacy measures
2. **Data Quality**: Ensure accurate product and customer information
3. **Real-time Updates**: Keep inventory and customer data current
4. **Performance Optimization**: Efficient queries for large-scale e-commerce data
5. **Relationship Modeling**: Accurately represent business relationships

### Common E-commerce Patterns

- **Customer Lifecycle**: From prospect to loyal customer
- **Product Discovery**: How customers find and evaluate products
- **Purchase Decision**: Factors influencing buying decisions
- **Post-Purchase**: Returns, reviews, and repeat purchases
- **Cross-selling/Upselling**: Leveraging relationship data for sales opportunities

### Integration Considerations

- **ERP Systems**: Integrating with existing enterprise resource planning
- **CRM Platforms**: Customer relationship management data synchronization
- **Analytics Tools**: Business intelligence and reporting integration
- **Marketing Automation**: Campaign management and customer targeting
- **Real-time Personalization**: Dynamic content and recommendation delivery