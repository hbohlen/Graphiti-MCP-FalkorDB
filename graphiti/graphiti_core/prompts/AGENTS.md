# AGENTS.md

This file provides guidance to AI agents when working with prompt components.

## Directory Overview

This directory contains LLM prompts and prompt management functionality for various knowledge graph operations including entity extraction, deduplication, summarization, and validation.

## Files

- `lib.py` - Core prompt library and management functions
- `models.py` - Data models for prompt inputs and outputs
- `prompt_helpers.py` - Helper functions for prompt processing
- `extract_nodes.py` - Prompts for extracting entities from text
- `extract_edges.py` - Prompts for extracting relationships from text
- `extract_edge_dates.py` - Prompts for extracting temporal information from relationships
- `dedupe_nodes.py` - Prompts for entity deduplication
- `dedupe_edges.py` - Prompts for relationship deduplication
- `summarize_nodes.py` - Prompts for entity summarization
- `invalidate_edges.py` - Prompts for relationship validation and invalidation
- `eval.py` - Prompts for evaluation and quality assessment

## Prompt Architecture

### Prompt Categories

1. **Extraction Prompts**: Extract entities and relationships from text
2. **Deduplication Prompts**: Identify and merge duplicate entities/relationships
3. **Summarization Prompts**: Generate summaries and descriptions
4. **Validation Prompts**: Validate and invalidate entities/relationships
5. **Evaluation Prompts**: Assess quality and relevance

### Structured Output

All prompts are designed to work with LLM structured output capabilities:

- Defined Pydantic models for consistent outputs
- Schema validation for reliability
- Error handling for malformed responses
- Type safety throughout the pipeline

## Agent Guidelines

### Working with Prompts

1. **Consistency**: Use provided prompts for consistent results across operations
2. **Customization**: Extend prompts for domain-specific needs
3. **Validation**: Always validate LLM outputs against expected schemas
4. **Error Handling**: Handle cases where LLMs don't follow instructions
5. **Performance**: Monitor prompt performance and adjust as needed

### Entity Extraction

```python
from graphiti_core.prompts.extract_nodes import extract_nodes_prompt

# Extract entities from text
entities = await llm_client.generate_response(
    prompt=extract_nodes_prompt,
    text_content="Your text content here",
    existing_entities=current_entities
)
```

### Relationship Extraction

```python
from graphiti_core.prompts.extract_edges import extract_edges_prompt

# Extract relationships from text
relationships = await llm_client.generate_response(
    prompt=extract_edges_prompt,
    text_content="Your text content here",
    source_nodes=entities
)
```

### Best Practices for Agents

1. **Context Provision**: Provide sufficient context for accurate extraction
2. **Entity Consistency**: Maintain consistent entity representations
3. **Temporal Accuracy**: Ensure temporal information is correctly extracted
4. **Quality Control**: Validate extracted information against source material
5. **Performance Monitoring**: Track extraction quality and adjust prompts

### Prompt Engineering Guidelines

#### Entity Extraction
- **Specificity**: Be specific about entity types and attributes
- **Context**: Provide relevant context for disambiguation
- **Examples**: Include examples for consistent formatting
- **Constraints**: Define clear constraints and requirements

#### Relationship Extraction
- **Relationship Types**: Define clear relationship taxonomies
- **Temporal Information**: Extract when relationships occurred
- **Confidence**: Include confidence scores for relationships
- **Bidirectionality**: Handle bidirectional relationships appropriately

#### Deduplication
- **Similarity Criteria**: Define clear criteria for entity similarity
- **Merge Rules**: Specify how to merge duplicate entities
- **Preservation**: Ensure important information is preserved
- **Confidence**: Include confidence scores for deduplication decisions

### Quality Assurance

1. **Output Validation**: Validate all LLM outputs against schemas
2. **Consistency Checks**: Ensure consistency across related operations
3. **Edge Case Handling**: Handle unusual or edge case inputs
4. **Performance Monitoring**: Track and improve prompt performance
5. **Human Review**: Implement human review for critical decisions

### Common Prompt Patterns

#### Extraction Pattern
```python
# Standard extraction workflow
1. Provide text content and context
2. Specify entity/relationship types to extract
3. Include existing entities for reference
4. Generate structured output
5. Validate and process results
```

#### Deduplication Pattern
```python
# Standard deduplication workflow
1. Provide candidate entities/relationships
2. Define similarity criteria
3. Request merge recommendations
4. Validate merge decisions
5. Apply deduplication actions
```

#### Summarization Pattern
```python
# Standard summarization workflow
1. Provide entity/relationship data
2. Specify summary requirements
3. Request structured summary
4. Validate summary quality
5. Store summary information
```

### Customization Guidelines

1. **Domain Adaptation**: Adapt prompts for specific domains
2. **Language Support**: Modify prompts for different languages
3. **Entity Types**: Extend prompts for custom entity types
4. **Business Rules**: Incorporate business-specific rules
5. **Quality Requirements**: Adjust for different quality standards

### Performance Optimization

1. **Prompt Length**: Optimize prompt length for efficiency
2. **Context Management**: Provide relevant context without overloading
3. **Batch Processing**: Design prompts for batch operations when possible
4. **Caching**: Cache prompt results for repeated operations
5. **Model Selection**: Choose appropriate models for different prompt types

### Error Handling

```python
from graphiti_core.prompts.errors import PromptError

try:
    result = await llm_client.generate_response(prompt, **kwargs)
    validate_output(result)
except PromptError as e:
    # Handle prompt-specific errors
    logger.error(f"Prompt error: {e}")
    # Implement fallback or retry logic
```

### Integration with Graphiti

Prompts are integrated throughout Graphiti's workflow:

1. **Episode Processing**: Extract entities and relationships from episodes
2. **Graph Maintenance**: Deduplicate and clean graph data
3. **Search Enhancement**: Improve search results through summarization
4. **Quality Assurance**: Validate and improve data quality
5. **User Interface**: Generate human-readable descriptions

### Extension Points

- **Custom Prompts**: Create domain-specific prompts
- **Prompt Optimization**: Optimize prompts for specific models
- **Multilingual Support**: Add support for multiple languages
- **Quality Metrics**: Implement custom quality assessment
- **Prompt Versioning**: Version control for prompt evolution