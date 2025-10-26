# MATLAB MCP Server - Exploration Examples

This directory contains example scripts demonstrating various ways to interact with MATLAB through Python.

## Quick Start

All examples require MATLAB Engine for Python to be installed:

```bash
cd /Users/weiqi/Documents/dropbox-weiqi-api/matlab-mcp-server
uv pip install /Applications/MATLAB_R2025b.app/extern/engines/python
```

## Example Scripts

### 1. Basic Exploration (`basic_test.py`)

Demonstrates fundamental MATLAB-Python interaction:
- Starting and stopping the MATLAB engine
- Executing simple commands
- Workspace variable access
- Calling built-in MATLAB functions
- Output redirection
- Error handling

**Run it:**
```bash
.venv/bin/python examples/basic_test.py
```

**Key concepts covered:**
- `matlab.engine.start_matlab()` - Start MATLAB
- `eng.eval()` - Execute MATLAB code
- `eng.workspace['var']` - Get/set workspace variables
- `eng.function_name()` - Call MATLAB functions directly
- Capturing stdout/stderr output

### 2. Advanced Features (`advanced_test.py`)

Demonstrates advanced MATLAB Engine capabilities:
- Multiple output arguments (`nargout`)
- Workspace dictionary operations
- Creating and calling custom MATLAB functions
- Asynchronous/background execution
- Data type conversions (Python ↔ MATLAB)
- Matrix and linear algebra operations
- Figure generation and saving

**Run it:**
```bash
.venv/bin/python examples/advanced_test.py
```

**Key concepts covered:**
- `nargout=N` - Get multiple return values
- `matlab.double()` - Convert Python lists to MATLAB arrays
- `background=True` - Async execution
- Custom function files (.m files)
- Plotting and saving figures

### 3. Enhanced Engine Test (`test_enhanced_engine.py`)

Tests the enhanced `MatlabEngine` wrapper class with convenience methods:

**Run it:**
```bash
.venv/bin/python examples/test_enhanced_engine.py
```

**Enhanced methods:**
- `engine.set_variable(name, value)` - Set workspace variable
- `engine.get_variable(name)` - Get workspace variable
- `engine.call_function(name, *args, nargout=1)` - Call any MATLAB function
- `engine.list_workspace()` - List all variables
- `engine.clear_workspace(*vars)` - Clear variables
- `engine.workspace` - Direct workspace dictionary access

### 4. MATLAB Script File (`test_script.m`)

A simple MATLAB script to demonstrate file execution via CLI.

**Run it:**
```bash
.venv/bin/matlab-cli -f examples/test_script.m
```

### 5. Real-World Test Suite (`real_world_tests.py` & `real_world_tests.m`)

**NEW!** Comprehensive test suite based on actual Stack Overflow questions, demonstrating practical MATLAB use cases and serving as regression tests for the MCP server.

**Python version (via MCP Server):**
```bash
.venv/bin/python examples/real_world_tests.py
```

**MATLAB version (native execution):**
```bash
.venv/bin/matlab-cli -f examples/real_world_tests.m
```

**Test cases included:**

1. **Vectorized Operations** - Column-by-column matrix operations using arrayfun, cellfun, and pure vectorization
2. **Function Accessibility** - Using `exist()` and `which()` to check function availability
3. **Conditional Filtering** - Complex logical indexing without loops
4. **Matrix Operations** - Linear algebra (determinant, rank, trace)
5. **Statistical Analysis** - Mean, std, min/max calculations
6. **Array Reshaping** - Multidimensional array manipulation
7. **Cell Arrays** - Structured data with cell arrays
8. **Advanced Plotting** - Multi-panel figures with subplots
9. **Data I/O** - MAT file and CSV import/export

**Expected results:**

All tests include validation logic with expected results:
- Test 1: All three vectorization methods match (tolerance < 1e-10)
- Test 2: Built-in functions detected, non-existent functions not found
- Test 3: Conditional sums computed without loops
- Test 4: magic(4) has trace=34, rank=3, det≈0
- Test 5: Random data N(0,1) has mean≈0, std≈1 (within ±0.1)
- Test 6: Reshape produces slice=[1 3 5; 2 4 6], diagonal=[1; 4]
- Test 7: Average of {95, 87, 92, 88} = 90.5
- Test 8: Figure with 4 subplots saved successfully
- Test 9: MAT and CSV round-trip with precision < 1e-10

**Use cases:**

- **Regression testing**: Run before releases to ensure MCP server functionality
- **Learning examples**: Practical patterns for common MATLAB tasks
- **Benchmarking**: Compare MCP server vs native MATLAB performance
- **Documentation**: Real-world usage patterns for users

## CLI Usage Examples

### Execute Single Commands

```bash
# Simple arithmetic
.venv/bin/matlab-cli -c "2 + 2"

# Matrix operations
.venv/bin/matlab-cli -c "x = magic(5); sum(x)"

# Statistical functions
.venv/bin/matlab-cli -c "data = [1,2,3,4,5]; fprintf('Mean: %.2f\n', mean(data))"
```

### Execute Script Files

```bash
.venv/bin/matlab-cli -f examples/test_script.m
```

### Interactive REPL Mode

```bash
.venv/bin/matlab-cli -i
```

Then type MATLAB commands:
```matlab
matlab> x = 1:10
matlab> mean(x)
matlab> plot(x, x.^2)
matlab> quit
```

### Verbose Mode

```bash
.venv/bin/matlab-cli -c "magic(3)" -v
```

## Key Learnings from Exploration

### 1. Data Type Conversion

Python lists must be converted to MATLAB arrays:
```python
from matlab import double as matlab_double

# Wrong:
eng.max([1, 2, 3, 4, 5])  # Error!

# Correct:
data = matlab_double([1, 2, 3, 4, 5])
eng.max(data)
```

### 2. Multiple Outputs

Use `nargout` parameter to get multiple return values:
```python
max_val, max_idx = eng.max(data, nargout=2)
rows, cols = eng.size(matrix, nargout=2)
```

### 3. Assignment Statements

When using `eval()` with assignments, set `nargout=0`:
```python
eng.eval("x = 10", nargout=0)  # Correct
eng.eval("x = 10")  # May cause issues
```

### 4. Async Execution

Long-running computations can run in background:
```python
future = eng.eval("pause(5); result = heavy_computation()", background=True)
# Do other work...
result = future.result()  # Wait for completion
```

### 5. Workspace Management

Access variables through workspace dictionary:
```python
eng.workspace['x'] = 42
y = eng.workspace['x']
```

### 6. Custom Functions

Create .m files and add to MATLAB path:
```python
eng.addpath('/path/to/functions', nargout=0)
result = eng.my_custom_function(arg1, arg2)
```

## Next Steps

1. **Integrate with NumPy/Pandas**: Convert between MATLAB arrays and NumPy/Pandas
2. **Advanced Plotting**: Explore more complex visualization workflows
3. **Toolbox-specific features**: Explore Simulink, Optimization, etc.
4. **Performance optimization**: Benchmark different interaction patterns
5. **Error handling**: Build robust error handling for production use

## Resources

- [MATLAB Engine API for Python Documentation](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)
- [Data Type Conversion](https://www.mathworks.com/help/matlab/matlab_external/python-to-matlab-data-type-mapping.html)
- [Async Execution](https://www.mathworks.com/help/matlab/matlab_external/call-matlab-functions-asynchronously-from-python.html)
