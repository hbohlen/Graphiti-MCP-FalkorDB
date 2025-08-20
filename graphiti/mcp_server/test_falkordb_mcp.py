#!/usr/bin/env python3
"""
Test script to verify FalkorDB MCP functionality
"""
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path to import graphiti modules
sys.path.append(str(Path(__file__).parent.parent))

from graphiti_core.driver.falkordb_driver import FalkorDriver
from dotenv import load_dotenv

load_dotenv()

async def test_falkordb_integration():
    """Test FalkorDB connection and basic operations"""
    
    print("Testing FalkorDB Integration")
    print("=" * 50)
    
    try:
        # Test 1: Basic connection
        print("1. Testing FalkorDB connection...")
        driver = FalkorDriver(
            host=os.getenv('FALKORDB_HOST', 'localhost'),
            port=int(os.getenv('FALKORDB_PORT', 6379)),
            username=os.getenv('FALKORDB_USER') or None,
            password=os.getenv('FALKORDB_PASSWORD') or None
        )
        
        # Test 2: Health check
        print("2. Running health check...")
        result = await driver.execute_query("MATCH (n) RETURN count(n) as node_count")
        print(f"   SUCCESS Connected! Current node count: {result[0][0]['node_count'] if result and result[0] else 0}")
        
        # Test 3: Create a test node
        print("3. Creating test node...")
        await driver.execute_query(
            "CREATE (test:TestNode {name: $name, timestamp: $timestamp})",
            name="FalkorDB_Test",
            timestamp="2025-08-18T04:26:00Z"
        )
        print("   SUCCESS Test node created")
        
        # Test 4: Query the test node
        print("4. Querying test node...")
        result = await driver.execute_query(
            "MATCH (test:TestNode {name: $name}) RETURN test.name, test.timestamp",
            name="FalkorDB_Test"
        )
        if result and result[0]:
            node_data = result[0][0]
            print(f"   SUCCESS Found test node: {node_data}")
        
        # Test 5: Clean up
        print("5. Cleaning up test data...")
        await driver.execute_query("MATCH (test:TestNode) DELETE test")
        print("   SUCCESS Test data cleaned up")
        
        # Close connection
        await driver.close()
        print("\nAll tests passed! FalkorDB is working correctly with Graphiti.")
        return True
        
    except Exception as e:
        print(f"\nTest failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_falkordb_integration())
    sys.exit(0 if success else 1)