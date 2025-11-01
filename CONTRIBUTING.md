# Contributing to MATLAB MCP Server

Thank you for your interest in contributing! This guide covers development setup, project structure, and testing.

## Development Setup

### From Source Installation

Clone the repository and install with uv:

```bash
git clone https://github.com/subspace-lab/matlab-mcp-server
cd matlab-mcp-server
uv sync
```

### MATLAB Library Path Configuration

#### Quick Setup (Recommended)

Auto-detect your MATLAB installation and generate `.env` file:

```bash
uv run scripts/setup_matlab_env.py
```

This will:
- Find all MATLAB installations on your system
- Detect the correct architecture (Intel/Apple Silicon/Linux/Windows)
- Create a `.env` file with the proper library paths

#### Manual Configuration

If MATLAB is **not** in the default location, manually create `.env`:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and uncomment/modify the appropriate line for your system:
```

**macOS (Apple Silicon):**
```bash
DYLD_LIBRARY_PATH=/Applications/MATLAB_R20XXx.app/bin/maca64
```

**macOS (Intel):**
```bash
DYLD_LIBRARY_PATH=/Applications/MATLAB_R20XXx.app/bin/maci64
```

**Linux:**
```bash
LD_LIBRARY_PATH=/usr/local/MATLAB/R20XXx/bin/glnxa64
```

**Windows:**
Usually not needed as the installer handles this automatically.

Replace `R20XXx` with your MATLAB version (e.g., R2024a, R2024b, R2025a).

### Using the .env File

After creating `.env`, run commands with:

```bash
# Single command execution
uv run --env-file .env matlab-cli -c "disp('Hello MATLAB')"

# MCP server
uv run --env-file .env matlab-mcp
```

Or set `UV_ENV_FILE` environment variable:

```bash
export UV_ENV_FILE=.env
uv run matlab-cli -c "disp('Hello')"
```

### Editable Installation

For active development, install in editable mode:

```bash
cd matlab-mcp-server
uv sync
```

The CLI tools will be available in `.venv/bin/`:
- `.venv/bin/matlab-cli`
- `.venv/bin/matlab-mcp`

Or activate the virtual environment:

```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Now you can use the commands directly:
matlab-cli --help
matlab-mcp
```

### Claude Code Configuration (Development)

When running from source, create `.mcp.json` in your project root directory:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/matlab-mcp-server",
        "run",
        "--env-file",
        ".env",
        "matlab-mcp"
      ]
    }
  }
}
```

Replace `/absolute/path/to/matlab-mcp-server` with the actual path to your cloned repository.

**Note:** For Claude Desktop, use `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows) instead.

## Project Structure

```
matlab-mcp-server/
├── src/
│   └── matlab_mcp_server/
│       ├── __init__.py       # Package initialization
│       ├── server.py         # MCP server (8 tools, resources)
│       ├── cli.py            # Command-line interface
│       ├── engine.py         # MATLAB engine wrapper (enhanced)
│       ├── tools.py          # Tool implementations
│       └── resources.py      # Resource handlers
├── examples/                 # Demo scripts
│   ├── essentials_demo.py   # Comprehensive tool demo
│   ├── basic_test.py        # Basic engine usage
│   ├── shared_session_demo.py
│   └── ...
├── tests/                    # Unit tests
│   ├── test_engine.py
│   └── test_server.py
├── scripts/                  # Setup and utility scripts
│   ├── setup_matlab_env.py  # Auto-detect MATLAB
│   └── ...
├── md-files/                 # Internal documentation
│   ├── PLANNING.md          # Roadmap and implementation notes
│   ├── TOOLS.md             # Tool catalog
│   ├── MATLAB_MCP_GUIDE.md  # Detailed user guide
│   └── ...
├── temp/                     # Test scripts
├── pyproject.toml            # Project configuration
├── .env.example              # Environment template
├── README.md                 # User documentation
└── CONTRIBUTING.md           # This file
```

### Key Files

- **`server.py`**: MCP server implementation, defines tools and resources
- **`engine.py`**: Enhanced MATLAB engine wrapper with error handling
- **`cli.py`**: Command-line interface for standalone usage
- **`tools.py`**: Tool implementations and business logic
- **`resources.py`**: Resource handlers for documentation and session info

## Running Locally

### Run MCP Server

```bash
uv run --env-file .env matlab-mcp
```

### Run CLI

```bash
# Single command
uv run --env-file .env matlab-cli -c "disp('Hello')"

