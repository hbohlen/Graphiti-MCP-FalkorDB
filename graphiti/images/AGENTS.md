# AGENTS.md

This file provides guidance to AI agents when working with image assets and visual documentation.

## Directory Overview

This directory contains visual assets, diagrams, screenshots, and other image files used in documentation, presentations, and project materials.

## Asset Categories

### Documentation Images

Visual assets for documentation and README files:

1. **Screenshots**: Application and interface screenshots
2. **Diagrams**: Architecture and flow diagrams  
3. **Animations**: GIFs demonstrating functionality
4. **Charts**: Performance charts and visualizations
5. **Logos**: Brand assets and logos

### Current Assets

- `arxiv-screenshot.png` - Screenshot for research/academic documentation
- `graphiti-graph-intro.gif` - Animated introduction to graph concepts
- `graphiti-intro-slides-stock-2.gif` - Presentation slide animations
- `simple_graph.svg` - Simple graph visualization diagram

## Agent Guidelines

### Image Management

1. **Optimization**: Ensure images are optimized for web use
2. **Formats**: Use appropriate formats (PNG for screenshots, SVG for diagrams, GIF for animations)
3. **Naming**: Use descriptive, consistent naming conventions
4. **Size**: Keep file sizes reasonable for fast loading
5. **Alt Text**: Provide descriptive alt text when using images

### Usage Patterns

#### In Documentation

```markdown
# Using images in README or documentation
![Graphiti Graph Introduction](images/graphiti-graph-intro.gif)

# With alt text and sizing
<img src="images/simple_graph.svg" alt="Simple graph showing nodes and edges" width="500">

# Referenced diagrams
See the [architecture diagram](images/architecture-diagram.png) for system overview.
```

#### In Presentations

Images in this directory are used for:

1. **Project Presentations**: Slide assets and animations
2. **Demo Materials**: Screenshots and workflow demonstrations
3. **Educational Content**: Explanatory diagrams and visualizations
4. **Marketing Materials**: Visual assets for project promotion

### Best Practices for Agents

1. **Image Optimization**: Compress images appropriately
2. **Accessibility**: Always include descriptive alt text
3. **Responsive Design**: Consider how images appear on different screen sizes
4. **Version Control**: Avoid committing unnecessarily large image files
5. **Documentation**: Reference images clearly in documentation

### Image Creation Guidelines

#### Screenshots

```bash
# Taking effective screenshots
- Use consistent browser/application settings
- Ensure high resolution for clarity
- Crop to relevant content
- Annotate when necessary
```

#### Diagrams

```bash
# Creating effective diagrams
- Use consistent styling and colors
- Include clear labels and legends
- Export as SVG when possible for scalability
- Keep complexity manageable
```

#### Animations

```bash
# Creating effective GIFs
- Keep file size under 5MB when possible
- Use appropriate frame rate (8-15 fps)
- Loop smoothly when applicable
- Focus on demonstrating key concepts
```

### Asset Organization

#### Naming Conventions

```
- Screenshots: feature-name-screenshot.png
- Diagrams: component-architecture.svg
- Animations: workflow-demo.gif
- Charts: performance-comparison.png
```

#### Directory Structure

```
images/
├── screenshots/          # Application screenshots
├── diagrams/            # Architecture and flow diagrams
├── animations/          # GIF demonstrations
├── charts/              # Performance and analytics charts
└── logos/               # Brand assets
```

### Integration with Documentation

#### README Integration

```markdown
# Graphiti Overview

![Graphiti Introduction](images/graphiti-intro-slides-stock-2.gif)

Graphiti enables real-time knowledge graph construction...

## Architecture

The system architecture follows a modular design:

![Simple Graph](images/simple_graph.svg)

## Research Background

Our approach is documented in academic literature:

![Research Screenshot](images/arxiv-screenshot.png)
```

#### API Documentation

```markdown
# Visual API Guide

## Graph Structure Visualization

![Graph Structure](images/simple_graph.svg)

The graph consists of:
- **Nodes**: Represent entities
- **Edges**: Represent relationships
- **Properties**: Metadata on nodes and edges
```

