"""MATLAB engine wrapper for executing code and managing sessions."""

import io
import json
import logging
from typing import Optional, Dict, Any, TYPE_CHECKING, List, Union
from pathlib import Path
import sys

try:
    import matlab.engine

    MATLAB_AVAILABLE = True
except ImportError:
    MATLAB_AVAILABLE = False
    if TYPE_CHECKING:
        import matlab.engine

# Set up logging with a default configuration
logger = logging.getLogger(__name__)

# Configure logging if not already configured
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class MatlabEngineError(Exception):
    """Base exception for MATLAB engine errors."""
    pass


class MatlabNotAvailableError(MatlabEngineError):
    """Raised when MATLAB engine is not available."""
    pass


class MatlabExecutionError(MatlabEngineError):
    """Raised when MATLAB code execution fails."""
    pass


class MatlabConnectionError(MatlabEngineError):
    """Raised when connection to MATLAB fails."""
    pass


class MatlabEngine:
    """Manages MATLAB engine sessions and code execution."""

    def __init__(self):
        """Initialize the MATLAB engine wrapper."""
        self._engine: Optional[matlab.engine.MatlabEngine] = None
        self._is_shared: bool = False
        self._session_name: Optional[str] = None

    def start(self, desktop: bool = False) -> None:
        """
        Start the MATLAB engine.

        Args:
            desktop: If True, starts MATLAB with GUI visible

        Raises:
            MatlabNotAvailableError: If MATLAB engine is not installed
            MatlabConnectionError: If MATLAB fails to start
        """
        if not MATLAB_AVAILABLE:
            logger.error("MATLAB Engine for Python is not installed")
            raise MatlabNotAvailableError(
                "MATLAB Engine for Python is not installed.\n\n"
                "Install from PyPI:\n"
                "  uv pip install matlabengine\n\n"
                "Or install all dependencies:\n"
                "  uv sync\n\n"
                "Then configure library paths (if needed):\n"
                "  uv run scripts/setup_matlab_env.py\n\n"
                "For more details, see README.md"
            )

        if self._engine is None:
            try:
                logger.info(f"Starting MATLAB engine (desktop={desktop})...")
                if desktop:
                    self._engine = matlab.engine.start_matlab("-desktop")
                else:
                    self._engine = matlab.engine.start_matlab()
                logger.info("MATLAB engine started successfully")
            except Exception as e:
                logger.error(f"Failed to start MATLAB engine: {e}")
                raise MatlabConnectionError(f"Failed to start MATLAB: {e}") from e
        else:
            logger.debug("MATLAB engine already running")

    def stop(self) -> None:
        """
        Stop the MATLAB engine.

        Raises:
            MatlabEngineError: If stopping the engine fails
        """
        if self._engine is not None:
            try:
                logger.info("Stopping MATLAB engine...")
                self._engine.quit()
                self._engine = None
                logger.info("MATLAB engine stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping MATLAB engine: {e}")
                self._engine = None  # Force cleanup
                raise MatlabEngineError(f"Failed to stop MATLAB: {e}") from e
        else:
            logger.debug("MATLAB engine not running, nothing to stop")

    def execute(self, code: str) -> Dict[str, Any]:
        """
        Execute MATLAB code and return results.

        Args:
            code: MATLAB code to execute

        Returns:
            Dictionary with 'output' and 'error' keys

        Raises:
            MatlabEngineError: If execution fails catastrophically
        """
        if not code or not code.strip():
            logger.warning("Empty code provided to execute()")
            return {"output": "", "error": "No code provided"}

        if self._engine is None:
            logger.debug("Engine not started, starting now...")
            self.start()

        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        try:
            logger.debug(f"Executing MATLAB code ({len(code)} chars)...")
            self._engine.eval(
                code, nargout=0, stdout=output_buffer, stderr=error_buffer
            )

            output = output_buffer.getvalue()
            error = error_buffer.getvalue()

            if error:
                logger.warning(f"MATLAB execution produced stderr: {error[:100]}")
            else:
                logger.debug("MATLAB code executed successfully")

            return {
                "output": output if output else "Code executed successfully.",
                "error": error if error else None,
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"MATLAB execution error: {error_msg[:200]}")

            if (
                MATLAB_AVAILABLE
                and hasattr(matlab.engine, "MatlabExecutionError")
                and isinstance(e, matlab.engine.MatlabExecutionError)
            ):
                return {"output": "", "error": error_msg}

            # Re-raise for catastrophic errors, return error dict for code errors
            if "connection" in error_msg.lower() or "engine" in error_msg.lower():
                raise MatlabEngineError(f"Engine error: {error_msg}") from e

            return {"output": "", "error": f"Unexpected error: {error_msg}"}

        finally:
            output_buffer.close()
            error_buffer.close()

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def get_variable(self, name: str) -> Any:
        """
        Get a variable from the MATLAB workspace.

        Args:
            name: Variable name

        Returns:
            Variable value
        """
        if self._engine is None:
            self.start()
        return self._engine.workspace[name]

    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a variable in the MATLAB workspace.

        Args:
            name: Variable name
            value: Variable value
        """
        if self._engine is None:
            self.start()
        self._engine.workspace[name] = value

    def call_function(self, name: str, *args, nargout: int = 1) -> Any:
        """
        Call a MATLAB function with arguments.

        Args:
            name: Function name
            *args: Function arguments
            nargout: Number of output arguments

        Returns:
            Function result(s)
        """
        if self._engine is None:
            self.start()
        func = getattr(self._engine, name)
        return func(*args, nargout=nargout)

    def list_workspace(self, detailed: bool = False) -> Dict[str, Any]:
        """
        List all variables in the MATLAB workspace.

        Args:
            detailed: If True, returns detailed info (type, size, bytes)

        Returns:
            Dictionary with variable information
        """
        if self._engine is None:
            self.start()

        if detailed:
            # Use whos for detailed info
            code = """
            ws = evalin('base', 'whos');
            result = struct();
            for i = 1:length(ws)
                info = struct();
                info.class = ws(i).class;
                info.size = ws(i).size;
                info.bytes = ws(i).bytes;
                result.(ws(i).name) = info;
            end
            disp(jsonencode(result));
            """
            result = self.execute(code)
            output = result.get("output", "{}")
            try:
                # Parse JSON from output
                import json
                return json.loads(output.strip())
            except json.JSONDecodeError:
                logger.warning("Failed to parse workspace JSON, falling back to text")
                return {"error": "Failed to parse workspace info", "raw": output}
        else:
            # Simple listing with who
            output_buffer = io.StringIO()
            self._engine.who(nargout=0, stdout=output_buffer)
            output = output_buffer.getvalue()
            output_buffer.close()
            return {"variables": output.strip().split()}

    def clear_workspace(self, *variables: str) -> None:
        """
        Clear variables from the MATLAB workspace.

        Args:
            *variables: Variable names to clear. If empty, clears all.
        """
        if self._engine is None:
            self.start()

        if variables:
            for var in variables:
                self._engine.eval(f"clear {var}", nargout=0)
        else:
            self._engine.eval("clear", nargout=0)

    @property
    def workspace(self) -> Dict[str, Any]:
        """
        Access the MATLAB workspace as a dictionary.

        Returns:
            Workspace dictionary
        """
        if self._engine is None:
            self.start()
        return self._engine.workspace

    def make_shared(self, name: Optional[str] = None) -> str:
        """
        Convert the current session to a shared session.

        Shared sessions can be connected to from the MATLAB GUI or other
        Python processes.

        Args:
            name: Optional name for the shared session. If None, MATLAB
                  will assign a default name like 'MATLAB_<PID>'

        Returns:
            The name of the shared session
        """
        if self._engine is None:
            self.start()

        if name:
            self._engine.eval(f"matlab.engine.shareEngine('{name}')", nargout=0)
            return name
        else:
            self._engine.eval("matlab.engine.shareEngine", nargout=0)
            # Get the assigned name
            session_name = self._engine.eval("matlab.engine.engineName")
            return session_name

    @staticmethod
    def find_shared_sessions() -> tuple:
        """
        Find all shared MATLAB sessions running on the local machine.

        Returns:
            Tuple of session names
        """
        if not MATLAB_AVAILABLE:
            raise ImportError("MATLAB Engine for Python is not installed")

        return matlab.engine.find_matlab()

    @staticmethod
    def connect_to_shared(name: Optional[str] = None) -> "MatlabEngine":
        """
        Connect to an existing shared MATLAB session.

        Args:
            name: Name of the session to connect to. If None, connects to
                  the first available session or starts a new shared one.

        Returns:
            MatlabEngine instance connected to the shared session
        """
        if not MATLAB_AVAILABLE:
            raise ImportError("MATLAB Engine for Python is not installed")

        engine = MatlabEngine()
        if name:
            engine._engine = matlab.engine.connect_matlab(name)
        else:
            engine._engine = matlab.engine.connect_matlab()
        return engine

    # ========================================================================
    # Figure operations
    # ========================================================================

    def save_figure(
        self,
        fig_num: Optional[int] = None,
        path: Optional[str] = None,
        fmt: str = "png",
        dpi: int = 150,
    ) -> Dict[str, Any]:
        """
        Save a MATLAB figure to file.

        Args:
            fig_num: Figure number (None for current figure)
            path: Output path (auto-generated if None)
            fmt: Format (png, jpg, svg, pdf, fig)
            dpi: DPI for raster formats

        Returns:
            Dictionary with status and path
        """
        if self._engine is None:
            self.start()

        # Generate default path if not provided
        if path is None:
            import tempfile
            suffix = f".{fmt}"
            fd, path = tempfile.mkstemp(suffix=suffix, prefix="matlab_fig_")
            import os
            os.close(fd)

        # Build the save command
        if fig_num is not None:
            fig_handle = f"figure({fig_num})"
        else:
            fig_handle = "gcf"

        if fmt in ["png", "jpg", "jpeg"]:
            code = f"print({fig_handle}, '{path}', '-d{fmt}', '-r{dpi}');"
        elif fmt in ["svg", "pdf"]:
            code = f"print({fig_handle}, '{path}', '-d{fmt}');"
        elif fmt == "fig":
            code = f"saveas({fig_handle}, '{path}', 'fig');"
        else:
            return {"success": False, "error": f"Unsupported format: {fmt}"}

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"], "path": None}
        else:
            return {"success": True, "path": path, "format": fmt}

    def close_figures(self, fig_nums: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Close MATLAB figures.

        Args:
            fig_nums: List of figure numbers to close (None for all)

        Returns:
            Dictionary with status
        """
        if self._engine is None:
            self.start()

        if fig_nums is None:
            code = "close all;"
        else:
            code = "; ".join([f"close({n})" for n in fig_nums]) + ";"

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"]}
        else:
            return {"success": True}

    # ========================================================================
    # Data I/O operations
    # ========================================================================

    def load_mat_file(self, path: str, var: Optional[str] = None) -> Dict[str, Any]:
        """
        Load data from a MAT file.

        Args:
            path: Path to MAT file
            var: Specific variable to load (None for all)

        Returns:
            Dictionary with status and loaded variables
        """
        if self._engine is None:
            self.start()

        if var:
            code = f"load('{path}', '{var}');"
        else:
            code = f"load('{path}');"

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"]}
        else:
            return {"success": True, "message": f"Loaded from {path}"}

    def save_mat_file(
        self, path: str, variables: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Save workspace variables to a MAT file.

        Args:
            path: Output path
            variables: List of variable names (None for all)

        Returns:
            Dictionary with status
        """
        if self._engine is None:
            self.start()

        if variables:
            vars_str = "', '".join(variables)
            code = f"save('{path}', '{vars_str}');"
        else:
            code = f"save('{path}');"

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"]}
        else:
            return {"success": True, "path": path}

    def import_data(self, path: str, fmt: Optional[str] = None) -> Dict[str, Any]:
        """
        Import data from various file formats.

        Args:
            path: File path
            fmt: Format hint (csv, txt, xlsx, json, etc.)

        Returns:
            Dictionary with status and variable name
        """
        if self._engine is None:
            self.start()

        # Auto-detect format from extension if not provided
        if fmt is None:
            import os
            _, ext = os.path.splitext(path)
            fmt = ext.lstrip(".")

        # Generate variable name from filename
        import os
        var_name = "imported_" + os.path.splitext(os.path.basename(path))[0]
        var_name = var_name.replace("-", "_").replace(" ", "_")

        # Build import command based on format
        if fmt in ["csv", "txt"]:
            code = f"{var_name} = readtable('{path}');"
        elif fmt == "xlsx":
            code = f"{var_name} = readtable('{path}');"
        elif fmt == "json":
            code = f"{var_name} = jsondecode(fileread('{path}'));"
        else:
            return {"success": False, "error": f"Unsupported format: {fmt}"}

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"]}
        else:
            return {"success": True, "variable": var_name, "format": fmt}

    def export_data(
        self, var: str, path: str, fmt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Export a variable to file.

        Args:
            var: Variable name
            path: Output path
            fmt: Format (csv, txt, xlsx, json)

        Returns:
            Dictionary with status
        """
        if self._engine is None:
            self.start()

        # Auto-detect format from extension if not provided
        if fmt is None:
            import os
            _, ext = os.path.splitext(path)
            fmt = ext.lstrip(".")

        # Build export command based on format
        if fmt in ["csv", "txt"]:
            code = f"writetable({var}, '{path}');"
        elif fmt == "xlsx":
            code = f"writetable({var}, '{path}');"
        elif fmt == "json":
            code = f"fid = fopen('{path}', 'w'); fprintf(fid, '%s', jsonencode({var})); fclose(fid);"
        else:
            return {"success": False, "error": f"Unsupported format: {fmt}"}

        result = self.execute(code)
        if result.get("error"):
            return {"success": False, "error": result["error"]}
        else:
            return {"success": True, "path": path, "format": fmt}

    # ========================================================================
    # Environment and toolbox operations
    # ========================================================================

    def get_version(self) -> Dict[str, Any]:
        """
        Get MATLAB version and platform info.

        Returns:
            Dictionary with version info
        """
        if self._engine is None:
            self.start()

        code = """
        v = version;
        c = computer;
        fprintf('Version: %s\\nComputer: %s\\n', v, c);
        """
        result = self.execute(code)
        return {
            "output": result.get("output", ""),
            "error": result.get("error"),
        }

    def list_toolboxes(self) -> Dict[str, Any]:
        """
        List installed MATLAB toolboxes.

        Returns:
            Dictionary with toolbox info
        """
        if self._engine is None:
            self.start()

        code = """
        tb = ver;
        for i = 1:numel(tb)
            fprintf('%s %s\\n', tb(i).Name, tb(i).Version);
        end
        """
        result = self.execute(code)
        return {
            "output": result.get("output", ""),
            "error": result.get("error"),
        }

    def check_toolbox(self, name: str) -> Dict[str, Any]:
        """
        Check if a toolbox is installed.

        Args:
            name: Toolbox name to check

        Returns:
            Dictionary with availability status
        """
        if self._engine is None:
            self.start()

        code = f"""
        tb = ver('{name}');
        if isempty(tb)
            fprintf('Toolbox not found: {name}\\n');
        else
            fprintf('Toolbox available: %s %s\\n', tb.Name, tb.Version);
        end
        """
        result = self.execute(code)
        installed = "not found" not in result.get("output", "").lower()
        return {
            "installed": installed,
            "output": result.get("output", ""),
            "error": result.get("error"),
        }

    # ========================================================================
    # Help and documentation operations
    # ========================================================================

    def get_help(
        self, name: str, op: str = "help"
    ) -> Dict[str, Any]:
        """
        Get MATLAB help for a function or topic.

        Args:
            name: Function or topic name
            op: Operation type (help, lookfor, which)

        Returns:
            Dictionary with help text
        """
        if self._engine is None:
            self.start()

        if op == "help":
            code = f"help {name}"
        elif op == "lookfor":
            code = f"lookfor {name}"
        elif op == "which":
            code = f"which -all {name}"
        else:
            return {"success": False, "error": f"Unknown help operation: {op}"}

        result = self.execute(code)
        return {
            "success": not bool(result.get("error")),
            "output": result.get("output", ""),
            "error": result.get("error"),
        }

    # ========================================================================
    # Session management operations
    # ========================================================================

    @staticmethod
    def list_sessions() -> Dict[str, Any]:
        """
        List all available shared MATLAB sessions.

        Returns:
            Dictionary with session list and count
        """
        if not MATLAB_AVAILABLE:
            return {
                "success": False,
                "error": "MATLAB Engine for Python is not installed",
            }

        try:
            sessions = matlab.engine.find_matlab()
            return {
                "success": True,
                "sessions": list(sessions),
                "count": len(sessions),
            }
        except Exception as e:
            logger.error(f"Error listing sessions: {e}")
            return {"success": False, "error": str(e)}

    def connect_to_session(self, session_name: str) -> Dict[str, Any]:
        """
        Connect to an existing shared MATLAB session.

        Args:
            session_name: Name of the shared session to connect to

        Returns:
            Dictionary with connection status
        """
        if not MATLAB_AVAILABLE:
            return {
                "success": False,
                "error": "MATLAB Engine for Python is not installed",
            }

        try:
            # Store current session info in case we need to rollback
            old_engine = self._engine
            old_is_shared = self._is_shared
            old_session_name = self._session_name

            # Try to connect to the shared session
            logger.info(f"Connecting to shared session '{session_name}'...")
            new_engine = matlab.engine.connect_matlab(session_name)

            # Connection successful, update state
            if old_engine is not None and not old_is_shared:
                # Stop the old engine only if it was created by us
                try:
                    old_engine.quit()
                except Exception as e:
                    logger.warning(f"Failed to stop old engine: {e}")

            self._engine = new_engine
            self._is_shared = True
            self._session_name = session_name

            logger.info(f"Successfully connected to '{session_name}'")
            return {
                "success": True,
                "session_name": session_name,
                "message": f"Successfully connected to '{session_name}'",
            }

        except Exception as e:
            logger.error(f"Failed to connect to session '{session_name}': {e}")
            # Connection failed, preserve current session
            return {
                "success": False,
                "error": f"Failed to connect to '{session_name}': {str(e)}",
                "current_session": self._session_name,
            }

    def get_current_session(self) -> Dict[str, Any]:
        """
        Get information about the current MATLAB session.

        Returns:
            Dictionary with current session info
        """
        if self._engine is None:
            return {
                "success": True,
                "connected": False,
                "message": "No active MATLAB session",
            }

        try:
            # Try to get session name from MATLAB
            try:
                engine_name = self._engine.eval("matlab.engine.engineName", nargout=1)
            except:
                engine_name = None

            # Get MATLAB version
            try:
                version_result = self.get_version()
                version_info = version_result.get("output", "Unknown")
            except:
                version_info = "Unknown"

            return {
                "success": True,
                "connected": True,
                "is_shared": self._is_shared,
                "session_name": engine_name or self._session_name or "unnamed",
                "version": version_info.split('\n')[0] if version_info else "Unknown",
            }

        except Exception as e:
            logger.error(f"Error getting session info: {e}")
            return {
                "success": False,
                "error": str(e),
            }
