#!/usr/bin/env python3
"""Advanced MATLAB Engine exploration script.

This script demonstrates advanced MATLAB-Python interaction:
- Multiple output arguments (nargout)
- Workspace dictionary operations
- Calling custom MATLAB functions
- Background/async execution
- Data type conversions
- Working with matrices and arrays
"""

import matlab.engine
import sys
import time
from pathlib import Path

# matlab.double is a function, not a module
from matlab import double as matlab_double


def test_multiple_outputs():
    """Test functions with multiple output arguments."""
    print("=" * 60)
    print("TEST 1: Multiple Output Arguments")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # max() returns both max value and index
    print("\n1. Getting max value and index:")
    data = eng.eval("[3, 7, 2, 9, 1]")
    max_val, max_idx = eng.max(data, nargout=2)
    print(f"   Data: {data}")
    print(f"   Max value: {max_val}")
    print(f"   Max index: {max_idx}")

    # size() returns dimensions
    print("\n2. Getting matrix dimensions:")
    matrix = eng.magic(4.0)
    rows, cols = eng.size(matrix, nargout=2)
    print(f"   Matrix shape: {rows} x {cols}")

    # sort() returns sorted array and indices
    print("\n3. Sorting with indices:")
    unsorted = eng.eval("[5, 2, 8, 1, 9]")
    sorted_data, indices = eng.sort(unsorted, nargout=2)
    print(f"   Unsorted: {unsorted}")
    print(f"   Sorted: {sorted_data}")
    print(f"   Indices: {indices}")

    eng.quit()
    print()


def test_workspace_operations():
    """Test advanced workspace dictionary operations."""
    print("=" * 60)
    print("TEST 2: Workspace Dictionary Operations")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Set multiple variables
    print("\n1. Setting multiple variables:")
    eng.workspace["a"] = 10.0
    eng.workspace["b"] = 20.0
    eng.workspace["c"] = 30.0
    print("   Set a=10, b=20, c=30")

    # List all workspace variables
    print("\n2. Listing workspace variables:")
    eng.eval("whos", nargout=0)

    # Clear specific variable
    print("\n3. Clearing variable 'b':")
    eng.eval("clear b", nargout=0)
    eng.eval("whos", nargout=0)

    # Save and load workspace
    print("\n4. Saving workspace to file:")
    save_path = Path("/tmp/matlab_workspace_test.mat")
    eng.save(str(save_path), nargout=0)
    print(f"   Saved to: {save_path}")

    # Clear all
    eng.eval("clear all", nargout=0)
    print("   Cleared all variables")

    # Load workspace
    print("\n5. Loading workspace from file:")
    eng.load(str(save_path), nargout=0)
    eng.eval("whos", nargout=0)

    eng.quit()
    print()


def test_data_type_conversion():
    """Test Python-MATLAB data type conversions."""
    print("=" * 60)
    print("TEST 3: Data Type Conversions")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Python list to MATLAB array
    print("\n1. Python list to MATLAB:")
    py_list = [1, 2, 3, 4, 5]
    matlab_array = matlab_double(py_list)
    eng.workspace["arr"] = matlab_array
    result = eng.eval("arr * 2")
    print(f"   Python list: {py_list}")
    print(f"   MATLAB array * 2: {result}")

    # 2D arrays
    print("\n2. 2D Python list to MATLAB matrix:")
    py_2d = [[1, 2, 3], [4, 5, 6]]
    matlab_2d = matlab_double(py_2d)
    eng.workspace["mat"] = matlab_2d
    result = eng.transpose(eng.workspace["mat"])
    print(f"   Python 2D: {py_2d}")
    print(f"   MATLAB transpose: {result}")

    # Complex numbers
    print("\n3. Complex numbers:")
    complex_result = eng.sqrt(-1.0)
    print(f"   sqrt(-1) = {complex_result}")
    print(f"   Type: {type(complex_result)}")

    # Strings
    print("\n4. String handling:")
    eng.workspace["str"] = "Hello, MATLAB!"
    upper_str = eng.upper(eng.workspace["str"])
    print(f"   Original: Hello, MATLAB!")
    print(f"   Uppercase: {upper_str}")

    eng.quit()
    print()


