#!/usr/bin/env python3
"""Basic MATLAB Engine exploration script.

This script demonstrates fundamental MATLAB-Python interaction:
- Starting and stopping the engine
- Executing simple commands
- Workspace variable access
- Calling built-in MATLAB functions
"""

import matlab.engine
import sys


def test_engine_start_stop():
    """Test starting and stopping the MATLAB engine."""
    print("=" * 60)
    print("TEST 1: Starting and Stopping MATLAB Engine")
    print("=" * 60)

    print("Starting MATLAB engine...")
    eng = matlab.engine.start_matlab()
    print("✓ MATLAB engine started successfully")

    print("Stopping MATLAB engine...")
    eng.quit()
    print("✓ MATLAB engine stopped successfully")
    print()


def test_simple_commands():
    """Test executing simple MATLAB commands."""
    print("=" * 60)
    print("TEST 2: Executing Simple Commands")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Test basic arithmetic
    print("\n1. Basic arithmetic: 2 + 2")
    result = eng.eval("2 + 2")
    print(f"   Result: {result}")

    # Test built-in functions
    print("\n2. Square root: sqrt(16)")
    result = eng.sqrt(16.0)
    print(f"   Result: {result}")

    # Test matrix operations
    print("\n3. Magic square: magic(3)")
    result = eng.magic(3.0)
    print(f"   Result:\n{result}")

    eng.quit()
    print()


def test_workspace_variables():
    """Test workspace variable access."""
    print("=" * 60)
    print("TEST 3: Workspace Variable Access")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Set variables from Python
    print("\n1. Setting variables from Python:")
    eng.workspace["x"] = 10.0
    eng.workspace["y"] = 5.0
    print(f"   Set x = 10.0")
    print(f"   Set y = 5.0")

    # Use variables in MATLAB
    print("\n2. Using variables in MATLAB (x + y):")
    result = eng.eval("x + y")
    print(f"   Result: {result}")

    # Get variables back to Python
    print("\n3. Getting variables from MATLAB workspace:")
    x_value = eng.workspace["x"]
    y_value = eng.workspace["y"]
    print(f"   x = {x_value}")
    print(f"   y = {y_value}")

    # Create variable in MATLAB, retrieve in Python
    print("\n4. Create in MATLAB, retrieve in Python:")
    eng.eval("z = x * y", nargout=0)
    z_value = eng.workspace["z"]
    print(f"   z = x * y = {z_value}")

    eng.quit()
    print()


def test_builtin_functions():
    """Test calling various built-in MATLAB functions."""
    print("=" * 60)
    print("TEST 4: Built-in MATLAB Functions")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Mathematical functions
    print("\n1. Mathematical functions:")
    print(f"   sin(pi/2) = {eng.sin(eng.eval('pi/2'))}")
    print(f"   cos(0) = {eng.cos(0.0)}")
    print(f"   exp(1) = {eng.exp(1.0)}")

    # Array functions
    print("\n2. Array functions:")
    result = eng.linspace(0.0, 10.0, 5.0)
    print(f"   linspace(0, 10, 5) = {result}")

    # Statistical functions
    print("\n3. Statistical functions:")
    data = eng.eval("[1, 2, 3, 4, 5]")
    print(f"   Data: {data}")
    print(f"   mean = {eng.mean(data)}")
    print(f"   std = {eng.std(data)}")
    print(f"   sum = {eng.sum(data)}")

    eng.quit()
    print()


def test_output_redirection():
    """Test capturing MATLAB output."""
    print("=" * 60)
    print("TEST 5: Output Redirection")
    print("=" * 60)

    import io

    eng = matlab.engine.start_matlab()

    # Capture stdout
    print("\n1. Capturing output from disp():")
    output = io.StringIO()
    eng.disp("Hello from MATLAB!", nargout=0, stdout=output)
    captured = output.getvalue()
    print(f"   Captured: {captured.strip()}")

    # Execute code with output
    print("\n2. Capturing eval() output:")
    output = io.StringIO()
    eng.eval("fprintf('The answer is %d\\n', 42)", nargout=0, stdout=output)
    captured = output.getvalue()
    print(f"   Captured: {captured.strip()}")

    eng.quit()
    print()


def test_error_handling():
    """Test error handling."""
    print("=" * 60)
    print("TEST 6: Error Handling")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    print("\n1. Testing syntax error:")
    try:
        eng.eval("invalid syntax here")
    except (matlab.engine.MatlabExecutionError, SyntaxError) as e:
        print(f"   ✓ Caught error: {str(e)[:60]}...")

    print("\n2. Testing undefined variable:")
    try:
        eng.eval("undefined_variable")
    except (matlab.engine.MatlabExecutionError, Exception) as e:
        print(f"   ✓ Caught error: {str(e)[:60]}...")

    print("\n3. Testing invalid function call:")
    try:
        result = eng.sqrt(-1.0)  # Will return complex number, not error
        print(f"   sqrt(-1) = {result} (complex number)")
    except Exception as e:
        print(f"   Error: {e}")

    eng.quit()
    print()


def main():
    """Run all basic tests."""
    print("\n" + "=" * 60)
    print("MATLAB ENGINE BASIC EXPLORATION")
    print("=" * 60 + "\n")

    try:
        test_engine_start_stop()
        test_simple_commands()
        test_workspace_variables()
        test_builtin_functions()
        test_output_redirection()
        test_error_handling()

        print("=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during testing: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