# Script file
uv run --env-file .env matlab-cli -f examples/test_script.m

# Interactive REPL
uv run --env-file .env matlab-cli -i

# Verbose output
uv run --env-file .env matlab-cli -c "x = magic(5)" -v
```

## Testing

### MCP Inspector

Test the server interactively using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv --directory $(pwd) run --env-file .env matlab-mcp
```

This provides a web UI to:
- Explore all tools and their schemas
- Test tool calls with different parameters
- View resources
- Debug MCP communication

### Unit Tests

Run the test suite:

```bash
# Run all tests
uv run --env-file .env pytest

# Run specific test file
uv run --env-file .env pytest tests/test_engine.py

# Run with verbose output
uv run --env-file .env pytest -v
```

### Example Scripts

Test with example scripts:

```bash
# Comprehensive demo
uv run --env-file .env python examples/essentials_demo.py

# Basic tests
uv run --env-file .env python examples/basic_test.py

# Advanced features
uv run --env-file .env python examples/advanced_test.py
```

### Manual Testing

Quick manual tests:

```bash
# Test MATLAB engine
uv run --env-file .env python temp/test_new_tools.py

# Test session management
uv run --env-file .env python temp/test_session_tool.py
```

## Exploring Tools (for AI Assistants)

If you're an AI assistant working with this codebase:

1. **Use MCP Inspector** to explore all tools interactively:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory $(pwd) run --env-file .env matlab-mcp
   ```

2. **Call `list_tools()`** to see all available tools with schemas

3. **Read implementation**:
   - Tool schemas: `src/matlab_mcp_server/server.py:list_tools()`
   - Tool implementations: `src/matlab_mcp_server/engine.py` (has detailed docstrings)
   - Resource definitions: `src/matlab_mcp_server/resources.py`

4. **Check examples** in `examples/` directory for usage patterns

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test locally:
   ```bash
   uv run --env-file .env pytest
   uv run --env-file .env python examples/essentials_demo.py
   ```

4. Test with MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector uv --directory $(pwd) run --env-file .env matlab-mcp
   ```

5. Commit and push:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin feature/your-feature-name
   ```

6. Open a pull request

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to public functions and classes
- Keep functions focused and modular

### Adding New Tools

1. Add tool schema in `server.py:list_tools()`
2. Implement tool logic in `engine.py`
3. Add tests in `tests/test_engine.py`
4. Update documentation in `TOOLS.md`
5. Add example usage in `examples/`

### Adding Resources

1. Add resource definition in `server.py:list_resources()`
2. Implement resource handler in `resources.py`
3. Update documentation

## Building and Distribution

### Build Package

```bash
uv build
```

This creates distribution files in `dist/`:
- `matlab_mcp_server-X.Y.Z-py3-none-any.whl`
- `matlab_mcp_server-X.Y.Z.tar.gz`

### Local Installation from Build

```bash
uv pip install dist/matlab_mcp_server-X.Y.Z-py3-none-any.whl
```

### Publishing to PyPI

```bash
# Publish to PyPI
uv publish --token $UV_PUBLISH_TOKEN
```

## Documentation

### Internal Documentation

- **`PLANNING.md`**: Roadmap, architecture decisions, implementation notes
- **`TOOLS.md`**: Detailed tool catalog with all operations
- **`MATLAB_MCP_GUIDE.md`**: Comprehensive user guide
- **`TESTING.md`**: Testing strategies and scenarios
- **`RESOURCES.md`**: Resource specifications

### Updating Documentation

When adding features:
1. Update `README.md` for user-facing changes
2. Update `TOOLS.md` for new tools/operations
3. Update `PLANNING.md` for architecture changes
4. Add examples to `examples/`

## Getting Help

- Check existing [issues](https://github.com/subspace-lab/matlab-mcp-server/issues)
- Read the [planning docs](md-files/PLANNING.md)
- Review example scripts in `examples/`

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the project
- Help others learn and grow

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

