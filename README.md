# MATLAB MCP Server

A Model Context Protocol (MCP) server that enables seamless integration between MATLAB and MCP-compatible applications. Execute MATLAB code, manage workspace variables, create plots, handle data I/O, and more - all through a token-efficient MCP interface.

## Features

### Essential Tools

- **Execute MATLAB Code**: Run MATLAB commands and scripts
- **Workspace Management**: Get, set, list, and clear workspace variables
- **Figure Operations**: Save, export, and close MATLAB figures (PNG, SVG, PDF, etc.)
- **Data I/O**: Import/export data (CSV, JSON, XLSX) and load/save MAT files
- **Environment Info**: Check MATLAB version and installed toolboxes
- **Documentation Access**: Get MATLAB help, search functions, and find toolbox locations
- **Meta-tools**: Intelligent routing and mode selection for extensibility

### Core Features

- **Persistent Session**: Maintains MATLAB session across tool calls
- **CLI Interface**: Command execution, file execution, and interactive REPL modes
- **Token-Efficient Design**: Multi-operation tools minimize token footprint
- **JSON Resources**: Structured access to workspace, toolboxes, and session info
- **Error Handling**: Comprehensive error reporting

## Quick Start

**No installation needed!** Just configure your MATLAB path and add to Claude Desktop.

### 1. Find your MATLAB library path

```bash
# macOS Apple Silicon
/Applications/MATLAB_R20XXx.app/bin/maca64

# macOS Intel
/Applications/MATLAB_R20XXx.app/bin/maci64

# Linux
/usr/local/MATLAB/R20XXx/bin/glnxa64
```

Replace `R20XXx` with your MATLAB version (e.g., R2024a, R2024b, R2025a, R2025b)

### 2. Add to Claude Desktop config

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**macOS (Apple Silicon):**
```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R20XXx.app/bin/maca64"
      }
    }
  }
}
```

**macOS (Intel):**
```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R20XXx.app/bin/maci64"
      }
    }
  }
}
```

**Linux:**
```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "LD_LIBRARY_PATH": "/usr/local/MATLAB/R20XXx/bin/glnxa64"
      }
    }
  }
}
```

Replace `R20XXx` with your actual MATLAB version.

### 3. Restart Claude Desktop

That's it! `uvx` will automatically download and run the latest version from PyPI.

## Prerequisites

