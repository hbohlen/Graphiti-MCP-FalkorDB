# AGENTS.md

This file provides guidance to AI agents when working with graph maintenance operations.

## Directory Overview

This directory contains specialized utilities for maintaining and optimizing Graphiti knowledge graphs, including operations on nodes, edges, communities, temporal data, and overall graph integrity.

## Files

- `utils.py` - General maintenance utility functions
- `node_operations.py` - Node-specific maintenance operations
- `edge_operations.py` - Edge/relationship maintenance operations
- `community_operations.py` - Community detection and management
- `temporal_operations.py` - Temporal data maintenance and cleanup
- `graph_data_operations.py` - Overall graph data operations and integrity

## Maintenance Categories

### Node Operations (`node_operations.py`)

Provides utilities for node maintenance:

1. **Node Cleanup**: Remove orphaned or invalid nodes
2. **Node Merging**: Merge duplicate or similar nodes
3. **Node Validation**: Validate node data integrity
4. **Node Optimization**: Optimize node storage and access
5. **Node Statistics**: Generate node-related statistics

### Edge Operations (`edge_operations.py`)

Handles relationship maintenance:

1. **Edge Cleanup**: Remove invalid or orphaned edges
2. **Edge Validation**: Validate relationship integrity
3. **Edge Optimization**: Optimize relationship storage
4. **Edge Statistics**: Generate relationship statistics
5. **Edge Deduplication**: Remove duplicate relationships

### Community Operations (`community_operations.py`)

Manages entity communities and clusters:

1. **Community Detection**: Identify entity communities
2. **Community Analysis**: Analyze community structures
3. **Community Optimization**: Optimize community representations
4. **Community Validation**: Validate community integrity
5. **Community Statistics**: Generate community metrics

### Temporal Operations (`temporal_operations.py`)

Handles time-related maintenance:

1. **Temporal Cleanup**: Remove outdated temporal data
2. **Temporal Validation**: Validate temporal consistency
3. **Temporal Optimization**: Optimize temporal queries
4. **Temporal Analysis**: Analyze temporal patterns
5. **Temporal Archiving**: Archive old temporal data

### Graph Data Operations (`graph_data_operations.py`)

Overall graph maintenance:

1. **Graph Integrity**: Validate overall graph integrity
2. **Graph Optimization**: Optimize graph performance
3. **Graph Statistics**: Generate comprehensive graph metrics
4. **Graph Backup**: Backup and restore operations
5. **Graph Migration**: Migrate graph data between systems

## Agent Guidelines

### Routine Maintenance

```python
from graphiti_core.utils.maintenance import (
    NodeOperations,
    EdgeOperations,
    GraphDataOperations
)

# Initialize maintenance operations
node_ops = NodeOperations(graphiti)
edge_ops = EdgeOperations(graphiti)
graph_ops = GraphDataOperations(graphiti)

# Perform routine maintenance
await node_ops.cleanup_orphaned_nodes()
await edge_ops.remove_invalid_edges()
await graph_ops.validate_graph_integrity()
```

### Performance Optimization

```python
# Optimize graph performance
await graph_ops.optimize_indices()
await node_ops.optimize_node_storage()
await edge_ops.optimize_edge_storage()

# Generate performance statistics
stats = await graph_ops.generate_performance_stats()
```

### Best Practices for Agents

1. **Regular Maintenance**: Schedule regular maintenance operations
2. **Backup First**: Always backup before major maintenance operations
3. **Validation**: Validate graph integrity after maintenance
4. **Monitoring**: Monitor performance impacts of maintenance
5. **Documentation**: Document maintenance operations and results

### Maintenance Workflows

#### Daily Maintenance
```python
async def daily_maintenance():
    # Remove orphaned data
    await node_ops.cleanup_orphaned_nodes()
    await edge_ops.cleanup_orphaned_edges()
    
    # Validate integrity
    integrity_report = await graph_ops.validate_graph_integrity()
    
    # Generate statistics
    stats = await graph_ops.generate_daily_stats()
    
    return integrity_report, stats
```

#### Weekly Maintenance
```python
async def weekly_maintenance():
    # Deep cleanup operations
    await temporal_ops.archive_old_data()
    await community_ops.refresh_communities()
    
    # Performance optimization
    await graph_ops.optimize_indices()
    
    # Comprehensive validation
    validation_report = await graph_ops.comprehensive_validation()
    
    return validation_report
```

