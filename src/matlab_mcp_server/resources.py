"""MCP resources for MATLAB documentation and state."""

from mcp.server import Server
from mcp.types import TextContent, ImageContent, EmbeddedResource, Resource
from .engine import MatlabEngine
from pathlib import Path
import json


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read_text_file(path: Path) -> str:
    """Read a text file with error handling."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading {path}: {e}"


def register_resources(app: Server, matlab_engine: MatlabEngine):
    """Register all MCP resources with the server."""

    @app.list_resources()
    async def list_resources() -> list[Resource]:
        """List available resources (user-facing docs and MATLAB info)."""
        return [
            # User-facing documentation resources
            Resource(uri="docs://readme", mimeType="text/markdown", name="README - Getting Started"),
            Resource(uri="docs://guide", mimeType="text/markdown", name="User Guide"),
            Resource(uri="docs://limitations", mimeType="text/markdown", name="Known Limitations"),

            # MATLAB environment resources
            Resource(uri="matlab://env/version", mimeType="text/plain", name="MATLAB Version Info"),
            Resource(uri="matlab://env/toolboxes", mimeType="application/json", name="Installed Toolboxes (JSON)"),
            Resource(uri="matlab://session/info", mimeType="application/json", name="Session Information"),

            # Workspace resources
            Resource(uri="matlab://workspace/snapshot", mimeType="application/json", name="Workspace Snapshot (JSON)"),
        ]

    @app.read_resource()
    async def read_resource(uri: str) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Return resource contents for the given URI."""
        # ========================================================================
        # Documentation resources
        # ========================================================================
        if uri == "docs://readme":
            content = _read_text_file(PROJECT_ROOT / "README.md")
            return [TextContent(type="text", text=content)]

        if uri == "docs://guide":
            # Try to find the main user guide
            guide_path = PROJECT_ROOT / "md-files" / "MATLAB_MCP_GUIDE.md"
            if guide_path.exists():
                content = _read_text_file(guide_path)
            else:
                content = _read_text_file(PROJECT_ROOT / "README.md")
            return [TextContent(type="text", text=content)]

        if uri == "docs://limitations":
            content = """# Known Limitations

## Figure Export in Headless Mode

**Limitation:** MATLAB's `print` command requires a display for vector formats (SVG, PDF).

**Impact:**
- **PNG/JPG export:** Works perfectly in headless mode (tested and supported)
- **SVG/PDF export:** Requires GUI mode (MATLAB with display)

**Workaround:**
- Use PNG or JPG format when running in headless mode (e.g., via MCP server)
- Use SVG or PDF format only when MATLAB has access to a display

**Not a Bug:** This is a MATLAB engine limitation, not a server issue.

**Example:**
```python
# Works in headless mode
result = figure(op="save", fmt="png")

# Requires GUI mode
result = figure(op="save", fmt="svg")  # Will fail in headless mode
```

## CLI REPL Mode

**Limitation:** Multi-line input not supported in interactive REPL mode.

**Workaround:** Use the `-f` flag to execute MATLAB script files, or use single-line commands.

## Long-Running Computations

**Limitation:** No built-in way to interrupt long-running MATLAB computations.

**Workaround:** Design computations to be interruptible, or restart the MATLAB session.

---

For the complete list of known issues and technical debt, see the project's PLANNING.md file.
"""
            return [TextContent(type="text", text=content)]

        # ========================================================================
        # MATLAB environment resources
        # ========================================================================
        if uri == "matlab://env/version":
            result = matlab_engine.get_version()
            text = result.get("output") or result.get("error") or ""
            return [TextContent(type="text", text=text)]

        if uri == "matlab://env/toolboxes":
            # Return JSON format
            code = """
            tb = ver;
            toolboxes = struct();
            for i = 1:numel(tb)
                info = struct('name', tb(i).Name, 'version', tb(i).Version, 'release', tb(i).Release, 'date', tb(i).Date);
                toolboxes(i).info = info;
            end
            disp(jsonencode(toolboxes));
            """
            result = matlab_engine.execute(code)
            output = result.get("output", "{}")
            try:
                # Validate JSON
                json_data = json.loads(output.strip())
                text = json.dumps(json_data, indent=2)
            except json.JSONDecodeError:
                # Fallback to plain text if JSON parsing fails
                text = output
            return [TextContent(type="text", text=text)]

        if uri == "matlab://session/info":
            # Get session information
            code = """
            info = struct();
            info.version = version;
            info.computer = computer;
            info.hostname = getenv('HOSTNAME');
            info.user = getenv('USER');
            try
                info.pid = feature('getpid');
            catch
                info.pid = 0;
            end
            disp(jsonencode(info));
            """
            result = matlab_engine.execute(code)
            output = result.get("output", "{}")
            try:
                json_data = json.loads(output.strip())
                text = json.dumps(json_data, indent=2)
            except json.JSONDecodeError:
                text = output
            return [TextContent(type="text", text=text)]

        # ========================================================================
        # Workspace resources
        # ========================================================================
        if uri == "matlab://workspace/snapshot":
            # Return JSON format with workspace variables
            result = matlab_engine.list_workspace(detailed=True)
            text = json.dumps(result, indent=2)
            return [TextContent(type="text", text=text)]

        # ========================================================================
        # Unknown resource
        # ========================================================================
        return [TextContent(type="text", text=f"Error: Unknown resource '{uri}'")]