### Image Processing

#### Optimization Tools

```bash
# Optimize PNG images
pngquant --quality 80-90 input.png --output output.png

# Optimize JPEG images  
jpegoptim --max=85 input.jpg

# Optimize SVG images
svgo input.svg -o output.svg

# Convert images
convert input.png -resize 800x600 output.png
```

#### Batch Processing

```bash
# Optimize all PNG images in directory
find images/ -name "*.png" -exec pngquant --quality 80-90 {} --output {} \;

# Resize all images to max width 1200px
find images/ -name "*.png" -exec convert {} -resize 1200x\> {} \;
```

### Documentation Assets

#### Workflow Diagrams

Create diagrams showing:

1. **Data Flow**: How data moves through the system
2. **User Workflows**: Step-by-step user interactions
3. **System Architecture**: Component relationships
4. **Process Flows**: Business process visualizations

#### Example Diagram Creation

```python
# Using matplotlib to create charts
import matplotlib.pyplot as plt

def create_performance_chart():
    # Performance data
    categories = ['Ingestion', 'Search', 'Retrieval']
    times = [0.5, 0.8, 0.3]
    
    plt.figure(figsize=(10, 6))
    plt.bar(categories, times, color=['blue', 'green', 'orange'])
    plt.title('Performance Metrics')
    plt.ylabel('Time (seconds)')
    plt.savefig('images/performance-chart.png', dpi=300, bbox_inches='tight')
    plt.close()

# Using graphviz for graph diagrams
import graphviz

def create_graph_diagram():
    dot = graphviz.Digraph()
    dot.node('A', 'Person')
    dot.node('B', 'Organization')
    dot.edge('A', 'B', 'works_for')
    dot.render('images/simple_graph', format='svg', cleanup=True)
```

### Animation Creation

#### Creating Demo GIFs

```bash
# Using ffmpeg to create GIFs from screen recordings
ffmpeg -i screen_recording.mov -vf "fps=10,scale=800:-1:flags=lanczos" output.gif

# Using gifsicle to optimize GIFs
gifsicle --optimize=3 --resize-width 800 input.gif -o output.gif
```

#### Animation Best Practices

1. **Duration**: Keep animations 3-10 seconds
2. **Loop**: Ensure smooth looping
3. **Focus**: Highlight key interactions
4. **Size**: Optimize for web delivery
5. **Accessibility**: Provide static alternatives

### Version Control

#### Git LFS for Large Files

```bash
# Track large image files with Git LFS
git lfs track "*.gif"
git lfs track "*.png"
git lfs track "*.jpg"

# Add .gitattributes
echo "*.gif filter=lfs diff=lfs merge=lfs -text" >> .gitattributes
```

#### Ignore Patterns

```gitignore
# Ignore working files
images/tmp/
images/src/
*.psd
*.ai
*.sketch
```

### Accessibility Considerations

#### Alt Text Guidelines

```html
<!-- Good alt text -->
<img src="images/graphiti-graph-intro.gif" 
     alt="Animation showing how nodes and edges are created in Graphiti knowledge graph">

<!-- Screen reader friendly -->
<img src="images/architecture-diagram.svg" 
     alt="System architecture diagram showing data flow from input through processing to storage">
```

#### Image Descriptions

For complex images, provide detailed descriptions:

```markdown
![Complex Diagram](images/complex-flow.png)

*Figure 1: The diagram shows the complete data processing pipeline with five main stages: 
(1) Data ingestion from multiple sources, (2) Entity extraction using LLMs, 
(3) Relationship discovery, (4) Graph storage, and (5) Search and retrieval.*
```

### Best Practices Summary

1. **Optimization**: Optimize all images for web use and version control
2. **Consistency**: Use consistent styling and naming conventions
3. **Accessibility**: Always provide alt text and descriptions
4. **Documentation**: Integrate images meaningfully into documentation
5. **Maintenance**: Regularly review and update visual assets