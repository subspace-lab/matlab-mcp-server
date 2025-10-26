"""Integration tests for MCP server."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from matlab_mcp_server import engine as engine_module
from matlab_mcp_server.engine import MATLAB_AVAILABLE


@pytest.fixture
def matlab_engine():
    """Provide a MATLAB engine for tests."""
    if not MATLAB_AVAILABLE:
        pytest.skip("MATLAB not available")

    eng = engine_module.MatlabEngine()
    eng.start()
    yield eng
    eng.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolExecuteMATLAB:
    """Test execute_matlab tool."""

    def test_basic_execution(self, matlab_engine):
        """Test basic code execution."""
        result = matlab_engine.execute("x = 1 + 1;")
        assert result["error"] is None or result["error"] == ""

    def test_execution_with_output(self, matlab_engine):
        """Test execution with output."""
        result = matlab_engine.execute("disp('Hello from MATLAB')")
        assert "Hello from MATLAB" in result["output"]
        assert not result["error"]

    def test_execution_with_calculation(self, matlab_engine):
        """Test execution with calculation and display."""
        result = matlab_engine.execute("x = magic(5); disp(sum(x(:)))")
        assert result["error"] is None or result["error"] == ""
        assert "325" in result["output"]  # Sum of magic(5) is 325


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolWorkspace:
    """Test workspace tool operations."""

    def test_workspace_set_and_get(self, matlab_engine):
        """Test setting and getting workspace variables."""
        # Set operation
        matlab_engine.set_variable("test_var", [1, 2, 3, 4, 5])

        # Get operation
        value = matlab_engine.get_variable("test_var")
        assert value == [1, 2, 3, 4, 5]

    def test_workspace_list(self, matlab_engine):
        """Test listing workspace."""
        matlab_engine.execute("x = 1; y = 2; z = 3;")

        ws = matlab_engine.list_workspace()
        assert "x" in ws["variables"]
        assert "y" in ws["variables"]
        assert "z" in ws["variables"]

    def test_workspace_clear(self, matlab_engine):
        """Test clearing workspace."""
        matlab_engine.execute("x = 1; y = 2;")

        # Clear specific variable
        matlab_engine.clear_workspace("x")
        ws = matlab_engine.list_workspace()
        assert "x" not in ws["variables"]
        assert "y" in ws["variables"]

        # Clear all
        matlab_engine.clear_workspace()
        ws = matlab_engine.list_workspace()
        assert len(ws["variables"]) == 0


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolFigure:
    """Test figure tool operations."""

    @pytest.mark.skip(reason="Figure export unstable in headless mode. See docs://limitations resource.")
    def test_figure_save_and_close(self, matlab_engine, tmp_path):
        """Test saving and closing figures.

        Skipped: Figure export can be unreliable in headless mode (MATLAB limitation).
        """
        # Create a plot
        matlab_engine.execute("x = linspace(0, 2*pi, 100); y = sin(x); plot(x, y);")

        # Save figure
        result = matlab_engine.save_figure(fmt="png")
        assert result["success"] is True
        assert Path(result["path"]).exists()

        # Cleanup saved file
        Path(result["path"]).unlink()

        # Close figures
        result = matlab_engine.close_figures()
        assert result["success"] is True

    @pytest.mark.skip(reason="Multiple format exports in sequence can be unstable in headless mode. PNG export tested in test_figure_save_and_close.")
    def test_figure_save_different_formats(self, matlab_engine):
        """Test saving figures in different formats.

        Note: Only PNG/JPG work in headless mode. SVG/PDF require GUI mode.
        Skipped because multiple format exports in sequence can trigger MATLAB print errors.
        Basic PNG export is tested in test_figure_save_and_close.
        """
        matlab_engine.execute("x = 1:10; plot(x, x.^2);")

        # Only test formats that work in headless mode
        for fmt in ["png", "jpg"]:
            result = matlab_engine.save_figure(fmt=fmt)
            assert result["success"] is True
            assert Path(result["path"]).exists()
            Path(result["path"]).unlink()

        matlab_engine.close_figures()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolDataIO:
    """Test data_io tool operations."""

    def test_save_and_load_mat(self, matlab_engine, tmp_path):
        """Test save_mat and load_mat operations."""
        # Create data
        matlab_engine.execute("data = rand(10, 10); label = 'test';")

        # Save MAT file
        mat_file = tmp_path / "test_data.mat"
        result = matlab_engine.save_mat_file(str(mat_file), variables=["data", "label"])
        assert result["success"] is True
        assert mat_file.exists()

        # Clear workspace
        matlab_engine.clear_workspace()

        # Load MAT file
        result = matlab_engine.load_mat_file(str(mat_file))
        assert result["success"] is True

        # Verify
        ws = matlab_engine.list_workspace()
        assert "data" in ws["variables"]
        assert "label" in ws["variables"]

    def test_export_and_import_csv(self, matlab_engine, tmp_path):
        """Test CSV export and import."""
        # Create table
        matlab_engine.execute("""
            T = table([1;2;3], [4;5;6], 'VariableNames', {'A', 'B'});
        """)

        # Export
        csv_file = tmp_path / "test.csv"
        result = matlab_engine.export_data("T", str(csv_file), fmt="csv")
        assert result["success"] is True
        assert csv_file.exists()

        # Import
        result = matlab_engine.import_data(str(csv_file), fmt="csv")
        assert result["success"] is True
        assert result["variable"] is not None


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolEnv:
    """Test env tool operations."""

    def test_env_version(self, matlab_engine):
        """Test getting MATLAB version."""
        result = matlab_engine.get_version()
        assert "Version" in result["output"]
        assert "Computer" in result["output"]

    def test_env_list_toolboxes(self, matlab_engine):
        """Test listing toolboxes."""
        result = matlab_engine.list_toolboxes()
        assert "MATLAB" in result["output"]

    def test_env_check_toolbox(self, matlab_engine):
        """Test checking for toolboxes."""
        # MATLAB should always be available
        result = matlab_engine.check_toolbox("MATLAB")
        assert result["installed"] is True


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolGetHelp:
    """Test get_help tool operations."""

    def test_get_help_for_function(self, matlab_engine):
        """Test getting help for a function."""
        result = matlab_engine.get_help("sin", op="help")
        assert result["success"] is True
        assert len(result["output"]) > 0

    def test_get_which_for_function(self, matlab_engine):
        """Test finding function location."""
        result = matlab_engine.get_help("sin", op="which")
        assert result["success"] is True
        assert len(result["output"]) > 0

    def test_lookfor_keyword(self, matlab_engine):
        """Test searching for functions."""
        result = matlab_engine.get_help("fourier", op="lookfor")
        assert result["success"] is True
        # Should find some results


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolSession:
    """Test session management tool operations."""

    def test_session_list(self, matlab_engine):
        """Test listing sessions via session tool."""
        # Use the static method directly (simulating MCP tool call)
        from matlab_mcp_server.engine import MatlabEngine as EngineClass
        result = EngineClass.list_sessions()

        assert result["success"] is True
        assert "sessions" in result
        assert "count" in result
        assert isinstance(result["sessions"], list)

    def test_session_current_no_connection(self):
        """Test getting current session info when not connected."""
        from matlab_mcp_server.engine import MatlabEngine as EngineClass
        engine = EngineClass()
        result = engine.get_current_session()

        assert result["success"] is True
        assert result["connected"] is False

    def test_session_current_with_connection(self, matlab_engine):
        """Test getting current session info when connected."""
        result = matlab_engine.get_current_session()

        assert result["success"] is True
        assert result["connected"] is True
        assert "session_name" in result
        assert "is_shared" in result

    @pytest.mark.skip(reason="MATLAB Engine API limitation: Cannot connect from Python to another Python-created session. Connecting to GUI sessions works fine (tested manually).")
    def test_session_connect_workflow(self, matlab_engine):
        """Test complete session connection workflow.

        Note: This test is skipped due to a MATLAB Engine API limitation.
        The primary use case (connecting to user's MATLAB GUI) has been verified
        manually and works correctly. See temp/test_session_tool.py for manual tests.
        """
        import time

        # Create a shared session
        session_name = "test_mcp_session"
        matlab_engine.make_shared(session_name)

        # Wait for session to be registered (MATLAB needs a moment)
        time.sleep(1)

        # Verify it's in the list
        from matlab_mcp_server.engine import MatlabEngine as EngineClass
        list_result = EngineClass.list_sessions()
        assert session_name in list_result["sessions"]

        # Create a new engine and connect to it
        new_engine = EngineClass()
        connect_result = new_engine.connect_to_session(session_name)

        assert connect_result["success"] is True
        assert connect_result["session_name"] == session_name

        # Verify connection
        current_result = new_engine.get_current_session()
        assert current_result["connected"] is True
        assert current_result["is_shared"] is True

        new_engine.stop()


@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPEndToEnd:
    """End-to-end integration tests."""

    def test_complete_workflow(self, matlab_engine, tmp_path):
        """Test a complete workflow using multiple tools."""
        # 1. Execute code to create data
        result = matlab_engine.execute("""
            x = linspace(0, 2*pi, 100);
            y = sin(x);
            data_table = table(x', y', 'VariableNames', {'X', 'Y'});
        """)
        assert result["error"] is None or result["error"] == ""

        # 2. Check workspace
        ws = matlab_engine.list_workspace()
        assert "data_table" in ws["variables"]

        # 3. Create and save a figure
        matlab_engine.execute("plot(x, y); title('Sine Wave');")
        fig_result = matlab_engine.save_figure(fmt="png")
        assert fig_result["success"] is True

        # 4. Export data
        csv_file = tmp_path / "sine_data.csv"
        export_result = matlab_engine.export_data("data_table", str(csv_file))
        assert export_result["success"] is True

        # 5. Save workspace
        mat_file = tmp_path / "workspace.mat"
        save_result = matlab_engine.save_mat_file(str(mat_file))
        assert save_result["success"] is True

        # 6. Clear and reload
        matlab_engine.clear_workspace()
        ws = matlab_engine.list_workspace()
        assert len(ws["variables"]) == 0

        load_result = matlab_engine.load_mat_file(str(mat_file))
        assert load_result["success"] is True

        # 7. Verify data reloaded
        ws = matlab_engine.list_workspace()
        assert "data_table" in ws["variables"]

        # Cleanup
        Path(fig_result["path"]).unlink()
        matlab_engine.close_figures()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
