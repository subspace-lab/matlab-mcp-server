"""MCP server implementation for MATLAB integration."""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from .engine import MatlabEngine
from .tools import register_tools
from .resources import register_resources


# Initialize the MCP server
app = Server("matlab-mcp-server")

# Global MATLAB engine instance
matlab_engine = MatlabEngine()

# Enabled tool groups (for mode management)
enabled_modes = set(["essentials"])

# Register tools and resources
register_tools(app, matlab_engine, enabled_modes)
register_resources(app, matlab_engine)


async def main():
    """Run the MCP server."""
    try:
        # Start MATLAB engine
        matlab_engine.start()

        # Run the server
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream, write_stream, app.create_initialization_options()
            )
    finally:
        # Clean up
        matlab_engine.stop()


def run():
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
