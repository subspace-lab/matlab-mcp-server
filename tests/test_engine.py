"""Unit tests for MatlabEngine class."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from matlab_mcp_server.engine import (
    MatlabEngine,
    MatlabEngineError,
    MatlabNotAvailableError,
    MatlabConnectionError,
    MatlabExecutionError,
    MATLAB_AVAILABLE,
)


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineBasics:
    """Test basic MATLAB engine functionality."""

    def test_engine_initialization(self):
        """Test that engine can be initialized."""
        engine = MatlabEngine()
        assert engine._engine is None

    def test_engine_start_stop(self):
        """Test starting and stopping the engine."""
        engine = MatlabEngine()
        engine.start()
        assert engine._engine is not None
        engine.stop()
        assert engine._engine is None

    def test_engine_context_manager(self):
        """Test using engine as context manager."""
        with MatlabEngine() as engine:
            assert engine._engine is not None
        assert engine._engine is None

    def test_execute_simple_code(self):
        """Test executing simple MATLAB code."""
        engine = MatlabEngine()
        engine.start()

        result = engine.execute("x = 1 + 1;")
        assert result["error"] is None or result["error"] == ""
        assert "executed successfully" in result["output"].lower() or result["output"] == ""

        engine.stop()

    def test_execute_with_output(self):
        """Test executing code that produces output."""
        engine = MatlabEngine()
        engine.start()

        result = engine.execute("disp('Hello MATLAB')")
        assert result["error"] is None or result["error"] == ""
        assert "Hello MATLAB" in result["output"]

        engine.stop()

    def test_execute_auto_start(self):
        """Test that execute auto-starts the engine."""
        engine = MatlabEngine()
        assert engine._engine is None

        result = engine.execute("x = 1;")
        assert engine._engine is not None
        assert result["error"] is None or result["error"] == ""

        engine.stop()

    def test_execute_with_error(self):
        """Test executing code that produces an error."""
        engine = MatlabEngine()
        engine.start()

        result = engine.execute("x = undefined_variable;")
        assert result["error"] is not None
        assert "undefined" in result["error"].lower() or "not found" in result["error"].lower()

        engine.stop()

    def test_execute_empty_code(self):
        """Test executing empty code."""
        engine = MatlabEngine()
        result = engine.execute("")
        assert "No code provided" in result["error"]

    def test_execute_whitespace_only(self):
        """Test executing whitespace-only code."""
        engine = MatlabEngine()
        result = engine.execute("   \n\t  ")
        assert "No code provided" in result["error"]


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineWorkspace:
    """Test workspace operations."""

    def test_set_and_get_variable(self):
        """Test setting and getting variables."""
        engine = MatlabEngine()
        engine.start()

        test_value = [1, 2, 3, 4, 5]
        engine.set_variable("test_var", test_value)

        result = engine.get_variable("test_var")
        assert result == test_value

        engine.stop()

    def test_list_workspace(self):
        """Test listing workspace variables."""
        engine = MatlabEngine()
        engine.start()

        # Create some variables
        engine.execute("x = 1; y = 2; z = 3;")

        # List workspace
        ws = engine.list_workspace()
        assert "variables" in ws
        assert "x" in ws["variables"]
        assert "y" in ws["variables"]
        assert "z" in ws["variables"]

        engine.stop()

    def test_list_workspace_detailed(self):
        """Test detailed workspace listing."""
        engine = MatlabEngine()
        engine.start()

        engine.execute("x = magic(5);")
        ws = engine.list_workspace(detailed=True)

        # Should have detailed info about x
        assert "x" in ws

        engine.stop()

    def test_clear_specific_variable(self):
        """Test clearing a specific variable."""
        engine = MatlabEngine()
        engine.start()

        engine.execute("x = 1; y = 2;")
        engine.clear_workspace("x")

        ws = engine.list_workspace()
        assert "x" not in ws["variables"]
        assert "y" in ws["variables"]

        engine.stop()

    def test_clear_all_workspace(self):
        """Test clearing all workspace variables."""
        engine = MatlabEngine()
        engine.start()

        engine.execute("x = 1; y = 2; z = 3;")
        engine.clear_workspace()

        ws = engine.list_workspace()
        assert len(ws["variables"]) == 0

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineFigures:
    """Test figure operations."""

    @pytest.mark.skip(reason="Figure export unstable in headless mode. See docs://limitations resource.")
    def test_save_figure(self):
        """Test saving a figure.

        Skipped: Figure export can be unreliable in headless mode (MATLAB limitation).
        """
        engine = MatlabEngine()
        engine.start()

        # Create a simple plot
        engine.execute("x = 1:10; y = x.^2; plot(x, y);")

        # Save figure
        result = engine.save_figure(fmt="png")
        assert result["success"] is True
        assert result["path"] is not None
        assert Path(result["path"]).exists()

        # Cleanup
        Path(result["path"]).unlink()
        engine.close_figures()
        engine.stop()

    def test_close_figures(self):
        """Test closing figures."""
        engine = MatlabEngine()
        engine.start()

        # Create some figures
        engine.execute("figure(1); plot(1:10); figure(2); plot(10:-1:1);")

        # Close all figures
        result = engine.close_figures()
        assert result["success"] is True

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineDataIO:
    """Test data I/O operations."""

    def test_save_and_load_mat_file(self, tmp_path):
        """Test saving and loading MAT files."""
        engine = MatlabEngine()
        engine.start()

        # Create some data
        engine.execute("data1 = rand(5, 5); data2 = magic(5);")

        # Save to MAT file
        mat_file = tmp_path / "test.mat"
        result = engine.save_mat_file(str(mat_file), variables=["data1", "data2"])
        assert result["success"] is True
        assert mat_file.exists()

        # Clear workspace
        engine.clear_workspace()

        # Load MAT file
        result = engine.load_mat_file(str(mat_file))
        assert result["success"] is True

        # Verify variables were loaded
        ws = engine.list_workspace()
        assert "data1" in ws["variables"]
        assert "data2" in ws["variables"]

        engine.stop()

    def test_export_import_csv(self, tmp_path):
        """Test exporting and importing CSV data."""
        engine = MatlabEngine()
        engine.start()

        # Create a table
        engine.execute("""
            T = table([1;2;3], [4;5;6], [7;8;9], 'VariableNames', {'A', 'B', 'C'});
        """)

        # Export to CSV
        csv_file = tmp_path / "test.csv"
        result = engine.export_data("T", str(csv_file), fmt="csv")
        assert result["success"] is True
        assert csv_file.exists()

        # Import CSV
        result = engine.import_data(str(csv_file), fmt="csv")
        assert result["success"] is True
        assert result["variable"] is not None

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineEnvironment:
    """Test environment operations."""

    def test_get_version(self):
        """Test getting MATLAB version."""
        engine = MatlabEngine()
        engine.start()

        result = engine.get_version()
        assert result["output"] is not None
        assert "Version" in result["output"]

        engine.stop()

    def test_list_toolboxes(self):
        """Test listing toolboxes."""
        engine = MatlabEngine()
        engine.start()

        result = engine.list_toolboxes()
        assert result["output"] is not None
        assert "MATLAB" in result["output"]

        engine.stop()

    def test_check_toolbox(self):
        """Test checking for a toolbox."""
        engine = MatlabEngine()
        engine.start()

        # Check for MATLAB (should always be available)
        result = engine.check_toolbox("MATLAB")
        assert result["installed"] is True

        # Check for a non-existent toolbox
        result = engine.check_toolbox("NonExistentToolbox12345")
        assert result["installed"] is False

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineHelp:
    """Test help operations."""

    def test_get_help(self):
        """Test getting help for a function."""
        engine = MatlabEngine()
        engine.start()

        result = engine.get_help("sin", op="help")
        assert result["success"] is True
        assert "sin" in result["output"].lower()

        engine.stop()

    def test_get_which(self):
        """Test finding function location."""
        engine = MatlabEngine()
        engine.start()

        result = engine.get_help("sin", op="which")
        assert result["success"] is True
        assert "sin" in result["output"].lower() or "built-in" in result["output"].lower()

        engine.stop()

    def test_lookfor(self):
        """Test searching for functions."""
        engine = MatlabEngine()
        engine.start()

        result = engine.get_help("sine", op="lookfor")
        assert result["success"] is True
        # lookfor should find something related to sine

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineSharedSessions:
    """Test shared session operations."""

    def test_find_shared_sessions(self):
        """Test finding shared sessions."""
        sessions = MatlabEngine.find_shared_sessions()
        assert isinstance(sessions, tuple)

    def test_make_shared(self):
        """Test making engine shared."""
        engine = MatlabEngine()
        engine.start()

        session_name = engine.make_shared("test_session")
        assert session_name == "test_session"

        # Find the session
        sessions = MatlabEngine.find_shared_sessions()
        assert "test_session" in sessions

        engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMatlabEngineSessionManagement:
    """Test session management operations (new session tool)."""

    def test_list_sessions(self):
        """Test listing available sessions."""
        result = MatlabEngine.list_sessions()

        assert result["success"] is True
        assert "sessions" in result
        assert "count" in result
        assert isinstance(result["sessions"], list)
        assert result["count"] == len(result["sessions"])

    def test_get_current_session_no_connection(self):
        """Test getting current session when not connected."""
        engine = MatlabEngine()
        result = engine.get_current_session()

        assert result["success"] is True
        assert result["connected"] is False
        assert "No active MATLAB session" in result["message"]

    def test_get_current_session_with_connection(self):
        """Test getting current session when connected."""
        engine = MatlabEngine()
        engine.start()

        result = engine.get_current_session()

        assert result["success"] is True
        assert result["connected"] is True
        assert "is_shared" in result
        assert "session_name" in result

        engine.stop()

    def test_connect_to_nonexistent_session(self):
        """Test connecting to a non-existent session."""
        engine = MatlabEngine()
        result = engine.connect_to_session("nonexistent_session_12345")

        assert result["success"] is False
        assert "error" in result

    @pytest.mark.skip(reason="MATLAB Engine API limitation: Cannot connect from Python to another Python-created session. Connecting to GUI sessions works fine (tested manually).")
    def test_connect_to_existing_session(self):
        """Test connecting to an existing shared session.

        Note: This test is skipped due to a MATLAB Engine API limitation.
        While sessions created in Python can be shared and listed, connecting to
        them from another Python process doesn't work reliably.

        However, the intended use case (connecting to user's MATLAB GUI) works
        perfectly - see manual verification in temp/test_session_tool.py.
        """
        import time

        # First create a shared session
        engine1 = MatlabEngine()
        engine1.start()
        session_name = engine1.make_shared("test_connect_session")

        # Wait for session to be registered (MATLAB needs a moment)
        time.sleep(1)

        try:
            # Now try to connect to it from another engine
            engine2 = MatlabEngine()
            result = engine2.connect_to_session(session_name)

            assert result["success"] is True
            assert result["session_name"] == session_name
            assert "Successfully connected" in result["message"]

            # Verify connection by checking session info
            session_info = engine2.get_current_session()
            assert session_info["connected"] is True
            assert session_info["is_shared"] is True

            engine2.stop()
        finally:
            engine1.stop()

    @pytest.mark.skip(reason="MATLAB Engine API limitation: Cannot connect from Python to another Python-created session. Connecting to GUI sessions works fine (tested manually).")
    def test_session_workspace_isolation(self):
        """Test that different sessions have isolated workspaces.

        Note: This test is skipped due to a MATLAB Engine API limitation.
        While sessions created in Python can be shared and listed, connecting to
        them from another Python process doesn't work reliably.

        However, workspace isolation between GUI sessions and Python sessions
        has been verified manually and works correctly.
        """
        import time

        # Create first session with a variable
        engine1 = MatlabEngine()
        engine1.start()
        engine1.set_variable("test_var_session1", [1, 2, 3])
        session1_name = engine1.make_shared("workspace_test_session1")

        # Wait for session to be registered (MATLAB needs a moment)
        time.sleep(1)

        # Create second session
        engine2 = MatlabEngine()
        engine2.start()
        engine2.set_variable("test_var_session2", [4, 5, 6])

        try:
            # Verify session2 doesn't have session1's variable
            with pytest.raises(Exception):
                engine2.get_variable("test_var_session1")

            # Connect to session1
            result = engine2.connect_to_session(session1_name)
            assert result["success"] is True

            # Now should be able to access session1's variable
            value = engine2.get_variable("test_var_session1")
            assert value == [1, 2, 3]

            # Should NOT have session2's variable anymore
            with pytest.raises(Exception):
                engine2.get_variable("test_var_session2")

        finally:
            engine1.stop()
            engine2.stop()


class TestMatlabEngineErrors:
    """Test error handling."""

    @pytest.mark.skipif(MATLAB_AVAILABLE, reason="Test requires MATLAB to be unavailable")
    def test_matlab_not_available_error(self):
        """Test error when MATLAB is not available."""
        engine = MatlabEngine()
        with pytest.raises(MatlabNotAvailableError):
            engine.start()

    @pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
    def test_get_variable_not_exists(self):
        """Test getting a variable that doesn't exist."""
        engine = MatlabEngine()
        engine.start()

        with pytest.raises(Exception):  # MATLAB will raise an error
            engine.get_variable("nonexistent_variable_12345")

        engine.stop()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
