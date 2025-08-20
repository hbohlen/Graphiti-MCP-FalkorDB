#!/usr/bin/env python3
"""
Simple FalkorDB Browser - A minimal web interface for FalkorDB
Works around Docker Desktop networking issues on Windows
"""
import asyncio
import sys
import os
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
import json

# Add parent directory to path to import graphiti modules
sys.path.append(str(Path(__file__).parent.parent))

from graphiti_core.driver.falkordb_driver import FalkorDriver
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# HTML template for the browser interface
BROWSER_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FalkorDB Browser</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .query-section { margin-bottom: 30px; }
        .query-input { width: 100%; height: 100px; font-family: monospace; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        .execute-btn { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        .execute-btn:hover { background: #005a87; }
        .results { margin-top: 20px; }
        .result-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        .result-table th, .result-table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .result-table th { background-color: #f2f2f2; }
        .error { color: red; background: #ffeaea; padding: 10px; border-radius: 4px; margin-top: 10px; }
        .success { color: green; background: #eafaf1; padding: 10px; border-radius: 4px; margin-top: 10px; }
        .examples { background: #f8f9fa; padding: 15px; border-radius: 4px; margin-bottom: 20px; }
        .example-query { background: #e9ecef; padding: 5px; border-radius: 3px; font-family: monospace; margin: 5px 0; cursor: pointer; }
        .example-query:hover { background: #dee2e6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 FalkorDB Browser</h1>
        <p>Connected to: <strong>localhost:6379</strong></p>
        
        <div class="examples">
            <h3>Example Queries (click to use):</h3>
            <div class="example-query" onclick="setQuery('MATCH (n) RETURN count(n) as node_count')">MATCH (n) RETURN count(n) as node_count</div>
            <div class="example-query" onclick="setQuery('MATCH (n) RETURN n LIMIT 10')">MATCH (n) RETURN n LIMIT 10</div>
            <div class="example-query" onclick="setQuery('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 5')">MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 5</div>
            <div class="example-query" onclick="setQuery('CREATE (test:TestNode {name: \\'Browser Test\\', timestamp: \\'{{ timestamp }}\\'}) RETURN test')">CREATE (test:TestNode {name: 'Browser Test', timestamp: '{{ timestamp }}'}) RETURN test</div>
        </div>
        
        <div class="query-section">
            <h3>Execute Cypher Query:</h3>
            <textarea id="queryInput" class="query-input" placeholder="Enter your Cypher query here...">MATCH (n) RETURN count(n) as node_count</textarea>
            <br>
            <button class="execute-btn" onclick="executeQuery()">Execute Query</button>
        </div>
        
        <div id="results" class="results"></div>
    </div>

    <script>
        function setQuery(query) {
            document.getElementById('queryInput').value = query.replace('{{ timestamp }}', new Date().toISOString());
        }
        
        async function executeQuery() {
            const query = document.getElementById('queryInput').value;
            const resultsDiv = document.getElementById('results');
            
            if (!query.trim()) {
                resultsDiv.innerHTML = '<div class="error">Please enter a query</div>';
                return;
            }
            
            resultsDiv.innerHTML = '<div>Executing query...</div>';
            
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query})
                });
                
                const result = await response.json();
                
                if (result.error) {
                    resultsDiv.innerHTML = `<div class="error">Error: ${result.error}</div>`;
                } else {
                    displayResults(result);
                }
            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">Network error: ${error.message}</div>`;
            }
        }
        
        function displayResults(result) {
            const resultsDiv = document.getElementById('results');
            
            if (!result.data || result.data.length === 0) {
                resultsDiv.innerHTML = '<div class="success">Query executed successfully. No results returned.</div>';
                return;
            }
            
            let html = '<div class="success">Query executed successfully</div>';
            html += '<table class="result-table">';
            
            // Headers
            if (result.headers && result.headers.length > 0) {
                html += '<thead><tr>';
                result.headers.forEach(header => {
                    html += `<th>${escapeHtml(header)}</th>`;
                });
                html += '</tr></thead>';
            }
            
            // Data
            html += '<tbody>';
            result.data.forEach(row => {
                html += '<tr>';
                if (result.headers) {
                    result.headers.forEach(header => {
                        const value = row[header];
                        html += `<td>${escapeHtml(JSON.stringify(value, null, 2))}</td>`;
                    });
                } else {
                    Object.values(row).forEach(value => {
                        html += `<td>${escapeHtml(JSON.stringify(value, null, 2))}</td>`;
                    });
                }
                html += '</tr>';
            });
            html += '</tbody></table>';
            
            resultsDiv.innerHTML = html;
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Allow Enter key to execute query (Ctrl+Enter)
        document.getElementById('queryInput').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                executeQuery();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def browser():
    """Serve the browser interface"""
    return render_template_string(BROWSER_TEMPLATE)

@app.route('/execute', methods=['POST'])
def execute_query():
    """Execute a Cypher query against FalkorDB"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
        
        # Run the async query
        result = asyncio.run(run_query(query))
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def run_query(query):
    """Execute query asynchronously"""
    try:
        driver = FalkorDriver(
            host=os.getenv('FALKORDB_HOST', 'localhost'),
            port=int(os.getenv('FALKORDB_PORT', 6379)),
            username=os.getenv('FALKORDB_USER') or None,
            password=os.getenv('FALKORDB_PASSWORD') or None
        )
        
        result = await driver.execute_query(query)
        await driver.close()
        
        if result:
            data, headers, _ = result
            return {
                'data': data,
                'headers': headers,
                'count': len(data) if data else 0
            }
        else:
            return {
                'data': [],
                'headers': [],
                'count': 0
            }
            
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    print("🔗 FalkorDB Browser starting...")
    print("📍 Access the browser at: http://localhost:5000")
    print("🔧 Make sure FalkorDB is running on localhost:6379")
    app.run(host='0.0.0.0', port=5000, debug=True)