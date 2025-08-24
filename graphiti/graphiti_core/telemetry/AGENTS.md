# AGENTS.md

This file provides guidance to AI agents when working with telemetry components.

## Directory Overview

This directory contains telemetry and monitoring functionality for tracking Graphiti operations, performance metrics, and system health.

## Files

- `telemetry.py` - Core telemetry implementation and metrics collection
- `__init__.py` - Module initialization and telemetry exports

## Telemetry Architecture

### Purpose and Function

Telemetry provides visibility into:

1. **Performance Metrics**: Operation latency, throughput, and resource usage
2. **System Health**: Error rates, success rates, and system status
3. **Usage Analytics**: Feature usage patterns and user behavior
4. **Resource Monitoring**: Database performance, memory usage, API calls
5. **Debugging Information**: Detailed logs for troubleshooting

### Metrics Categories

1. **Operation Metrics**: Individual operation performance and success rates
2. **System Metrics**: Overall system health and resource utilization
3. **User Metrics**: Usage patterns and feature adoption
4. **Error Metrics**: Error rates, types, and recovery patterns
5. **Business Metrics**: High-level business and usage insights

## Agent Guidelines

### Basic Telemetry Usage

```python
from graphiti_core.telemetry import TelemetryManager

# Initialize telemetry
telemetry = TelemetryManager(
    service_name="graphiti-agent",
    environment="production",
    enable_logging=True,
    enable_metrics=True
)

# Track operation
with telemetry.track_operation("entity_extraction"):
    entities = await extract_entities(text)

# Record custom metric
telemetry.record_metric(
    name="entities_extracted",
    value=len(entities),
    tags={"operation": "batch_processing"}
)
```

### Performance Monitoring

```python
# Monitor operation performance
@telemetry.monitor_performance
async def process_episode(episode_data):
    # Operation implementation
    result = await graphiti.add_episode(episode_data)
    
    # Record success
    telemetry.record_success("episode_processing")
    
    return result

# Monitor with custom context
async def batch_process_episodes(episodes):
    with telemetry.operation_context("batch_processing"):
        for i, episode in enumerate(episodes):
            telemetry.record_metric("batch_progress", i / len(episodes))
            await process_episode(episode)
```

### Best Practices for Agents

1. **Comprehensive Tracking**: Track all significant operations
2. **Contextual Information**: Include relevant context in telemetry data
3. **Performance Impact**: Minimize telemetry overhead on operations
4. **Privacy Awareness**: Avoid logging sensitive information
5. **Actionable Metrics**: Focus on metrics that enable decisions

### Error Tracking

```python
# Track errors and exceptions
try:
    result = await risky_operation()
except Exception as e:
    telemetry.record_error(
        operation="risky_operation",
        error_type=type(e).__name__,
        error_message=str(e),
        context={"user_id": user_id, "operation_id": op_id}
    )
    raise
```

### Custom Metrics

```python
# Define custom metrics for your use case
class AgentTelemetry:
    def __init__(self, telemetry_manager):
        self.telemetry = telemetry_manager
    
    def track_knowledge_extraction(self, text_length, entities_found, relationships_found):
        self.telemetry.record_metric("text_processing_length", text_length)
        self.telemetry.record_metric("entities_extracted", entities_found)
        self.telemetry.record_metric("relationships_extracted", relationships_found)
        
        # Calculate derived metrics
        entity_density = entities_found / text_length if text_length > 0 else 0
        self.telemetry.record_metric("entity_density", entity_density)
    
    def track_search_performance(self, query, results_count, latency):
        self.telemetry.record_metric(
            "search_latency", 
            latency,
            tags={"query_type": self.classify_query(query)}
        )
        self.telemetry.record_metric("search_results_count", results_count)
```

### Distributed Tracing

```python
# Track operations across distributed systems
async def distributed_operation():
    trace_id = telemetry.start_trace("distributed_processing")
    
    try:
        # Step 1: Entity extraction
        with telemetry.span("entity_extraction", trace_id):
            entities = await extract_entities(text)
        
        # Step 2: Relationship discovery
        with telemetry.span("relationship_discovery", trace_id):
            relationships = await discover_relationships(entities)
        
        # Step 3: Graph update
        with telemetry.span("graph_update", trace_id):
            await update_graph(entities, relationships)
            
        telemetry.end_trace(trace_id, status="success")
        
    except Exception as e:
        telemetry.end_trace(trace_id, status="error", error=str(e))
        raise
```

### Resource Monitoring

```python
# Monitor resource usage
class ResourceMonitor:
    def __init__(self, telemetry):
        self.telemetry = telemetry
        self.start_monitoring()
    
    def start_monitoring(self):
        # Monitor database connections
        self.monitor_database_connections()
        
        # Monitor API rate limits
        self.monitor_api_usage()
        
        # Monitor memory usage
        self.monitor_memory_usage()
    
    async def monitor_database_connections(self):
        while True:
            connection_count = await get_active_connections()
            self.telemetry.record_metric("db_connections_active", connection_count)
            
            # Database-specific monitoring
            db_type = get_database_type()  # "neo4j" or "falkordb"
            
            if db_type == "neo4j":
                await self.monitor_neo4j_metrics()
            elif db_type == "falkordb":
                await self.monitor_falkordb_metrics()
                
            await asyncio.sleep(60)  # Check every minute
    
    async def monitor_neo4j_metrics(self):
        # Neo4j-specific metrics
        pool_status = await get_neo4j_pool_status()
        self.telemetry.record_metric("neo4j_pool_active", pool_status.active)
        self.telemetry.record_metric("neo4j_pool_idle", pool_status.idle)
        
        # Query performance
        query_stats = await get_neo4j_query_stats()
        self.telemetry.record_metric("neo4j_query_duration_avg", query_stats.avg_duration)
        
    async def monitor_falkordb_metrics(self):
        # FalkorDB-specific metrics
        redis_info = await get_falkordb_info()
        self.telemetry.record_metric("falkordb_memory_used", redis_info.used_memory)
        self.telemetry.record_metric("falkordb_commands_processed", redis_info.total_commands_processed)
        
        # Graph-specific metrics
        graph_stats = await get_falkordb_graph_stats()
        self.telemetry.record_metric("falkordb_nodes_count", graph_stats.node_count)
        self.telemetry.record_metric("falkordb_edges_count", graph_stats.edge_count)
    
    def monitor_api_usage(self):
        # Track API calls and rate limits
        for provider in ["openai", "anthropic", "google"]:
            usage = get_api_usage(provider)
            self.telemetry.record_metric(
                f"api_calls_{provider}",
                usage.calls_count,
                tags={"time_window": "1h"}
            )
```

