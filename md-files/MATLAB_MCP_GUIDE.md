# MATLAB MCP Server - Complete Guide

A comprehensive reference for the MATLAB-Python MCP server, covering installation, usage, development environment, and advanced features.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Environment Setup with UV](#environment-setup-with-uv)
3. [CLI Usage](#cli-usage)
4. [Python API](#python-api)
5. [GUI and Shared Sessions](#gui-and-shared-sessions)
6. [Key Concepts and Best Practices](#key-concepts-and-best-practices)
7. [Advanced Features](#advanced-features)
8. [Troubleshooting](#troubleshooting)
9. [Resources](#resources)

---

## Quick Start

### What We Built

A complete MATLAB MCP server with Python integration:
- ✅ MCP server for AI assistant integration (Claude Desktop)
- ✅ Standalone CLI tool for terminal use
- ✅ Enhanced engine wrapper with convenience methods
- ✅ Comprehensive exploration examples
- ✅ GUI support with shared sessions

### Installation

```bash
# Install MATLAB Engine API for Python
uv pip install /Applications/MATLAB_R2025b.app/extern/engines/python

# Install project in editable mode
uv sync
```

### First Commands

```bash
# Quick calculation
uv run matlab-cli -c "magic(3)"

# Interactive REPL
uv run matlab-cli -i

# Python script
uv run python examples/basic_test.py
```

---

## Environment Setup with UV

### Understanding `uv run`

When you run `uv run <command>`, uv automatically:

1. Uses the project's virtual environment (`.venv/`) if it exists
2. Auto-creates `.venv/` if it doesn't exist
3. Syncs dependencies from `pyproject.toml` before running
4. Uses the Python version specified in `requires-python`

**In this project:** Python 3.12.9 (from `requires-python = ">=3.10,<3.14"`)

### Why Use `uv run`?

| Method | Environment | Auto-sync | Activation | Speed |
|--------|-------------|-----------|------------|-------|
| `uv run` | Project .venv | ✅ Yes | ❌ Not needed | Fast |
| `python3` | System Python | ❌ No | ❌ Not needed | Fast |
| `.venv/bin/python` | Project .venv | ❌ No | ❌ Not needed | Fast |
| `source .venv/bin/activate` + `python` | Project .venv | ❌ No | ✅ Required | Fast |

**Benefits of `uv run`:**
- ✅ Guaranteed consistent environment
- ✅ Auto-syncs dependencies before every run
- ✅ No manual activation needed
- ✅ Works identically across different machines

### Common Scenarios

**First time running:**
```bash
$ uv run scripts/setup_matlab_env.py
# Creates .venv/ with Python 3.12.9
# Installs all dependencies
# Runs the script
```

**After changing dependencies:**
```bash
$ # Edit pyproject.toml
$ uv run scripts/setup_matlab_env.py
# Auto-syncs new dependencies
# Runs the script
```

**Regular use (already set up):**
```bash
$ uv run matlab-cli -c "disp('Hello')"
# Verifies .venv/ is up-to-date
# Runs immediately (very fast!)
```

### With Environment Variables

```bash
# Load from .env file
uv run --env-file .env matlab-cli -c "disp('Hello')"
```

Execution order:
1. Load environment variables from `.env`
2. Create/verify `.venv/` environment
3. Run command with those environment variables

### Best Practices

**✅ Recommended:**
```bash
uv run scripts/setup_matlab_env.py
uv run matlab-cli -c "magic(3)"
uv run matlab-mcp
```

**⚠️ Avoid:**
```bash
python3 scripts/setup_matlab_env.py  # Wrong Python version (3.13 vs 3.12)
```

---

## CLI Usage

### Basic Commands

```bash
# Single command execution
uv run matlab-cli -c "magic(3)"

# Execute MATLAB script file
uv run matlab-cli -f script.m

# Interactive REPL
uv run matlab-cli -i

# Verbose output (shows stdout/stderr)
uv run matlab-cli -c "x = 1:10; mean(x)" -v
```

### Advanced CLI Usage

```bash
# With environment variables
uv run --env-file .env matlab-cli -c "getenv('MYVAR')"

# Complex calculations
uv run matlab-cli -c "A = [1 2; 3 4]; inv(A)"

# Multi-line code
uv run matlab-cli -c "
x = 1:100;
y = sin(x);
mean(y)
"
```

---

## Python API

### Enhanced Engine API

```python
from matlab_mcp_server.engine import MatlabEngine
from matlab import double as matlab_double

# Basic usage with context manager
with MatlabEngine() as eng:
    # Execute code
    result = eng.execute("x = magic(5)")
    
    # Set/get variables
    eng.set_variable('x', 42.0)
    x = eng.get_variable('x')
    
    # Call functions
    result = eng.call_function('sqrt', 16.0)
    
    # Multiple outputs
    data = matlab_double([1, 2, 3, 4, 5])
    max_val, idx = eng.call_function('max', data, nargout=2)
    
    # Workspace access
    eng.workspace['y'] = 100.0
    y = eng.workspace['y']
    
    # List workspace variables
    vars = eng.list_workspace()
    
    # Clear specific variables
    eng.clear_workspace('x', 'y')
```

### Direct MATLAB Engine API

```python
import matlab.engine
from matlab import double
import io

eng = matlab.engine.start_matlab()

# Execute with output capture
out = io.StringIO()
eng.eval("disp('Hello')", nargout=0, stdout=out)
print(out.getvalue())

# Call functions
result = eng.sqrt(16.0)
M = eng.magic(3.0)

# Workspace manipulation
eng.workspace['x'] = 10.0
x = eng.workspace['x']

# Multiple outputs
max_val, max_idx = eng.max(double([1,2,3,4,5]), nargout=2)

# Async execution (for long operations)
future = eng.eval("pause(2); x = 42", nargout=0, background=True)
# Continue with other work...
result = future.result()  # Wait for completion

eng.quit()
```

### Custom MATLAB Functions

```python
from pathlib import Path

# Create custom function file
Path('/tmp/myfunction.m').write_text('''
function result = myfunction(a, b)
    result = a + b;
end
''')

# Add to path and use
eng.addpath('/tmp', nargout=0)
result = eng.myfunction(5.0, 7.0)
```

---

## GUI and Shared Sessions

### Quick Answer

**Yes, you can see the MATLAB GUI while controlling it from Python!**

Benefits:
- ✅ View the MATLAB desktop while Python executes code
- ✅ See plots and figures as they're created
- ✅ Inspect variables in the Workspace browser
- ✅ Manually interact with MATLAB while Python controls it

### Option 1: Start MATLAB with GUI from Python

```python
from matlab_mcp_server.engine import MatlabEngine

# Start with GUI visible
engine = MatlabEngine()
engine.start(desktop=True)

# Make it shared (optional but recommended for multiple connections)
engine.make_shared("MySession")

# Use normally - you'll see everything in the GUI!
engine.execute("x = magic(5)")
engine.execute("plot(1:10, (1:10).^2)")
```

### Option 2: Connect to Existing MATLAB GUI

**Step 1:** Open MATLAB GUI manually

**Step 2:** In MATLAB Command Window:
```matlab
>> matlab.engine.shareEngine('MyGUI')
```

**Step 3:** In Python:
```python
from matlab_mcp_server.engine import MatlabEngine

# Connect to the running GUI
engine = MatlabEngine.connect_to_shared('MyGUI')

# Control the GUI from Python
engine.set_variable('x', 42)
engine.execute("disp('Hello from Python!')")
```

### Finding and Managing Sessions

```python
from matlab_mcp_server.engine import MatlabEngine

# List all shared sessions
sessions = MatlabEngine.find_shared_sessions()
print(f"Found sessions: {sessions}")

# Connect to specific session
engine = MatlabEngine.connect_to_shared("MySessionName")

# Or connect to any available session
engine = MatlabEngine.connect_to_shared()
```

### Example Scripts

```bash
# Quick demo - opens GUI and runs examples
uv run python examples/quick_shared_session.py

# Interactive menu with multiple demos
uv run python examples/shared_session_demo.py
```

### Common Use Cases

#### 1. Debugging
```python
# Start with GUI for debugging
engine = MatlabEngine()
engine.start(desktop=True)
engine.make_shared("Debug")

# Run your code
engine.execute("myComplexFunction()")

# You can now:
# - See errors in MATLAB Command Window
# - Inspect variables in Workspace browser
# - Use MATLAB's debugging tools
# - Manually test fixes
```

#### 2. Interactive Visualization
```python
# Create plots you can interact with
engine = MatlabEngine()
engine.start(desktop=True)

# Generate data
import numpy as np
x = np.linspace(0, 10, 100).tolist()

engine.workspace['x'] = x
engine.execute("""
    y = sin(x);
    figure;
    plot(x, y);
    title('Interactive Plot');
    
    % You can now:
    % - Zoom in/out
    % - Rotate 3D plots
    % - Use Data Cursor
    % - Export figure manually
""")
```

#### 3. Iterative Development
```python
# Start once, keep MATLAB open
engine = MatlabEngine()
engine.start(desktop=True)
engine.make_shared("Development")

# Run experiments
engine.execute("experiment1()")

# Modify MATLAB functions in editor
# Rerun to see changes
engine.execute("experiment1()")  # Changes reflected immediately
```

#### 4. Multiple Connections (Advanced)
```python
# Python Script 1
engine1 = MatlabEngine()
engine1.start(desktop=True)
engine1.make_shared("Shared")
engine1.set_variable('data', 100)

# Python Script 2 (separate process)
engine2 = MatlabEngine.connect_to_shared("Shared")
value = engine2.get_variable('data')  # Gets 100
engine2.set_variable('data', 200)

# Back in Script 1
value = engine1.get_variable('data')  # Gets 200!
```

### Tips and Tricks

**Keep MATLAB open after Python exits:**
```python
# Don't call engine.stop() or engine.quit()
engine = MatlabEngine()
engine.start(desktop=True)
engine.make_shared("KeepOpen")

# Do work...
engine.execute("x = 1:10")

# Exit Python - MATLAB GUI stays open!
```

**Reconnect later:**
```python
# First run
engine = MatlabEngine()
engine.start(desktop=True)
engine.make_shared("MyWork")
# ... exit Python ...

# Later, reconnect
engine = MatlabEngine.connect_to_shared("MyWork")
# All variables still there!
```

**Monitor in real-time:**
```python
import time

engine = MatlabEngine()
engine.start(desktop=True)
engine.make_shared("Monitor")

# Watch updates in Command Window
for i in range(10):
    engine.set_variable('iteration', i)
    engine.execute("fprintf('Iteration %d\\n', iteration)")
    time.sleep(1)
```

### Session Management Summary

| What You Want | How To Do It |
|---------------|--------------|
| Start MATLAB with GUI | `engine.start(desktop=True)` |
| Make session shared | `engine.make_shared("name")` |
| Find sessions | `MatlabEngine.find_shared_sessions()` |
| Connect to session | `MatlabEngine.connect_to_shared("name")` |
| Keep MATLAB open | Don't call `engine.stop()` |
| See variables | Workspace browser in GUI |
| See output | Command Window in GUI |
| See plots | Figure windows appear automatically |

---

## Key Concepts and Best Practices

### 1. Data Type Conversion is Critical

```python
# ❌ Wrong - Python list won't work
eng.max([1, 2, 3, 4, 5])

# ✅ Correct - Convert to MATLAB array
from matlab import double
eng.max(double([1, 2, 3, 4, 5]))
```

**Common MATLAB types:**
- `matlab.double` - Double precision arrays
- `matlab.int32` - 32-bit integer arrays
- `matlab.logical` - Boolean arrays

### 2. Handle Multiple Outputs Properly

```python
# Get multiple return values
max_val, max_idx = eng.max(data, nargout=2)
rows, cols = eng.size(matrix, nargout=2)
eigenvals, eigenvecs = eng.eig(matrix, nargout=2)
```

### 3. Assignment Statements Need nargout=0

```python
# ✅ Correct
eng.eval("x = 10; y = 20;", nargout=0)

# ⚠️ May cause issues
eng.eval("x = 10")
```

### 4. Use Async for Long Operations

```python
# Start computation in background
future = eng.eval("result = heavy_computation()", background=True)

# Continue with other work
print("Computing in background...")

# Wait when needed
result = future.result()
```

### 5. Capture Output Properly

```python
import io

# Capture standard output
out = io.StringIO()
eng.eval("disp('Hello World')", nargout=0, stdout=out)
output = out.getvalue()
print(output)  # "Hello World\n"
```

---

## Advanced Features

### MATLAB Engine Capabilities Reference

| Feature | Method | Example |
|---------|--------|---------|
| Start engine | `matlab.engine.start_matlab()` | `eng = matlab.engine.start_matlab()` |
| Start with GUI | `start_matlab('-desktop')` | `eng = matlab.engine.start_matlab('-desktop')` |
| Execute code | `eng.eval(code, nargout=N)` | `eng.eval("x = 1:10", nargout=0)` |
| Call function | `eng.function_name(*args)` | `eng.sqrt(16.0)` |
| Get variable | `eng.workspace['var']` | `x = eng.workspace['x']` |
| Set variable | `eng.workspace['var'] = val` | `eng.workspace['x'] = 42` |
| Multiple outputs | `nargout=N` parameter | `val, idx = eng.max(data, nargout=2)` |
| Async execution | `background=True` | `fut = eng.eval(code, background=True)` |
| Output capture | `stdout=buffer` | `eng.eval(code, stdout=io.StringIO())` |
| Share session | `eng.matlab.engine.shareEngine(name)` | Share for multi-client access |
| Connect to shared | `matlab.engine.connect_matlab(name)` | Connect to existing session |

### Integration Scenarios

**1. With Claude Desktop (MCP Server):**
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "matlab": {
      "command": "uv",
      "args": ["run", "matlab-mcp"],
      "cwd": "/path/to/matlab-mcp-server"
    }
  }
}
```

**2. With NumPy/Pandas:**
```python
import numpy as np
import pandas as pd
from matlab import double

# NumPy to MATLAB
np_array = np.array([[1, 2], [3, 4]])
matlab_array = double(np_array.tolist())

# MATLAB to NumPy
matlab_result = eng.magic(3.0)
np_result = np.array(matlab_result)

# With Pandas
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
eng.workspace['data'] = double(df.values.tolist())
```

**3. Hybrid Python-MATLAB Workflows:**
```python
# Python preprocessing
data = preprocess_with_python(raw_data)

# MATLAB computation
eng.workspace['data'] = matlab.double(data.tolist())
result = eng.eval("optimized = run_optimization(data)", nargout=1)

# Python postprocessing
final_result = postprocess_with_python(np.array(result))
```

---

## Troubleshooting

### Environment Issues

**Problem:** "Wrong Python version"
```bash
$ python3 scripts/setup_matlab_env.py
# Uses system Python 3.13 instead of project Python 3.12
```
**Solution:** Always use `uv run`:
```bash
$ uv run scripts/setup_matlab_env.py
```

**Problem:** "Module not found"
```bash
$ .venv/bin/python scripts/setup_matlab_env.py
# Dependencies might be outdated
```
**Solution:** Use `uv run` to auto-sync:
```bash
$ uv run scripts/setup_matlab_env.py
```

### Shared Session Issues

**Problem:** "No shared sessions found"

**Solution:** Make sure you created a shared session:
```python
# In Python
engine.make_shared("MySession")

# Or in MATLAB
matlab.engine.shareEngine('MySession')
```

**Problem:** "Cannot connect to session"

**Solution:** Check exact session name:
```python
# List all available sessions
print(MatlabEngine.find_shared_sessions())

# Use exact name
engine = MatlabEngine.connect_to_shared("exact_name_here")
```

**Problem:** "GUI doesn't appear"

**Solution:** Use `desktop=True`:
```python
engine.start(desktop=True)  # ✓ Correct
engine.start()              # ✗ No GUI
```

### MATLAB Engine Issues

**Problem:** "Version mismatch" or cryptic connection errors

**Cause:** The `matlabengine` Python package version doesn't match your MATLAB installation.

**How version matching works:**
- The `matlabengine` package contains Python bindings that communicate with MATLAB
- At runtime, when `import matlab.engine` executes, Python loads the installed matlabengine package
- When `matlab.engine.start_matlab()` runs, it connects to your MATLAB installation via shared libraries (DYLD_LIBRARY_PATH/LD_LIBRARY_PATH)
- If major versions differ significantly, you may get connection failures or undefined behavior

**Recommended version matching:**
| MATLAB Version | matlabengine Version |
|----------------|---------------------|
| R2026a         | 26.1.x              |
| R2025b         | 25.2.x              |
| R2025a         | 25.1.x              |
| R2024b         | 24.2.x              |
| R2024a         | 24.1.x              |

**Solution:** Check your versions and reinstall if needed:

```bash
# Check your MATLAB version
matlab -batch "version"

# Check your matlabengine version
uv pip show matlabengine

# Reinstall matching version from PyPI
uv pip install matlabengine==25.2.2  # For R2025b

# OR install from MATLAB installation (recommended for exact match)
cd /Applications/MATLAB_R2025b.app/extern/engines/python
uv pip install .
```

**Note:** Minor version mismatches often work (e.g., matlabengine 25.2.x with MATLAB R2025a), but exact matches are most reliable.

---

**Problem:** Type conversion errors

**Solution:** Always convert Python data to MATLAB types:
```python
from matlab import double
eng.max(double([1, 2, 3]))  # Correct
```

**Problem:** "Too many output arguments"

**Solution:** Specify `nargout` for assignments:
```python
eng.eval("x = 10", nargout=0)  # Correct
```

### Performance Issues

**Problem:** Slow startup

**Solution:** Use shared sessions to reuse MATLAB instances:
```python
# Start once
engine.start(desktop=True)
engine.make_shared("Persistent")

# Reconnect in other scripts (much faster)
engine = MatlabEngine.connect_to_shared("Persistent")
```

---

## Resources

### Project Structure

```
matlab-mcp-server/
├── src/matlab_mcp_server/
│   ├── server.py          # MCP server implementation
│   ├── engine.py          # Enhanced MATLAB engine wrapper
│   └── cli.py             # Command-line interface
├── examples/
│   ├── basic_test.py      # Basic MATLAB concepts
│   ├── advanced_test.py   # Advanced features
│   ├── test_enhanced_engine.py
│   ├── quick_shared_session.py
│   └── shared_session_demo.py
├── scripts/
│   └── setup_matlab_env.py
├── md-files/              # Documentation
│   └── MATLAB_MCP_GUIDE.md  # This file
└── pyproject.toml
```

### Example Scripts

```bash
# Basic concepts
uv run python examples/basic_test.py

# Advanced features (async, multiple outputs, etc.)
uv run python examples/advanced_test.py

# Enhanced engine methods
uv run python examples/test_enhanced_engine.py

# Shared sessions
uv run python examples/quick_shared_session.py
uv run python examples/shared_session_demo.py
```

### What You Can Do

1. **Quick MATLAB tasks via CLI**
   ```bash
   uv run matlab-cli -c "your_matlab_code"
   ```

2. **Integrate with Python scripts**
   ```python
   from matlab_mcp_server.engine import MatlabEngine
   with MatlabEngine() as eng:
       result = eng.execute("your code")
   ```

3. **Use with Claude Desktop (MCP server)**
   - Configure in `claude_desktop_config.json`
   - Ask Claude to run MATLAB code
   - Generate and execute MATLAB scripts

4. **Build custom workflows**
   - Combine Python data processing with MATLAB analysis
   - Automate MATLAB simulations
   - Create hybrid Python-MATLAB pipelines

### Next Steps

- Explore specific MATLAB toolboxes (Optimization, Signal Processing, etc.)
- Integrate with NumPy/Pandas for data exchange
- Build production workflows with error handling
- Create custom MCP tools for specific use cases
- Optimize performance for large-scale computations
- Implement parallel processing with multiple MATLAB instances

---

## Summary

This MATLAB MCP server provides three main ways to interact with MATLAB:

1. **CLI:** Quick command-line access (`uv run matlab-cli`)
2. **Python API:** Programmatic control with enhanced wrapper
3. **MCP Server:** Integration with AI assistants like Claude

All methods support:
- ✅ Full MATLAB functionality
- ✅ GUI visualization with shared sessions
- ✅ Async execution for long operations
- ✅ Multiple output handling
- ✅ Custom function integration

Always use `uv run` for consistent, managed Python environments.

Happy computing! 🚀
