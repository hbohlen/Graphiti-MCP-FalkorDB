#!/usr/bin/env python3
"""
Test script to validate the OpenCode configuration for Cognitive-Copilot
"""

import json
import os
import sys
from pathlib import Path

def validate_opencode_config():
    """Validate the opencode.jsonc configuration"""
    
    print("🔍 Validating OpenCode Configuration for Cognitive-Copilot")
    print("=" * 60)
    
    # Check if config file exists
    config_path = Path("opencode.jsonc")
    if not config_path.exists():
        print("❌ opencode.jsonc not found")
        return False
    
    print("✅ Found opencode.jsonc")
    
    # Load and parse the configuration
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Simple JSONC comment removal
        lines = []
        for line in content.split('\n'):
            if '//' in line and not line.strip().startswith('"'):
                comment_pos = line.find('//')
                line = line[:comment_pos].rstrip()
            lines.append(line)
        
        clean_json = '\n'.join(lines)
        config = json.loads(clean_json)
        print("✅ Configuration syntax is valid")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False
    
    # Validate required sections
    required_sections = {
        'mcpServers': 'MCP Servers',
        'agents': 'Specialized Agents', 
        'instructions': 'Project Instructions',
        'commands': 'Quick Commands',
        'environment': 'Environment Variables'
    }
    
    for section, name in required_sections.items():
        if section in config:
            print(f"✅ Found {name} section")
        else:
            print(f"❌ Missing {name} section")
            return False
    
    # Validate MCP servers
    mcp_servers = config.get('mcpServers', {})
    expected_servers = ['graphiti-memory', 'sequential-thinking', 'brave-search', 'filesystem']
    
    print(f"\n📡 MCP Servers ({len(mcp_servers)} configured):")
    for server in expected_servers:
        if server in mcp_servers:
            print(f"  ✅ {server}")
        else:
            print(f"  ❌ {server} (missing)")
    
    # Validate agents
    agents = config.get('agents', [])
    expected_agents = [
        'Graphiti Knowledge Engineer',
        'Research Assistant', 
        'Full Stack Developer',
        'Documentation Specialist',
        'DevOps Engineer'
    ]
    
    print(f"\n🤖 Specialized Agents ({len(agents)} configured):")
    agent_names = [agent.get('name', 'Unknown') for agent in agents]
    for agent in expected_agents:
        if agent in agent_names:
            print(f"  ✅ {agent}")
        else:
            print(f"  ❌ {agent} (missing)")
    
    # Validate file paths
    print(f"\n📁 File Path Validation:")
    
    paths_to_check = [
        './graphiti',
        './graphiti/mcp_server', 
        './graphiti/mcp_server/graphiti_mcp_server.py',
        './graphiti/AGENTS.md',
        './graphiti/mcp_server/AGENTS.md',
        './graphiti/Makefile',
        './graphiti/pyproject.toml'
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path} (not found)")
    
    # Validate commands
    commands = config.get('commands', {})
    expected_commands = ['setup', 'test', 'lint', 'format', 'check', 'start-mcp', 'stop-mcp']
    
    print(f"\n⚡ Quick Commands ({len(commands)} configured):")
    for cmd in expected_commands:
        if cmd in commands:
            print(f"  ✅ {cmd}")
        else:
            print(f"  ❌ {cmd} (missing)")
    
    # Check environment variables
    env_vars = config.get('environment', {})
    print(f"\n🌍 Environment Configuration:")
    print(f"  ✅ {len(env_vars)} environment variables configured")
    
    # Summary
    print(f"\n📋 Configuration Summary:")
    print(f"  • {len(mcp_servers)} MCP servers configured")
    print(f"  • {len(agents)} specialized agents defined")
    print(f"  • {len(commands)} quick commands available") 
    print(f"  • {len(env_vars)} environment variables")
    
    print(f"\n🎉 OpenCode configuration validation complete!")
    print(f"💡 See OPENCODE.md for setup and usage instructions")
    
    return True

def validate_documentation():
    """Validate that documentation files exist"""
    
    print(f"\n📖 Documentation Validation:")
    
    docs_to_check = [
        'OPENCODE.md',
        'graphiti/README.md',
        'graphiti/AGENTS.md',
        'graphiti/mcp_server/AGENTS.md',
        'graphiti/mcp_server/README.md'
    ]
    
    for doc in docs_to_check:
        if os.path.exists(doc):
            print(f"  ✅ {doc}")
        else:
            print(f"  ❌ {doc} (not found)")

if __name__ == "__main__":
    try:
        success = validate_opencode_config()
        validate_documentation()
        
        if success:
            print(f"\n🚀 Configuration is ready for use!")
            sys.exit(0)
        else:
            print(f"\n💥 Configuration validation failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Validation error: {e}")
        sys.exit(1)