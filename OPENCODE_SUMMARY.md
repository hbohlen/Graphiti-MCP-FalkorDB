# OpenCode Configuration Summary

This repository now includes a comprehensive OpenCode configuration for AI-powered development with the Graphiti knowledge graph framework.

## 🚀 Quick Start

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Set your API keys:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export BRAVE_API_KEY="your-brave-api-key"  # Optional
   ```

3. **Start the MCP server stack:**
   ```bash
   cd graphiti/mcp_server
   docker compose up -d
   ```

## 🔧 What's Included

### MCP Servers (4 configured)
- **graphiti-memory**: Knowledge graph storage and search
- **sequential-thinking**: Enhanced reasoning capabilities  
- **brave-search**: Web search for research
- **filesystem**: Enhanced file operations

### Specialized Agents (5 configured)
- **Graphiti Knowledge Engineer**: Knowledge graph expert
- **Research Assistant**: Web search + knowledge synthesis
- **Full Stack Developer**: Framework development specialist
- **Documentation Specialist**: Technical documentation expert
- **DevOps Engineer**: Infrastructure and deployment specialist

### Quick Commands (7 available)
- `setup`, `test`, `lint`, `format`, `check`
- `start-mcp`, `stop-mcp`

## 📖 Documentation

- **OPENCODE.md**: Detailed setup and usage guide
- **opencode.jsonc**: Complete configuration file
- **graphiti/AGENTS.md**: Framework development patterns
- **graphiti/mcp_server/AGENTS.md**: MCP server integration guide

## ✅ Validation

Run `python validate_config.py` to verify your configuration is working correctly.

---

**Ready to build knowledge graphs with AI assistance!** 🎉