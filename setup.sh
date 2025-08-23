#!/bin/bash
# Setup script for Cognitive-Copilot OpenCode configuration

set -e

echo "🚀 Setting up Cognitive-Copilot with OpenCode Configuration"
echo "============================================================"

# Check if we're in the right directory
if [ ! -f "opencode.jsonc" ]; then
    echo "❌ Error: opencode.jsonc not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Found opencode.jsonc configuration"

# Check for required environment variables
echo ""
echo "🔧 Checking environment variables..."

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. You'll need to set this before using the MCP servers."
    echo "   export OPENAI_API_KEY='your-api-key-here'"
else
    echo "✅ OPENAI_API_KEY is set"
fi

if [ -z "$BRAVE_API_KEY" ]; then
    echo "ℹ️  BRAVE_API_KEY not set (optional for web search functionality)"
else
    echo "✅ BRAVE_API_KEY is set"
fi

# Install uv if not present
echo ""
echo "📦 Checking package managers..."

if ! command -v uv &> /dev/null; then
    echo "⚠️  uv not found. Installing uv package manager..."
    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    else
        echo "❌ curl not found. Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
else
    echo "✅ uv is available"
fi

# Install Node.js dependencies for MCP servers
echo ""
echo "📦 Installing Node.js MCP servers..."

if command -v npm &> /dev/null; then
    echo "Installing MCP servers globally..."
    npm install -g @modelcontextprotocol/server-sequential-thinking
    npm install -g @modelcontextprotocol/server-brave-search  
    npm install -g @modelcontextprotocol/server-filesystem
    echo "✅ MCP servers installed"
else
    echo "⚠️  npm not found. Please install Node.js to use additional MCP servers."
    echo "   The Graphiti MCP server will still work without npm."
fi

# Setup Graphiti project
echo ""
echo "🔧 Setting up Graphiti project..."

cd graphiti

# Install Python dependencies
if command -v uv &> /dev/null; then
    echo "Installing Python dependencies with uv..."
    uv sync --extra dev
    echo "✅ Graphiti dependencies installed"
else
    echo "⚠️  uv not available, skipping Python dependency installation"
fi

cd ..

# Check Docker for MCP server
echo ""
echo "🐳 Checking Docker setup..."

if command -v docker &> /dev/null; then
    echo "✅ Docker is available"
    
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        echo "✅ Docker Compose is available"
        echo "💡 You can start the MCP server stack with: cd graphiti/mcp_server && docker compose up"
    else
        echo "⚠️  Docker Compose not found"
    fi
else
    echo "⚠️  Docker not found. You'll need Docker to run the Graphiti MCP server."
fi

# Validate configuration
echo ""
echo "🔍 Validating configuration..."
python validate_config.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your API keys:"
echo "   export OPENAI_API_KEY='your-openai-api-key'"
echo "   export BRAVE_API_KEY='your-brave-api-key'  # Optional"
echo ""
echo "2. Start the Graphiti MCP server:"
echo "   cd graphiti/mcp_server"
echo "   docker compose up -d"
echo ""
echo "3. Start using OpenCode with the configured agents!"
echo ""
echo "📖 See OPENCODE.md for detailed instructions and usage examples."