def test_custom_function():
    """Test creating and calling custom MATLAB functions."""
    print("=" * 60)
    print("TEST 4: Custom MATLAB Functions")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Create a temporary MATLAB function file
    func_path = Path("/tmp/mysum.m")
    func_code = """function result = mysum(a, b)
    % Custom function to add two numbers
    result = a + b;
    fprintf('Adding %f + %f = %f\\n', a, b, result);
end
"""
    func_path.write_text(func_code)
    print(f"\n1. Created custom function: {func_path}")

    # Add path and call function
    print("\n2. Calling custom function:")
    eng.addpath("/tmp", nargout=0)
    result = eng.mysum(5.0, 7.0)
    print(f"   Result: {result}")

    # Create another function with multiple outputs
    func2_path = Path("/tmp/mystats.m")
    func2_code = """function [mean_val, std_val, min_val, max_val] = mystats(data)
    % Calculate statistics for data
    mean_val = mean(data);
    std_val = std(data);
    min_val = min(data);
    max_val = max(data);
end
"""
    func2_path.write_text(func2_code)
    print(f"\n3. Created function with multiple outputs: {func2_path}")

    print("\n4. Calling mystats:")
    data = matlab_double([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    mean_val, std_val, min_val, max_val = eng.mystats(data, nargout=4)
    print(f"   Mean: {mean_val}")
    print(f"   Std: {std_val}")
    print(f"   Min: {min_val}")
    print(f"   Max: {max_val}")

    # Cleanup
    func_path.unlink()
    func2_path.unlink()

    eng.quit()
    print()


def test_async_execution():
    """Test asynchronous/background execution."""
    print("=" * 60)
    print("TEST 5: Asynchronous Execution")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    print("\n1. Starting long-running computation in background:")
    # Start a computation that takes some time
    future = eng.eval("pause(2); result = sum(1:1000000);", nargout=0, background=True)
    print("   ✓ Computation started in background")

    print("\n2. Doing other work while MATLAB computes...")
    for i in range(3):
        print(f"   Python working... {i + 1}")
        time.sleep(0.5)

    print("\n3. Checking if computation is done:")
    print(f"   Done: {future.done()}")

    print("\n4. Waiting for result:")
    result = future.result()
    print(f"   ✓ Result received: {result}")

    # Multiple async tasks
    print("\n5. Running multiple async tasks:")
    future1 = eng.sqrt(16.0, background=True)
    future2 = eng.sqrt(25.0, background=True)
    future3 = eng.sqrt(36.0, background=True)

    results = [future1.result(), future2.result(), future3.result()]
    print(f"   Results: {results}")

    eng.quit()
    print()


def test_matrix_operations():
    """Test matrix and linear algebra operations."""
    print("=" * 60)
    print("TEST 6: Matrix and Linear Algebra")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Create matrices
    print("\n1. Matrix creation:")
    A = matlab_double([[1, 2], [3, 4]])
    B = matlab_double([[5, 6], [7, 8]])
    eng.workspace["A"] = A
    eng.workspace["B"] = B
    print(f"   A = {A}")
    print(f"   B = {B}")

    # Matrix operations
    print("\n2. Matrix multiplication:")
    C = eng.eval("A * B")
    print(f"   A * B = {C}")

    print("\n3. Matrix inverse:")
    A_inv = eng.inv(eng.workspace["A"])
    print(f"   inv(A) = {A_inv}")

    print("\n4. Eigenvalues and eigenvectors:")
    eigenvals, eigenvecs = eng.eig(eng.workspace["A"], nargout=2)
    print(f"   Eigenvalues: {eigenvals}")
    print(f"   Eigenvectors: {eigenvecs}")

    print("\n5. Determinant:")
    det_val = eng.det(eng.workspace["A"])
    print(f"   det(A) = {det_val}")

    eng.quit()
    print()


def test_plotting():
    """Test figure generation and saving."""
    print("=" * 60)
    print("TEST 7: Plotting and Figures")
    print("=" * 60)

    eng = matlab.engine.start_matlab()

    # Create a simple plot
    print("\n1. Creating a plot:")
    x = matlab_double(list(range(0, 11)))
    y = eng.eval("[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]")

    eng.figure(nargout=0)
    eng.plot(x, y, nargout=0)
    eng.title("Square Function", nargout=0)
    eng.xlabel("x", nargout=0)
    eng.ylabel("x^2", nargout=0)
    eng.grid("on", nargout=0)
    print("   ✓ Plot created")

    # Save figure
    print("\n2. Saving figure to file:")
    fig_path = "/tmp/matlab_plot.png"
    eng.saveas(eng.gcf(), fig_path, nargout=0)
    print(f"   ✓ Saved to: {fig_path}")

    # Close figure
    eng.close("all", nargout=0)

    eng.quit()
    print()


def main():
    """Run all advanced tests."""
    print("\n" + "=" * 60)
    print("MATLAB ENGINE ADVANCED EXPLORATION")
    print("=" * 60 + "\n")

    try:
        test_multiple_outputs()
        test_workspace_operations()
        test_data_type_conversion()
        test_custom_function()
        test_async_execution()
        test_matrix_operations()
        test_plotting()

        print("=" * 60)
        print("ALL ADVANCED TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nNext steps:")
        print("  - Check /tmp/matlab_plot.png for the generated plot")
        print("  - Experiment with your own MATLAB functions")
        print("  - Try integrating with NumPy and Pandas")

    except Exception as e:
        print(f"\n✗ Error during testing: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
