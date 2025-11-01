# MATLAB MCP Server - Testing Guide

This document provides a comprehensive overview of the testing strategy for the MATLAB MCP Server project.

## Table of Contents

- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Test Types](#test-types)
- [Running Tests](#running-tests)
- [Writing New Tests](#writing-new-tests)
- [Test Coverage](#test-coverage)
- [Continuous Integration](#continuous-integration)
- [Best Practices](#best-practices)

---

## Quick Start

### Running Tests

#### Using pytest Directly (Recommended)

```bash
# All pytest tests
uv run pytest

# Only unit tests
uv run pytest tests/test_engine.py -v

# Only integration tests
uv run pytest tests/test_server.py -v

# Run specific test
uv run pytest tests/test_engine.py::TestMatlabEngineBasics -v

# With coverage
uv run pytest --cov=src/matlab_mcp_server --cov-report=html
```

#### Running Real-World Tests

```bash
# Python version (via MCP Server)
uv run --env-file .env python examples/real_world_tests.py

# MATLAB version (native MATLAB)
uv run --env-file .env matlab-cli -f examples/real_world_tests.m
```

### Test Overview

| Test Type | File | Coverage | Run Time |
|-----------|------|----------|----------|
| **Unit Tests** | `tests/test_engine.py` | MatlabEngine class features | ~30 sec |
| **Integration Tests** | `tests/test_server.py` | MCP tool integration | ~45 sec |
| **End-to-End Tests** | `examples/real_world_tests.py` | 9 real-world scenarios | ~1-2 min |

### Pre-Release Checklist

```bash
# 1. Run all tests with coverage
uv run --env-file .env pytest --cov=src/matlab_mcp_server --cov-report=html

# 2. Verify real-world scenarios
uv run --env-file .env python examples/real_world_tests.py

# 3. View coverage report
open htmlcov/index.html
```

---

## Test Structure

```
matlab-mcp-server/
├── tests/                          # Unit and integration tests
│   ├── __init__.py
│   ├── test_engine.py             # Unit tests for MatlabEngine class
│   └── test_server.py             # Integration tests for MCP server tools
├── examples/                       # Example scripts and regression tests
│   ├── real_world_tests.py        # End-to-end tests (Python/MCP)
│   ├── real_world_tests.m         # End-to-end tests (pure MATLAB)
│   ├── basic_test.py              # Basic functionality examples
│   ├── advanced_test.py           # Advanced features examples
│   └── ...
└── pyproject.toml                 # Test configuration
```

## Test Types

### 1. Unit Tests (`tests/test_engine.py`)

**Purpose**: Test individual components of the MatlabEngine class in isolation.

**Coverage**:
- Basic engine lifecycle (start/stop)
- Context manager usage
- Code execution (simple, with output, with errors)
- Workspace operations (set/get/list/clear variables)
- Figure operations (save/close)
- Data I/O (MAT files, CSV)
- Environment queries (version, toolboxes)
- Help system (help, which, lookfor)
- Shared sessions

**Test Classes**:
- `TestMatlabEngineBasics` - Core functionality
- `TestMatlabEngineWorkspace` - Workspace management
- `TestMatlabEngineFigures` - Figure operations (some skipped in headless mode)
- `TestMatlabEngineDataIO` - File I/O
- `TestMatlabEngineEnvironment` - Environment info
- `TestMatlabEngineHelp` - Documentation access
- `TestMatlabEngineSharedSessions` - Session sharing (find and create)
- `TestMatlabEngineSessionManagement` - Session management (list, connect, current)
- `TestMatlabEngineErrors` - Error handling

**Run unit tests**:
```bash
uv run pytest tests/test_engine.py -v
```

### 2. Integration Tests (`tests/test_server.py`)

**Purpose**: Test the integration of MCP server tools with the MATLAB engine.

**Coverage**:
- All MCP tool operations:
  - `execute_matlab` - Code execution
  - `workspace` - Variable management
  - `figure` - Plot handling
  - `data_io` - Import/export
  - `env` - Environment queries
  - `get_help` - Documentation
- End-to-end workflows combining multiple tools

**Test Classes**:
- `TestMCPToolExecuteMATLAB` - Code execution tool
- `TestMCPToolWorkspace` - Workspace tool
- `TestMCPToolFigure` - Figure tool
- `TestMCPToolDataIO` - Data I/O tool
- `TestMCPToolEnv` - Environment tool
- `TestMCPToolGetHelp` - Help tool
- `TestMCPToolSession` - Session management tool (list, connect, current)
- `TestMCPEndToEnd` - Complete workflows

**Run integration tests**:
```bash
uv run pytest tests/test_server.py -v
```

### 3. End-to-End Tests (`examples/real_world_tests.py`)

**Purpose**: Test real-world use cases based on actual Stack Overflow questions.

**Coverage**:
1. **Vectorized Operations** - Column-by-column matrix operations
2. **Function Accessibility** - Checking function availability
3. **Conditional Filtering** - Complex logical indexing
4. **Matrix Operations** - Linear algebra (det, rank, trace)
5. **Statistical Analysis** - Mean, std, min/max
6. **Array Reshaping** - Multidimensional arrays
7. **Cell Arrays** - Structured data
8. **Advanced Plotting** - Multi-panel figures
9. **Data I/O** - MAT and CSV files

**Expected Results**: All tests include validation with expected outputs.

**Run end-to-end tests**:
```bash
# Via MCP Server
uv run --env-file .env python examples/real_world_tests.py

# Pure MATLAB (for comparison/validation)
uv run --env-file .env matlab-cli -f examples/real_world_tests.m
```

## Running Tests

### Prerequisites

1. **Install dependencies**:
```bash
cd /path/to/matlab-mcp-server
uv sync --dev
```

2. **Ensure MATLAB is installed** and the MATLAB Engine for Python is available.

### Run All Tests

```bash
# All tests
uv run pytest

# With coverage report
uv run pytest --cov=src/matlab_mcp_server --cov-report=html

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

### Run Specific Test Categories

```bash
# Only unit tests
uv run pytest tests/test_engine.py

# Only integration tests
uv run pytest tests/test_server.py

# Specific test class
uv run pytest tests/test_engine.py::TestMatlabEngineBasics

# Specific test method
uv run pytest tests/test_engine.py::TestMatlabEngineBasics::test_engine_start_stop

# Skip slow tests
uv run pytest -m "not slow"
```

### Run Real-World Tests

```bash
# Python version (via MCP)
uv run --env-file .env python examples/real_world_tests.py

# MATLAB version (native)
uv run --env-file .env matlab-cli -f examples/real_world_tests.m
```

### Test Output

**Success**:
```
====================================================================
TEST SUMMARY
====================================================================
Total Tests: 9
Passed: 9 ✅
Failed: 0 ❌
Success Rate: 100.0%
====================================================================
```

**Failure**:
```
❌ FAILED: Vectorized Operations - All methods should match
```

## Writing New Tests

### Unit Test Template

```python
@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestNewFeature:
    """Test new feature."""

    def test_feature_basic(self):
        """Test basic functionality."""
        engine = MatlabEngine()
        engine.start()

        # Test code here
        result = engine.some_new_method()
        assert result["success"] is True

        engine.stop()

    def test_feature_edge_case(self):
        """Test edge case."""
        engine = MatlabEngine()
        engine.start()

        # Test edge case
        with pytest.raises(SomeException):
            engine.some_new_method(invalid_input)

        engine.stop()
```

### Integration Test Template

```python
@pytest.mark.skipif(not MATLAB_AVAILABLE, reason="MATLAB not available")
class TestMCPToolNewTool:
    """Test new_tool MCP tool."""

    def test_new_tool_operation(self, matlab_engine):
        """Test tool operation."""
        # Use fixture for engine lifecycle
        result = matlab_engine.new_tool_method()
        assert result["success"] is True
```

### Real-World Test Template

Add to `examples/real_world_tests.py`:

```python
async def test_new_scenario(engine_manager):
    """
    Test: Description of real-world scenario
    Source: Stack Overflow link (if applicable)

    Expected: What should happen
    """
    print("\n" + "="*70)
    print("TEST N: Test Name")
    print("="*70)

    code = """
    % MATLAB code for test
    result = some_operation();
    fprintf('Result: %d\\n', result);
    """

    result = await engine_manager.execute_code(code)

    # Assertions
    assert "expected output" in result['output'], "Error message"
    print("✅ PASSED: Test passed message")
    return result
```

Add to test list in `run_all_tests()`:
```python
tests = [
    # ...existing tests...
    ("New Scenario", test_new_scenario),
]
```

## Test Coverage

### Current Coverage

```bash
# Generate coverage report
uv run pytest --cov=src/matlab_mcp_server --cov-report=term-missing

# Generate HTML report
uv run pytest --cov=src/matlab_mcp_server --cov-report=html
# Open htmlcov/index.html in browser
```

### Coverage Goals

- **Unit Tests**: >80% line coverage for core modules
- **Integration Tests**: All MCP tools should have basic tests
- **End-to-End Tests**: Cover common real-world workflows

### Uncovered Areas

Check coverage report to identify:
1. Untested code paths
2. Error handling branches
3. Edge cases

## Continuous Integration

### GitHub Actions (Recommended)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12', '3.13']
        matlab-version: ['R2024b', 'R2025a']

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install uv
      run: pip install uv

    - name: Install dependencies
      run: uv sync --dev

    - name: Run unit tests
      run: uv run pytest tests/test_engine.py -v

    - name: Run integration tests
      run: uv run pytest tests/test_server.py -v

    - name: Generate coverage report
      run: uv run pytest --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v4
```

**Note**: MATLAB installation on CI runners requires special setup or MATLAB license.

### Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest-quick
        name: Run quick tests
        entry: uv run pytest tests/ -x --tb=short
        language: system
        pass_filenames: false
        always_run: true
```

Install:
```bash
pip install pre-commit
pre-commit install
```

## Best Practices

### 1. Test Isolation

- Each test should be independent
- Clean up resources (figures, files, workspace)
- Use `tmp_path` fixture for temporary files

```python
def test_with_temp_file(tmp_path):
    test_file = tmp_path / "data.mat"
    # Use test_file
    # Automatic cleanup after test
```

### 2. Use Fixtures

```python
@pytest.fixture
def matlab_engine():
    """Provide a MATLAB engine for tests."""
    eng = MatlabEngine()
    eng.start()
    yield eng
    eng.stop()  # Cleanup
```

### 3. Skip Unstable Tests

```python
@pytest.mark.skip(reason="Figure export unstable in headless mode")
def test_figure_export(self):
    # Test code
    pass
```

### 4. Parameterized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### 5. Test Names

- Use descriptive names: `test_engine_starts_successfully`
- Follow pattern: `test_<what>_<condition>_<expected>`
- Group related tests in classes

### 6. Assertions

```python
# Good - Specific assertion
assert result["success"] is True, "Operation should succeed"

# Better - Check exact value
assert result["value"] == 42

# Best - Multiple specific checks
assert result["success"] is True
assert result["value"] == 42
assert result["message"] == "Done"
```

### 7. Error Testing

```python
def test_error_handling(self):
    """Test that errors are handled correctly."""
    with pytest.raises(MatlabExecutionError) as exc_info:
        engine.execute("invalid matlab code")

    assert "error message" in str(exc_info.value)
```

### 8. Test Documentation

```python
def test_complex_scenario(self):
    """
    Test complex data pipeline.

    This test verifies:
    1. Data import from CSV
    2. Processing with MATLAB
    3. Export to MAT file

    Expected: All operations succeed with correct data.
    """
    # Test implementation
```

## Test Maintenance

### Before Each Release

1. **Run full test suite**:
   ```bash
   uv run pytest -v
   ```

2. **Run real-world tests**:
   ```bash
   uv run python examples/real_world_tests.py
   ```

3. **Check coverage**:
   ```bash
   uv run pytest --cov=src --cov-report=term-missing
   ```

4. **Update tests** for new features

5. **Review and update** expected results if MATLAB behavior changes

### Regular Maintenance

- Review skipped tests quarterly
- Update tests when fixing bugs
- Add regression tests for reported issues
- Keep dependencies updated

## Troubleshooting

### Tests Hang

- Check for MATLAB GUI dialogs
- Ensure figures are closed
- Use timeout decorators

### Tests Fail in Headless Mode

- Skip figure export tests: `@pytest.mark.skip(reason="Headless mode")`
- Test figure operations manually

### MATLAB Not Found

- Check MATLAB installation
- Verify Python engine installation
- Set MATLAB path if needed

### Flaky Tests

- Add retries for unstable operations
- Increase timeouts
- Use more reliable assertions (ranges instead of exact values)

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)
- [Stack Overflow MATLAB Questions](https://stackoverflow.com/questions/tagged/matlab)

## Test Statistics

| Test Type | File | Test Count | Coverage |
|-----------|------|------------|----------|
| Unit Tests | `test_engine.py` | 35+ tests | MatlabEngine class |
| Integration Tests | `test_server.py` | 18+ tests | MCP tool integration |
| End-to-End Tests | `real_world_tests.py` | 9 tests | Real-world scenarios |
| **Total** | | **60+ tests** | **Comprehensive** |

### Important Notes

- Some tests are skipped in headless mode (figure operations)
- Some session tests are skipped due to MATLAB API limitations (Python-to-Python connections)
- The primary use case (connecting to MATLAB GUI) is manually verified and works correctly
- All non-skipped tests should pass on a system with MATLAB installed

## Summary

| Test Type | Location | Purpose | Run Command |
|-----------|----------|---------|-------------|
| Unit | `tests/test_engine.py` | Test individual components | `uv run pytest tests/test_engine.py` |
| Integration | `tests/test_server.py` | Test MCP tools | `uv run pytest tests/test_server.py` |
| End-to-End | `examples/real_world_tests.py` | Test real workflows | `uv run python examples/real_world_tests.py` |
| All | `tests/` | Run everything | `uv run pytest` |

**Test early, test often, and keep your tests maintainable!** 🧪
