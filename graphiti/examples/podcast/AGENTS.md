# AGENTS.md

This file provides guidance to AI agents when working with the podcast example.

## Directory Overview

This directory demonstrates how to use Graphiti for podcast content management, including transcript processing, content relationship modeling, and temporal content organization.

## Files

- `podcast_runner.py` - Main script for processing podcast content
- `transcript_parser.py` - Utility for parsing and processing podcast transcripts
- `podcast_transcript.txt` - Sample podcast transcript data

## Example Features

This example shows how to:

1. **Content Processing**: Parse and process podcast transcripts and metadata
2. **Temporal Modeling**: Track podcast episodes, series, and temporal relationships
3. **Speaker Recognition**: Identify and track different speakers across episodes
4. **Topic Extraction**: Extract themes, topics, and key concepts from audio content
5. **Content Relationships**: Build relationships between episodes, topics, and speakers

## Prerequisites

- Python 3.9+
- OpenAI API key for content processing
- Neo4j or FalkorDB database
- Podcast transcript data

## Agent Guidelines

### Environment Setup

```bash
# Required for content processing
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
# Process podcast content
python podcast_runner.py

# Parse transcript separately
python transcript_parser.py
```

### Key Podcast Concepts

1. **Episode Structure**: Individual episodes with metadata (title, date, duration, description)
2. **Series/Show Organization**: Podcast series with consistent hosts and themes
3. **Speaker Identification**: Tracking hosts, guests, and their contributions
4. **Content Segmentation**: Breaking episodes into topics, segments, or chapters
5. **Temporal Relationships**: Episode sequences, recurring themes, guest appearances

### Content Modeling Patterns

- **Hierarchical Structure**: Show → Season → Episode → Segment
- **Speaker Networks**: Host-guest relationships, recurring participants
- **Topic Evolution**: How themes develop across episodes and time
- **Content References**: Citations, mentions, and cross-references
- **Audience Engagement**: Comments, feedback, and community discussions

### Use Cases

1. **Content Discovery**: Help users find relevant episodes based on interests
2. **Show Analytics**: Understand content patterns and audience preferences
3. **Guest Management**: Track guest appearances and expertise areas
4. **Content Planning**: Identify gaps and opportunities for new content
5. **Automated Summaries**: Generate episode summaries and highlights

### Processing Patterns

1. **Transcript Analysis**: Extract meaningful content from spoken word
2. **Speaker Diarization**: Identify who said what and when
3. **Topic Modeling**: Identify main themes and subject matter
4. **Entity Extraction**: People, places, organizations mentioned
5. **Sentiment Analysis**: Understand tone and emotional content

### Best Practices for Agents

1. **Audio Quality**: Handle varying transcript quality and accuracy
2. **Speaker Consistency**: Maintain consistent speaker identification across episodes
3. **Content Chunking**: Break long episodes into manageable segments
4. **Metadata Enrichment**: Add context and structure to raw transcript data
5. **Timeline Accuracy**: Maintain accurate temporal relationships

### Integration Opportunities

- **Podcast Platforms**: RSS feeds, Apple Podcasts, Spotify integration
- **Transcription Services**: Automated transcript generation
- **Content Management**: Integration with CMS and publishing workflows
- **Analytics Platforms**: Podcast analytics and audience insights
- **Search Systems**: Enhanced podcast search and discovery

### Advanced Features

- **Cross-Episode Analysis**: Finding connections across entire podcast libraries
- **Guest Recommendation**: Suggesting guests based on content and network analysis
- **Content Gaps**: Identifying topics that haven't been covered
- **Audience Insights**: Understanding listener preferences and behavior
- **Automated Curation**: Creating thematic playlists and content collections