"""MCP tools for MATLAB operations."""

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from typing import Any
from .engine import MatlabEngine
import json


def register_tools(app: Server, matlab_engine: MatlabEngine, enabled_modes: set):
    """Register all MCP tools with the server."""

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        """List available MATLAB tools based on enabled modes."""
        tools = []

        # Essential tools (always available)
        tools.extend([
            Tool(
                name="execute_matlab",
                description="Execute MATLAB code and return output/errors",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "MATLAB code to execute"}
                    },
                    "required": ["code"],
                },
            ),
            Tool(
                name="workspace",
                description="Workspace get/set/list/clear operations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "op": {
                            "type": "string",
                            "enum": ["get", "set", "list", "clear"],
                            "description": "Operation: get|set|list|clear"
                        },
                        "var": {
                            "type": "string",
                            "description": "Variable name (for get/set operations)"
                        },
                        "value": {
                            "description": "Value to set (for set operation)"
                        },
                        "type_hint": {
                            "type": "string",
                            "description": "Type hint for value conversion (optional)"
                        },
                    },
                    "required": ["op"],
                },
            ),
            Tool(
                name="figure",
                description="Save/export/close MATLAB figures",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "op": {
                            "type": "string",
                            "enum": ["save", "export", "close"],
                            "description": "Operation: save|export|close"
                        },
                        "fig": {
                            "type": "integer",
                            "description": "Figure number (optional, uses current figure if not specified)"
                        },
                        "fmt": {
                            "type": "string",
                            "enum": ["png", "jpg", "svg", "pdf", "fig"],
                            "description": "Output format"
                        },
                        "dpi": {
                            "type": "integer",
                            "description": "DPI for raster formats (default: 150)"
                        },
                        "path": {
                            "type": "string",
                            "description": "Output path (auto-generated if not specified)"
                        },
                    },
                    "required": ["op"],
                },
            ),
            Tool(
                name="data_io",
                description="Import/export data and load/save MAT files",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "op": {
                            "type": "string",
                            "enum": ["import", "export", "load_mat", "save_mat"],
                            "description": "Operation: import|export|load_mat|save_mat"
                        },
                        "path": {
                            "type": "string",
                            "description": "File path"
                        },
                        "var": {
                            "type": "string",
                            "description": "Variable name (for export, or specific var for load_mat)"
                        },
                        "fmt": {
                            "type": "string",
                            "description": "File format (csv, txt, xlsx, json, etc.)"
                        },
                        "variables": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of variable names (for save_mat)"
                        },
                    },
                    "required": ["op", "path"],
                },
            ),
            Tool(
                name="env",
                description="Get MATLAB version and toolbox information",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "op": {
                            "type": "string",
                            "enum": ["version", "list_toolboxes", "check_toolbox"],
                            "description": "Operation: version|list_toolboxes|check_toolbox"
                        },
                        "name": {
                            "type": "string",
                            "description": "Toolbox name (for check_toolbox)"
                        },
                    },
                    "required": ["op"],
                },
            ),
            Tool(
                name="get_help",
                description="Retrieve MATLAB documentation or search for functions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Function or topic name"
                        },
                        "op": {
                            "type": "string",
                            "enum": ["help", "lookfor", "which"],
                            "description": "Operation: help (usage/examples) | lookfor (keyword search) | which (path/toolbox info)",
                            "default": "help"
                        },
                    },
                    "required": ["name"],
                },
            ),
        ])

        # Meta-tools for mode management
        tools.extend([
            Tool(
                name="route_intent",
                description="Lightweight routing to choose appropriate tool mode/group",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "User query to route"
                        }
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="select_mode",
                description="Enable a tool group for the session (plotting, data_io, workspace+, toolboxes, domain groups)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "mode": {
                            "type": "string",
                            "description": "Mode to enable"
                        }
                    },
                    "required": ["mode"],
                },
            ),
            Tool(
                name="session",
                description="Manage MATLAB session connections (list, connect, switch sessions)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "op": {
                            "type": "string",
                            "enum": ["list", "connect", "current"],
                            "description": "Operation: list (show available sessions) | connect (connect to a session) | current (get current session info)"
                        },
                        "session_name": {
                            "type": "string",
                            "description": "Session name (required for 'connect' operation)"
                        }
                    },
                    "required": ["op"],
                },
            ),
        ])

        return tools

    @app.call_tool()
    async def call_tool(
        name: str, arguments: Any
    ) -> list[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls."""

        # ========================================================================
        # execute_matlab
        # ========================================================================
        if name == "execute_matlab":
            code = arguments.get("code")
            if not code:
                return [TextContent(type="text", text="Error: No code provided")]

            result = matlab_engine.execute(code)

            if result["error"]:
                response = f"Error executing MATLAB code:\n\n{result['error']}"
            else:
                response = f"MATLAB Output:\n\n{result['output']}"

            return [TextContent(type="text", text=response)]

        # ========================================================================
        # workspace
        # ========================================================================
        elif name == "workspace":
            op = arguments.get("op")

            if op == "list":
                result = matlab_engine.list_workspace(detailed=True)
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            elif op == "get":
                var = arguments.get("var")
                if not var:
                    return [TextContent(type="text", text="Error: Variable name required for 'get' operation")]

                try:
                    value = matlab_engine.get_variable(var)
                    # Convert to string representation
                    response = f"Variable '{var}': {value}"
                    return [TextContent(type="text", text=response)]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error getting variable '{var}': {str(e)}")]

            elif op == "set":
                var = arguments.get("var")
                value = arguments.get("value")
                if not var:
                    return [TextContent(type="text", text="Error: Variable name required for 'set' operation")]
                if value is None:
                    return [TextContent(type="text", text="Error: Value required for 'set' operation")]

                try:
                    matlab_engine.set_variable(var, value)
                    return [TextContent(type="text", text=f"Successfully set variable '{var}'")]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error setting variable '{var}': {str(e)}")]

            elif op == "clear":
                var = arguments.get("var")
                try:
                    if var:
                        matlab_engine.clear_workspace(var)
                        return [TextContent(type="text", text=f"Cleared variable '{var}'")]
                    else:
                        matlab_engine.clear_workspace()
                        return [TextContent(type="text", text="Cleared all workspace variables")]
                except Exception as e:
                    return [TextContent(type="text", text=f"Error clearing workspace: {str(e)}")]

            else:
                return [TextContent(type="text", text=f"Error: Unknown operation '{op}'")]

        # ========================================================================
        # figure
        # ========================================================================
        elif name == "figure":
            op = arguments.get("op")

            if op in ["save", "export"]:
                fig_num = arguments.get("fig")
                fmt = arguments.get("fmt", "png")
                dpi = arguments.get("dpi", 150)
                path = arguments.get("path")

                result = matlab_engine.save_figure(fig_num=fig_num, path=path, fmt=fmt, dpi=dpi)

                if result["success"]:
                    return [TextContent(type="text", text=f"Figure saved to {result['path']}")]
                else:
                    return [TextContent(type="text", text=f"Error saving figure: {result.get('error', 'Unknown error')}")]

            elif op == "close":
                fig_nums = arguments.get("fig")
                if fig_nums:
                    if not isinstance(fig_nums, list):
                        fig_nums = [fig_nums]
                else:
                    fig_nums = None

                result = matlab_engine.close_figures(fig_nums=fig_nums)

                if result["success"]:
                    if fig_nums:
                        return [TextContent(type="text", text=f"Closed figure(s) {fig_nums}")]
                    else:
                        return [TextContent(type="text", text="Closed all figures")]
                else:
                    return [TextContent(type="text", text=f"Error closing figures: {result.get('error', 'Unknown error')}")]

            else:
                return [TextContent(type="text", text=f"Error: Unknown operation '{op}'")]

        # ========================================================================
        # data_io
        # ========================================================================
        elif name == "data_io":
            op = arguments.get("op")
            path = arguments.get("path")

            if op == "import":
                fmt = arguments.get("fmt")
                result = matlab_engine.import_data(path, fmt=fmt)

                if result["success"]:
                    return [TextContent(type="text", text=f"Data imported from {path}")]
                else:
                    return [TextContent(type="text", text=f"Error importing data: {result.get('error', 'Unknown error')}")]

            elif op == "export":
                var = arguments.get("var")
                fmt = arguments.get("fmt")

                if not var:
                    return [TextContent(type="text", text="Error: Variable name required for 'export' operation")]

                result = matlab_engine.export_data(var, path, fmt=fmt)

                if result["success"]:
                    return [TextContent(type="text", text=f"Variable '{var}' exported to {path}")]
                else:
                    return [TextContent(type="text", text=f"Error exporting data: {result.get('error', 'Unknown error')}")]

            elif op == "load_mat":
                var = arguments.get("var")
                result = matlab_engine.load_mat_file(path, var=var)

                if result["success"]:
                    return [TextContent(type="text", text=f"MAT file loaded from {path}")]
                else:
                    return [TextContent(type="text", text=f"Error loading MAT file: {result.get('error', 'Unknown error')}")]

            elif op == "save_mat":
                variables = arguments.get("variables")
                result = matlab_engine.save_mat_file(path, variables=variables)

                if result["success"]:
                    return [TextContent(type="text", text=f"Workspace saved to {path}")]
                else:
                    return [TextContent(type="text", text=f"Error saving MAT file: {result.get('error', 'Unknown error')}")]

            else:
                return [TextContent(type="text", text=f"Error: Unknown operation '{op}'")]

        # ========================================================================
        # env
        # ========================================================================
        elif name == "env":
            op = arguments.get("op")

            if op == "version":
                result = matlab_engine.get_version()
                if result["output"]:
                    return [TextContent(type="text", text=result["output"])]
                else:
                    return [TextContent(type="text", text=f"Error getting version: {result.get('error', 'Unknown error')}")]

            elif op == "list_toolboxes":
                result = matlab_engine.list_toolboxes()
                if result["output"]:
                    return [TextContent(type="text", text=result["output"])]
                else:
                    return [TextContent(type="text", text=f"Error listing toolboxes: {result.get('error', 'Unknown error')}")]

            elif op == "check_toolbox":
                name = arguments.get("name")
                if not name:
                    return [TextContent(type="text", text="Error: Toolbox name required for 'check_toolbox' operation")]

                result = matlab_engine.check_toolbox(name)
                if result["output"]:
                    return [TextContent(type="text", text=result["output"])]
                else:
                    return [TextContent(type="text", text=f"Error checking toolbox: {result.get('error', 'Unknown error')}")]

            else:
                return [TextContent(type="text", text=f"Error: Unknown operation '{op}'")]

        # ========================================================================
        # get_help
        # ========================================================================
        elif name == "get_help":
            topic_name = arguments.get("name")
            op = arguments.get("op", "help")

            if not topic_name:
                return [TextContent(type="text", text="Error: Name required for 'get_help'")]

            result = matlab_engine.get_help(topic_name, op=op)

            if result["output"]:
                return [TextContent(type="text", text=result["output"])]
            else:
                return [TextContent(type="text", text=f"Error getting help: {result.get('error', 'Unknown error')}")]

        # ========================================================================
        # route_intent
        # ========================================================================
        elif name == "route_intent":
            query = arguments.get("query", "").lower()

            # Simple keyword-based routing
            keywords = {
                "plot": "plotting",
                "figure": "plotting",
                "chart": "plotting",
                "graph": "plotting",
                "import": "data_io",
                "export": "data_io",
                "load": "data_io",
                "save": "data_io",
                "workspace": "workspace+",
                "variable": "workspace+",
                "toolbox": "toolboxes",
            }

            for keyword, mode in keywords.items():
                if keyword in query:
                    return [TextContent(type="text", text=json.dumps({
                        "mode": mode,
                        "confidence": 0.8,
                        "reason": f"Detected keyword '{keyword}'"
                    }, indent=2))]

            # Default to essentials
            return [TextContent(type="text", text=json.dumps({
                "mode": "essentials",
                "confidence": 0.5,
                "reason": "No specific keywords detected"
            }, indent=2))]

        # ========================================================================
        # select_mode
        # ========================================================================
        elif name == "select_mode":
            mode = arguments.get("mode")
            if mode:
                enabled_modes.add(mode)
                return [TextContent(type="text", text=f"Mode '{mode}' enabled for this session")]
            else:
                return [TextContent(type="text", text="Error: Mode name required")]

        # ========================================================================
        # session
        # ========================================================================
        elif name == "session":
            op = arguments.get("op")

            if op == "list":
                result = MatlabEngine.list_sessions()
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            elif op == "connect":
                session_name = arguments.get("session_name")
                if not session_name:
                    return [TextContent(type="text", text=json.dumps({
                        "success": False,
                        "error": "session_name is required for connect operation"
                    }, indent=2))]

                result = matlab_engine.connect_to_session(session_name)
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            elif op == "current":
                result = matlab_engine.get_current_session()
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            else:
                return [TextContent(type="text", text=json.dumps({
                    "success": False,
                    "error": f"Unknown session operation: {op}"
                }, indent=2))]

        # ========================================================================
        # Unknown tool
        # ========================================================================
        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]