- Python 3.10-3.13
- MATLAB installed on your system (R2024a or later recommended)
- `uv` package manager ([installation](https://github.com/astral-sh/uv))

## Installation

### From PyPI (Recommended)

Install the latest stable version from PyPI using uv:

```bash
uv pip install matlab-mcp-server
```

Or with pip (if you don't have uv):

```bash
pip install matlab-mcp-server
```

This automatically installs:
- The matlab-mcp-server package
- The matlabengine package from PyPI
- Makes `matlab-cli` and `matlab-mcp` commands available globally

### From Source (For Development)

Clone the repository and install with uv:

```bash
git clone https://github.com/subspace-lab/matlab-mcp-server
cd matlab-mcp-server
uv sync
```

### Version Matching

The `matlabengine` package version should match your MATLAB installation:

| MATLAB Version | matlabengine Version |
|----------------|---------------------|
| R2026a         | 26.1.x              |
| R2025b         | 25.2.x              |
| R2025a         | 25.1.x              |
| R2024b         | 24.2.x              |
| R2024a         | 24.1.x              |

To install a specific version:

```bash
uv pip install matlabengine==25.2.0  # For MATLAB R2025b
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

#### Using the .env File

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

#### Manual Configuration

If MATLAB is **not** in the default location, you can manually create `.env`:

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

**Default MATLAB locations:**

- macOS: `/Applications/MATLAB_R20XXx.app`
- Linux: `/usr/local/MATLAB/R20XXx`
- Windows: `C:\Program Files\MATLAB\R20XXx`

Replace `R20XXx` with your MATLAB version (e.g., R2024a, R2024b, R2025a, R2025b).

### Editable Installation for Development

For development, install in editable mode:

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

## Usage

### Command Line Interface (CLI)

The package provides a standalone CLI tool for running MATLAB code directly from your terminal.

#### Execute a Single Command

```bash
# Using uv run (no installation needed)
uv run matlab-cli -c "disp('Hello, MATLAB!')"

# Or if installed/activated
matlab-cli -c "disp('Hello, MATLAB!')"
```

#### Execute a MATLAB Script File

```bash
matlab-cli -f my_script.m
```

#### Interactive REPL Mode

Start an interactive MATLAB session:

```bash
matlab-cli -i
```

Then type MATLAB commands interactively:

```
matlab> x = 1:10
matlab> mean(x)
matlab> plot(x, x.^2)
matlab> exit
```

#### Verbose Output

Get detailed execution information:

```bash
matlab-cli -c "x = magic(5)" -v
```

#### CLI Help

```bash
matlab-cli --help
```

**Note:** If you haven't activated the virtual environment, prefix commands with `uv run`:
```bash
uv run matlab-cli --help
```

### Configure Claude Desktop

Add the following configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**Option 1: Using uvx (Recommended - No installation needed)**

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R20XXx.app/bin/maca64"
      }
    }
  }
}
```

Replace `DYLD_LIBRARY_PATH` with `LD_LIBRARY_PATH` on Linux, and update the path for your MATLAB version and architecture.

**Option 2: Using installed package**

After installing with `uv pip install matlab-mcp-server`:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "matlab-mcp",
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R20XXx.app/bin/maca64"
      }
    }
  }
}
```

**Option 3: Running from source**

If you've cloned the repository:

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

Replace `/absolute/path/to/matlab-mcp-server` with the actual path to your installation. Make sure you've created a `.env` file with the MATLAB library path (see Installation section).

### Available MCP Tools

The server provides 8 tools organized as multi-operation tools for token efficiency:

#### 1. `execute_matlab`

Execute MATLAB code and get the output.

**Parameters:**
- `code` (string): MATLAB code to execute

**Example:**
```
Execute: x = 1:10; y = x.^2; plot(x, y); title('Quadratic Function');
```

#### 2. `workspace`

Manage MATLAB workspace variables.

**Operations:**
- `get` - Get variable value
- `set` - Set variable value
- `list` - List all variables with details (JSON)
- `clear` - Clear one or all variables

**Parameters:**
- `op` (string): Operation to perform
- `var` (string, optional): Variable name
- `value` (any, optional): Value to set

**Examples:**
```
List workspace variables
Get variable x
Set variable data to [1, 2, 3, 4, 5]
Clear all workspace variables
```

#### 3. `figure`

Manage MATLAB figures.

**Operations:**
- `save` / `export` - Save figure to file
- `close` - Close specific or all figures

**Parameters:**
- `op` (string): Operation to perform
- `fig` (int, optional): Figure number (uses current if not specified)
- `fmt` (string, optional): Format (png, jpg, svg, pdf, fig)
- `dpi` (int, optional): DPI for raster formats (default: 150)
- `path` (string, optional): Output path (auto-generated if not specified)

**Examples:**
```
Save current figure as PNG
Export figure 1 as PDF with path /tmp/my_plot.pdf
Close all figures
```

#### 4. `data_io`

Import and export data in various formats.

**Operations:**
- `import` - Import data from file (CSV, TXT, XLSX, JSON)
- `export` - Export variable to file
- `load_mat` - Load MAT file
- `save_mat` - Save workspace to MAT file

**Parameters:**
- `op` (string): Operation to perform
- `path` (string): File path
- `var` (string, optional): Variable name
- `fmt` (string, optional): Format (auto-detected from extension if not specified)
- `variables` (array, optional): Variable names for save_mat

**Examples:**
```
Import data from /path/to/data.csv
Export variable results to /path/to/output.xlsx
Load MAT file /path/to/data.mat
Save workspace to /path/to/backup.mat
```

#### 5. `env`

Get MATLAB environment information.

**Operations:**
- `version` - Get MATLAB version and platform info
- `list_toolboxes` - List installed toolboxes
- `check_toolbox` - Check if specific toolbox is installed

**Parameters:**
- `op` (string): Operation to perform
- `name` (string, optional): Toolbox name for check_toolbox

**Examples:**
```
Get MATLAB version
List all installed toolboxes
Check if Signal Processing Toolbox is installed
```

#### 6. `get_help`

Access MATLAB documentation.

**Operations:**
- `help` - Get function documentation (usage, examples)
- `lookfor` - Search for functions by keyword
- `which` - Find function location and toolbox

**Parameters:**
- `name` (string): Function or topic name
- `op` (string, optional): Operation type (default: help)

**Examples:**
```
Get help for fft function
Search for "fourier transform" functions
Find where the plot function is located
```

#### 7. `route_intent` (Meta-tool)

Suggest appropriate tool mode based on user query.

**Parameters:**
- `query` (string): User query to analyze

**Returns:** Suggested mode and confidence score

#### 8. `select_mode` (Meta-tool)

Enable optional tool groups for the session.

**Parameters:**
- `mode` (string): Mode to enable

**Available modes:** plotting, data_io, workspace+, toolboxes, domain groups

### MCP Resources

Access MATLAB environment info and documentation:

- `docs://readme` - Getting started guide
- `docs://guide` - Complete user guide
- `matlab://env/version` - MATLAB version info
- `matlab://env/toolboxes` - Installed toolboxes (JSON)
- `matlab://session/info` - Session details (JSON)
- `matlab://workspace/snapshot` - Workspace variables (JSON)