### Business Metrics

```python
# Track business-relevant metrics
class BusinessTelemetry:
    def __init__(self, telemetry):
        self.telemetry = telemetry
    
    def track_user_engagement(self, user_id, session_duration, operations_count):
        self.telemetry.record_metric(
            "user_session_duration",
            session_duration,
            tags={"user_id": user_id}
        )
        self.telemetry.record_metric(
            "user_operations_count",
            operations_count,
            tags={"user_id": user_id}
        )
    
    def track_knowledge_growth(self, new_entities, new_relationships):
        self.telemetry.record_metric("knowledge_base_growth_entities", new_entities)
        self.telemetry.record_metric("knowledge_base_growth_relationships", new_relationships)
    
    def track_search_success(self, query, found_results, user_clicked):
        self.telemetry.record_metric("search_results_found", found_results)
        self.telemetry.record_metric(
            "search_success_rate",
            1 if user_clicked else 0,
            tags={"query_complexity": self.classify_query_complexity(query)}
        )
```

### Alerting and Notifications

```python
# Set up alerts based on telemetry data
class TelemetryAlerting:
    def __init__(self, telemetry):
        self.telemetry = telemetry
        self.alert_rules = self.setup_alert_rules()
    
    def setup_alert_rules(self):
        return [
            {
                "metric": "error_rate",
                "threshold": 0.05,  # 5% error rate
                "window": "5m",
                "action": self.send_error_alert
            },
            {
                "metric": "response_latency_p95",
                "threshold": 5000,  # 5 seconds
                "window": "10m", 
                "action": self.send_performance_alert
            }
        ]
    
    async def check_alerts(self):
        for rule in self.alert_rules:
            current_value = await self.telemetry.get_metric_value(
                rule["metric"],
                window=rule["window"]
            )
            
            if current_value > rule["threshold"]:
                await rule["action"](rule["metric"], current_value)
```

### Configuration and Setup

```python
# Configure telemetry for different environments
def setup_telemetry(environment):
    if environment == "production":
        return TelemetryManager(
            service_name="graphiti-production",
            log_level="INFO",
            sampling_rate=1.0,  # Sample all operations
            export_to=["prometheus", "jaeger", "cloudwatch"]
        )
    elif environment == "staging":
        return TelemetryManager(
            service_name="graphiti-staging",
            log_level="DEBUG",
            sampling_rate=0.1,  # Sample 10% of operations
            export_to=["prometheus", "jaeger"]
        )
    else:  # development
        return TelemetryManager(
            service_name="graphiti-dev",
            log_level="DEBUG",
            sampling_rate=0.01,  # Sample 1% of operations
            export_to=["console"]
        )
```

### Privacy and Security

```python
# Handle sensitive data in telemetry
class PrivacyAwareTelemetry:
    def __init__(self, telemetry):
        self.telemetry = telemetry
        self.sensitive_fields = ["user_id", "email", "personal_data"]
    
    def sanitize_data(self, data):
        # Remove or hash sensitive information
        sanitized = {}
        for key, value in data.items():
            if key in self.sensitive_fields:
                sanitized[key] = self.hash_sensitive_value(value)
            else:
                sanitized[key] = value
        return sanitized
    
    def record_operation(self, operation_name, data):
        sanitized_data = self.sanitize_data(data)
        self.telemetry.record_operation(operation_name, sanitized_data)
```

### Testing and Validation

```python
# Test telemetry functionality
def test_telemetry_metrics():
    test_telemetry = TelemetryManager(
        service_name="test",
        export_to=["memory"]  # Store in memory for testing
    )
    
    # Record test metrics
    test_telemetry.record_metric("test_metric", 42)
    test_telemetry.record_error("test_operation", "TestError", "Test error message")
    
    # Validate metrics were recorded
    metrics = test_telemetry.get_recorded_metrics()
    assert "test_metric" in metrics
    assert metrics["test_metric"][-1]["value"] == 42
```

### Integration with Monitoring Systems

```python
# Export telemetry to external systems
class TelemetryExporter:
    def __init__(self):
        self.exporters = {
            "prometheus": PrometheusExporter(),
            "datadog": DatadogExporter(),
            "cloudwatch": CloudWatchExporter(),
            "jaeger": JaegerExporter()
        }
    
    async def export_metrics(self, metrics):
        for exporter_name, exporter in self.exporters.items():
            try:
                await exporter.export(metrics)
            except Exception as e:
                logger.error(f"Failed to export to {exporter_name}: {e}")
```

### Best Practices Summary

1. **Comprehensive Coverage**: Track all significant operations and their outcomes
2. **Performance Awareness**: Minimize telemetry overhead on system performance
3. **Privacy Protection**: Sanitize sensitive data before logging
4. **Actionable Metrics**: Focus on metrics that enable operational decisions
5. **Monitoring Integration**: Export telemetry data to monitoring and alerting systems