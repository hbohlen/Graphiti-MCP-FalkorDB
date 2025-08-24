# AGENTS.md

This file provides guidance to AI agents when working with the Wizard of Oz example.

## Directory Overview

This directory contains a domain-specific example using "The Wonderful Wizard of Oz" story to demonstrate custom entity types, relationship modeling, and narrative structure analysis using Graphiti.

## Files

- `runner.py` - Main script for processing the Wizard of Oz text
- `parser.py` - Text parsing utilities for narrative content
- `woo.txt` - The Wonderful Wizard of Oz text content

## Example Features

This example demonstrates:

1. **Narrative Analysis**: Processing literary text and extracting story elements
2. **Character Modeling**: Tracking characters, their relationships, and development
3. **Plot Structure**: Modeling story progression, events, and narrative arcs
4. **Custom Entities**: Domain-specific entity types for literary analysis
5. **Temporal Storytelling**: Tracking story timeline and event sequences

## Prerequisites

- Python 3.9+
- OpenAI API key for text processing
- Neo4j or FalkorDB database
- Text content to analyze

## Agent Guidelines

### Environment Setup

```bash
# Required for text analysis
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
# Process the Wizard of Oz text
python runner.py

# Use parser utilities
python parser.py
```

### Literary Analysis Concepts

1. **Character Entities**: Main characters (Dorothy, Scarecrow, Tin Man, Lion, Wizard)
2. **Location Mapping**: Kansas, Oz, Yellow Brick Road, Emerald City
3. **Plot Events**: Key story moments and turning points
4. **Relationships**: Character interactions and relationship development
5. **Themes**: Courage, wisdom, heart, home - abstract concept tracking

### Narrative Modeling Patterns

- **Character Development**: How characters change throughout the story
- **Journey Structure**: Physical and emotional journey mapping
- **Conflict Resolution**: Problems introduced and how they're resolved
- **Symbolic Elements**: Ruby slippers, yellow brick road, wizard's curtain
- **Moral Lessons**: Life lessons and character growth

### Use Cases

1. **Literary Analysis**: Academic study of narrative structure and themes
2. **Content Understanding**: Deep comprehension of story elements
3. **Educational Tools**: Teaching narrative analysis and story structure
4. **Creative Writing**: Understanding successful storytelling patterns
5. **Content Adaptation**: Analyzing source material for adaptations

### Text Processing Patterns

1. **Chapter Segmentation**: Breaking story into logical sections
2. **Character Recognition**: Identifying when characters appear and interact
3. **Event Extraction**: Key plot points and story developments
4. **Dialogue Analysis**: Character voice and communication patterns
5. **Descriptive Content**: Setting, atmosphere, and world-building elements

### Custom Entity Types

- **Characters**: Protagonists, antagonists, supporting characters
- **Locations**: Physical places and their significance
- **Objects**: Important items (ruby slippers, wizard's gifts)
- **Events**: Plot points, conflicts, resolutions
- **Themes**: Abstract concepts and moral lessons

### Best Practices for Agents

1. **Context Preservation**: Maintain story context across different sections
2. **Character Consistency**: Track character traits and development accurately
3. **Temporal Accuracy**: Maintain correct sequence of events
4. **Relationship Complexity**: Handle complex character relationships
5. **Thematic Analysis**: Extract both explicit and implicit themes

### Domain-Specific Considerations

- **Literary Conventions**: Understanding narrative techniques and structures
- **Cultural Context**: Historical and cultural background of the story
- **Symbolic Interpretation**: Recognizing metaphors and symbolic elements
- **Genre Characteristics**: Fantasy elements and their significance
- **Audience Analysis**: Understanding intended audience and messages

### Advanced Applications

- **Comparative Analysis**: Comparing different versions or adaptations
- **Cross-Reference Analysis**: Finding similar themes in other works
- **Character Archetype**: Identifying universal character types
- **Narrative Patterns**: Recognizing common storytelling structures
- **Educational Content**: Generating study guides and analysis materials