### Exploring Tools

**For AI Assistants:**
- Use MCP Inspector to explore all tools: `npx @modelcontextprotocol/inspector uv --directory $(pwd) run --env-file .env matlab-mcp`
- Call `list_tools()` to see all available tools with schemas
- Read `src/matlab_mcp_server/server.py` for implementation details
- Check `examples/` directory for usage patterns

**For Humans:**
- Tools are listed above with descriptions
- Tool schemas are defined in `server.py:list_tools()`
- Implementation in `engine.py` has docstrings
- Examples in `examples/` directory show real usage

## Examples

See the `examples/` directory for demonstrations:

- **essentials_demo.py** - Comprehensive demo of all essential tools
- **basic_test.py** - Basic MATLAB engine usage
- **shared_session_demo.py** - GUI and shared session examples

Run the essentials demo:

```bash
uv run --env-file .env python examples/essentials_demo.py
```

## Development

### Project Structure

```
matlab-mcp-server/
├── src/
│   └── matlab_mcp_server/
│       ├── __init__.py
│       ├── server.py       # MCP server (8 tools, resources)
│       ├── cli.py          # Command-line interface
│       └── engine.py       # MATLAB engine wrapper (enhanced)
├── examples/               # Demo scripts
│   ├── essentials_demo.py # Comprehensive tool demo
│   └── ...
├── md-files/              # Internal documentation
│   ├── PLANNING.md        # Roadmap and implementation notes
│   ├── TOOLS.md           # Tool catalog
│   └── ...
├── scripts/               # Setup and utility scripts
├── temp/                  # Test scripts
├── pyproject.toml         # Project configuration
├── .env.example           # Environment template
└── README.md
```

### Running Locally

```bash
# Run MCP server
uv run --env-file .env matlab-mcp

# Run CLI
uv run --env-file .env matlab-cli -c "disp('Hello')"
```

### Testing

Test the server using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector uv --directory $(pwd) run --env-file .env matlab-mcp
```

Or run the test suite:

```bash
uv run --env-file .env python temp/test_new_tools.py
```

## Troubleshooting

### MATLAB Engine Not Found

If you get an error about MATLAB engine not being found, ensure:
1. MATLAB is properly installed
2. MATLAB Engine API for Python is installed
3. The Python version matches your MATLAB version compatibility

### Permission Issues

On macOS/Linux, you may need to set execute permissions:
```bash
chmod +x src/matlab_mcp_server/server.py
```

## Roadmap

### Phase 2: Enhanced Functionality

- File management tools (upload/download)
- Enhanced plotting support
- Toolbox-specific helpers
- Performance optimizations

### Phase 3+

- Parallel computing support
- Session persistence
- Simulink integration (separate server)
- Domain-specific tool groups (control, RF, finance)

See [PLANNING.md](md-files/PLANNING.md) for detailed roadmap.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

For development guidance:
- See [PLANNING.md](md-files/PLANNING.md) for roadmap and architecture
- See [md-files/MATLAB_MCP_GUIDE.md](md-files/MATLAB_MCP_GUIDE.md) for detailed usage guide

---

**Built with [MCP](https://modelcontextprotocol.io/) and [uv](https://github.com/astral-sh/uv)**