#### Monthly Maintenance
```python
async def monthly_maintenance():
    # Major optimization operations
    await graph_ops.full_optimization()
    
    # Community analysis
    community_report = await community_ops.analyze_communities()
    
    # Temporal analysis
    temporal_report = await temporal_ops.analyze_temporal_patterns()
    
    return community_report, temporal_report
```

### Maintenance Monitoring

```python
from graphiti_core.utils.maintenance.monitoring import MaintenanceMonitor

# Monitor maintenance operations
monitor = MaintenanceMonitor()

# Track operation performance
with monitor.track_operation("node_cleanup"):
    await node_ops.cleanup_orphaned_nodes()

# Generate maintenance reports
report = monitor.generate_report()
```

### Error Handling and Recovery

```python
from graphiti_core.utils.maintenance.errors import MaintenanceError

try:
    await maintenance_operation()
except MaintenanceError as e:
    # Handle maintenance-specific errors
    logger.error(f"Maintenance error: {e}")
    
    # Implement recovery procedures
    await recovery_operation()
    
    # Validate recovery
    await validate_recovery()
```

### Data Integrity Validation

```python
# Comprehensive integrity check
integrity_results = await graph_ops.validate_graph_integrity()

if not integrity_results.is_valid:
    # Handle integrity issues
    for issue in integrity_results.issues:
        if issue.severity == "critical":
            await handle_critical_issue(issue)
        elif issue.severity == "warning":
            await handle_warning_issue(issue)
```

### Performance Optimization

#### General Performance Guidelines
1. **Index Optimization**: Regularly optimize database indices
2. **Query Optimization**: Optimize frequently used queries
3. **Storage Optimization**: Optimize data storage layouts
4. **Memory Management**: Optimize memory usage patterns
5. **Concurrent Operations**: Optimize concurrent access patterns

#### Database-Specific Performance

**Neo4j Performance Optimization:**
- **Index Management**: Use BTREE and full-text indices appropriately
- **Query Tuning**: Optimize Cypher queries for large datasets
- **Memory Configuration**: Tune heap and page cache settings
- **Enterprise Features**: Leverage parallel runtime and clustering
- **APOC Procedures**: Use APOC for bulk operations and performance

**FalkorDB Performance Optimization:**
- **Memory Management**: Monitor Redis memory usage and limits
- **Persistence Settings**: Choose appropriate persistence strategy
- **Connection Pooling**: Use connection pooling for high throughput
- **Query Patterns**: Optimize for FalkorDB's graph query capabilities
- **Data Distribution**: Consider data partitioning for large graphs

### Maintenance Scheduling

```python
from graphiti_core.utils.maintenance.scheduler import MaintenanceScheduler

# Schedule regular maintenance
scheduler = MaintenanceScheduler()

# Schedule daily operations
scheduler.schedule_daily(daily_maintenance, hour=2)

# Schedule weekly operations
scheduler.schedule_weekly(weekly_maintenance, day="sunday", hour=1)

# Schedule monthly operations
scheduler.schedule_monthly(monthly_maintenance, day=1, hour=0)
```

### Custom Maintenance Operations

```python
# Create custom maintenance operation
class CustomMaintenanceOperation:
    def __init__(self, graphiti):
        self.graphiti = graphiti
    
    async def execute(self):
        # Custom maintenance logic
        pass
    
    async def validate(self):
        # Validation logic
        pass
    
    async def rollback(self):
        # Rollback logic if needed
        pass
```

### Maintenance Reporting

```python
# Generate comprehensive maintenance report
report = await graph_ops.generate_maintenance_report(
    include_statistics=True,
    include_performance=True,
    include_integrity=True,
    include_recommendations=True
)

# Save report
await report.save_to_file("maintenance_report.json")

# Send alerts if needed
if report.has_critical_issues():
    await send_maintenance_alert(report)
```

### Integration with Monitoring Systems

- **Logging**: Comprehensive logging of maintenance operations
- **Metrics**: Export maintenance metrics to monitoring systems
- **Alerts**: Automatic alerts for maintenance issues
- **Dashboards**: Integration with monitoring dashboards
- **API**: REST API for maintenance operations

### Best Practices Summary

1. **Proactive Maintenance**: Regular scheduled maintenance prevents issues
2. **Backup Strategy**: Always backup before major operations
3. **Validation**: Validate integrity after maintenance operations
4. **Monitoring**: Continuous monitoring of graph health
5. **Documentation**: Document all maintenance procedures and results