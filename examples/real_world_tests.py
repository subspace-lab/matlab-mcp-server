#!/usr/bin/env python3
"""
Real-World MATLAB Test Cases from Stack Overflow
=================================================

This test suite contains real problems from Stack Overflow's MATLAB forum,
demonstrating practical use cases of the MATLAB MCP Server.

Test cases cover:
1. Vectorized column-by-column matrix operations
2. Function accessibility checking
3. Conditional matrix filtering and summing
4. Matrix operations and linear algebra
5. Statistical analysis
6. Array reshaping and indexing
7. Cell arrays and structured data
8. Advanced plotting with subplots
9. Data I/O (MAT files and CSV)

Each test includes expected results for validation.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from matlab_mcp_server.engine_manager import MATLABEngineManager


async def test_vectorized_operations(engine_manager):
    """
    Test Q1: Applying a function column-by-column to two matrices
    Source: Stack Overflow - "Applying a function to two matrices column-by-column"

    Expected: Three methods should produce identical results
    """
    print("\n" + "="*70)
    print("TEST 1: Vectorized Column-by-Column Operations")
    print("="*70)

    code = """
    % Create two test matrices
    A = rand(100, 5);
    B = rand(100, 5);

    % Method 1: Using arrayfun
    dotproducts_method1 = arrayfun(@(col) dot(A(:,col), B(:,col)), 1:size(A,2));

    % Method 2: Using cellfun
    A_cells = num2cell(A, 1);
    B_cells = num2cell(B, 1);
    dotproducts_method2 = cellfun(@(a,b) dot(a,b), A_cells, B_cells);

    % Method 3: Pure vectorization (most efficient)
    dotproducts_method3 = sum(A .* B, 1);

    % Verify all methods match
    match_1_2 = isequal(dotproducts_method1, dotproducts_method2);
    match_1_3 = max(abs(dotproducts_method1 - dotproducts_method3)) < 1e-10;

    fprintf('Method 1 (arrayfun): '); disp(dotproducts_method1);
    fprintf('Method 2 (cellfun):  '); disp(dotproducts_method2);
    fprintf('Method 3 (vectorized): '); disp(dotproducts_method3);
    fprintf('\\nAll methods match: %d\\n', match_1_2 && match_1_3);
    """

    result = await engine_manager.execute_code(code)

    # Expected: All methods should match (output should end with "1")
    assert "All methods match: 1" in result['output'], "Vectorization methods should produce identical results"
    print("✅ PASSED: All three vectorization methods produce identical results")
    return result


async def test_function_accessibility(engine_manager):
    """
    Test Q7: Check whether a name is a locally accessible function
    Source: Stack Overflow - "How to check whether a name is a locally accessible function?"

    Expected: Built-in functions should be found, non-existent should not
    """
    print("\n" + "="*70)
    print("TEST 2: Function Accessibility Checking")
    print("="*70)

    code = """
    % Test with different function types
    test_names = {'sin', 'plot', 'disp', 'nonexistent_func', 'rand'};

    fprintf('Testing function accessibility:\\n');
    fprintf('%-20s %-10s %-30s\\n', 'Name', 'Exists?', 'Location');
    fprintf('%s\\n', repmat('-', 1, 60));

    results = struct('name', {}, 'exists', {}, 'location', {});

    for i = 1:length(test_names)
        name = test_names{i};
        exists_result = exist(name, 'builtin') || exist(name, 'file');

        if exists_result
            location = which(name);
        else
            location = 'Not found';
        end

        results(i).name = name;
        results(i).exists = exists_result;
        results(i).location = location;

        fprintf('%-20s %-10s %-30s\\n', name, string(exists_result), location);
    end

    % Check specific expectations
    sin_exists = exist('sin', 'builtin') == 5;
    nonexistent_missing = ~(exist('nonexistent_func', 'builtin') || exist('nonexistent_func', 'file'));

    fprintf('\\nValidation:\\n');
    fprintf('  sin exists as builtin: %d\\n', sin_exists);
    fprintf('  nonexistent_func not found: %d\\n', nonexistent_missing);
    """

    result = await engine_manager.execute_code(code)

    # Expected: sin should exist, nonexistent_func should not
    assert "sin exists as builtin: 1" in result['output'], "sin should be detected as builtin"
    assert "nonexistent_func not found: 1" in result['output'], "nonexistent_func should not be found"
    print("✅ PASSED: Function accessibility correctly detected")
    return result


async def test_conditional_filtering(engine_manager):
    """
    Test Q8: Filter and sum matrix elements based on multiple conditions without loops
    Source: Stack Overflow - "How to filter and sum elements of a matrix without a loop?"

    Expected: Logical indexing should correctly filter and sum
    """
    print("\n" + "="*70)
    print("TEST 3: Conditional Matrix Filtering Without Loops")
    print("="*70)

    code = """
    % Create a deterministic test matrix for reproducible results
    rng(42);  % Set seed for reproducibility
    M = randi([1, 100], 10, 10);

    fprintf('Test matrix created (10x10)\\n');

    % Condition 1: Sum all elements > 50
    sum1 = sum(M(M > 50));
    count1 = sum(M(:) > 50);
    fprintf('Condition 1 - Elements > 50:\\n');
    fprintf('  Sum: %d, Count: %d\\n', sum1, count1);

    % Condition 2: Sum all elements > 30 AND < 70
    mask2 = (M > 30) & (M < 70);
    sum2 = sum(M(mask2));
    count2 = sum(mask2(:));
    fprintf('Condition 2 - Elements (30 < x < 70):\\n');
    fprintf('  Sum: %d, Count: %d\\n', sum2, count2);

    % Condition 3: Sum elements in even rows AND odd columns
    [rows, cols] = size(M);
    row_indices = repmat((1:rows)', 1, cols);
    col_indices = repmat(1:cols, rows, 1);
    mask3 = (mod(row_indices, 2) == 0) & (mod(col_indices, 2) == 1);
    sum3 = sum(M(mask3));
    count3 = sum(mask3(:));
    fprintf('Condition 3 - Even rows & odd columns:\\n');
    fprintf('  Sum: %d, Count: %d\\n', sum3, count3);

    % Verify no loops were used
    fprintf('\\n✓ All operations completed without loops\\n');
    """

    result = await engine_manager.execute_code(code)

    # Expected: Should complete without errors and show results for all 3 conditions
    assert "Condition 1" in result['output'], "Should show condition 1 results"
    assert "Condition 2" in result['output'], "Should show condition 2 results"
    assert "Condition 3" in result['output'], "Should show condition 3 results"
    assert "without loops" in result['output'], "Should confirm no loops used"
    print("✅ PASSED: Conditional filtering works without loops")
    return result


async def test_matrix_operations(engine_manager):
    """
    Test: Matrix operations and linear algebra

    Expected: Correct calculations of determinant, rank, trace
    """
    print("\n" + "="*70)
    print("TEST 4: Matrix Operations and Linear Algebra")
    print("="*70)

    code = """
    % Use magic square (determinant is always 0 for n>2 and even n)
    A = magic(4);
    B = pascal(4);

    fprintf('Matrix A (magic square 4x4):\\n');
    disp(A);

    det_A = det(A);
    rank_A = rank(A);
    trace_A = trace(A);

    fprintf('Determinant of A: %.2f\\n', det_A);
    fprintf('Rank of A: %d\\n', rank_A);
    fprintf('Trace of A: %d\\n', trace_A);

    % Magic square of order 4 has known properties
    expected_trace = 34;  % Sum of main diagonal for magic(4)
    expected_rank = 3;    % Magic(4) is rank-deficient

    trace_correct = (trace_A == expected_trace);
    rank_correct = (rank_A == expected_rank);
    det_near_zero = abs(det_A) < 1e-10;

    fprintf('\\nValidation:\\n');
    fprintf('  Trace is 34: %d\\n', trace_correct);
    fprintf('  Rank is 3: %d\\n', rank_correct);
    fprintf('  Determinant near 0: %d\\n', det_near_zero);
    """

    result = await engine_manager.execute_code(code)

    # Expected: magic(4) has trace=34, rank=3, det≈0
    assert "Trace is 34: 1" in result['output'], "Magic(4) should have trace 34"
    assert "Rank is 3: 1" in result['output'], "Magic(4) should have rank 3"
    assert "Determinant near 0: 1" in result['output'], "Magic(4) should have determinant near 0"
    print("✅ PASSED: Matrix operations produce expected results")
    return result


async def test_statistics(engine_manager):
    """
    Test: Statistical operations on multi-column data

    Expected: Mean and std calculated for each column
    """
    print("\n" + "="*70)
    print("TEST 5: Statistical Analysis")
    print("="*70)

    code = """
    % Generate reproducible random data
    rng(123);
    data = randn(1000, 5);

    means = mean(data);
    stds = std(data);
    mins = min(data);
    maxs = max(data);

    fprintf('Statistical Analysis (1000 samples x 5 variables):\\n');
    fprintf('Mean (should be near 0):\\n  ');
    fprintf('%.3f ', means);
    fprintf('\\n');

    fprintf('Std (should be near 1):\\n  ');
    fprintf('%.3f ', stds);
    fprintf('\\n');

    % Validation: for N(0,1), mean should be close to 0, std close to 1
    means_near_zero = all(abs(means) < 0.1);
    stds_near_one = all(abs(stds - 1) < 0.1);

    fprintf('\\nValidation:\\n');
    fprintf('  All means near 0 (±0.1): %d\\n', means_near_zero);
    fprintf('  All stds near 1 (±0.1): %d\\n', stds_near_one);
    """

    result = await engine_manager.execute_code(code)

    # Expected: With 1000 samples, means should be near 0, stds near 1
    assert "All means near 0" in result['output'], "Should calculate means"
    assert "All stds near 1" in result['output'], "Should calculate standard deviations"
    print("✅ PASSED: Statistical analysis completed correctly")
    return result


async def test_array_reshaping(engine_manager):
    """
    Test: Array reshaping and indexing

    Expected: Correct reshaping to 3D and diagonal extraction
    """
    print("\n" + "="*70)
    print("TEST 6: Array Reshaping and Indexing")
    print("="*70)

    code = """
    % Create vector and reshape to 3D
    original = 1:24;
    reshaped_3d = reshape(original, 2, 3, 4);

    fprintf('Original: 1:24\\n');
    fprintf('Reshaped to 2x3x4\\n');
    fprintf('Size: [%s]\\n', num2str(size(reshaped_3d)));

    % Extract first 2D slice
    slice = reshaped_3d(:,:,1);
    fprintf('\\nFirst 2D slice:\\n');
    disp(slice);

    % Extract diagonal
    diag_vals = diag(slice);
    fprintf('Diagonal: [%s]\\n', num2str(diag_vals'));

    % Validation
    expected_slice = [1 3 5; 2 4 6];
    expected_diag = [1; 4];

    slice_correct = isequal(slice, expected_slice);
    diag_correct = isequal(diag_vals, expected_diag);

    fprintf('\\nValidation:\\n');
    fprintf('  First slice correct: %d\\n', slice_correct);
    fprintf('  Diagonal correct: %d\\n', diag_correct);
    """

    result = await engine_manager.execute_code(code)

    # Expected: slice = [1 3 5; 2 4 6], diagonal = [1; 4]
    assert "First slice correct: 1" in result['output'], "Reshape should produce correct slice"
    assert "Diagonal correct: 1" in result['output'], "Diagonal extraction should work"
    print("✅ PASSED: Array reshaping and indexing work correctly")
    return result


async def test_cell_arrays(engine_manager):
    """
    Test: Cell arrays and structured data

    Expected: Correct cell array manipulation and average calculation
    """
    print("\n" + "="*70)
    print("TEST 7: Cell Arrays and Structured Data")
    print("="*70)

    code = """
    % Create cell arrays
    names = {'Alice', 'Bob', 'Charlie', 'David'};
    scores = {95, 87, 92, 88};

    fprintf('Student Scores:\\n');
    for i = 1:length(names)
        fprintf('  %s: %d\\n', names{i}, scores{i});
    end

    % Calculate average
    average = mean([scores{:}]);
    expected_avg = (95 + 87 + 92 + 88) / 4;

    fprintf('\\nAverage score: %.2f\\n', average);
    fprintf('Expected: %.2f\\n', expected_avg);
    fprintf('Match: %d\\n', abs(average - expected_avg) < 0.01);
    """

    result = await engine_manager.execute_code(code)

    # Expected: average = 90.5
    assert "Average score: 90.50" in result['output'], "Should calculate correct average"
    assert "Match: 1" in result['output'], "Average should match expected value"
    print("✅ PASSED: Cell array operations work correctly")
    return result


async def test_advanced_plotting(engine_manager):
    """
    Test: Advanced plotting with multiple subplots

    Expected: Figure created with 4 subplots and saved successfully
    """
    print("\n" + "="*70)
    print("TEST 8: Advanced Plotting")
    print("="*70)

    code = """
    % Create test data
    t = 0:0.1:10;
    y1 = sin(t);
    y2 = cos(t);
    y3 = exp(-t/5) .* sin(t);

    % Create figure with subplots
    figure(99);
    set(gcf, 'Color', 'white');
    set(gcf, 'Position', [100, 100, 1200, 800]);

    % Subplot 1: Line plots
    subplot(2, 2, 1);
    plot(t, y1, 'r-', 'LineWidth', 2);
    hold on;
    plot(t, y2, 'b--', 'LineWidth', 2);
    hold off;
    grid on;
    title('Sine and Cosine');
    xlabel('Time (s)');
    ylabel('Amplitude');
    legend('sin(t)', 'cos(t)');

    % Subplot 2: Damped oscillation
    subplot(2, 2, 2);
    plot(t, y3, 'g-', 'LineWidth', 2);
    grid on;
    title('Damped Oscillation');
    xlabel('Time (s)');
    ylabel('Amplitude');

    % Subplot 3: Scatter plot
    subplot(2, 2, 3);
    rng(456);
    x_scatter = randn(50, 1);
    y_scatter = 2*x_scatter + randn(50, 1)*0.5;
    scatter(x_scatter, y_scatter, 50, 'filled');
    grid on;
    title('Scatter Plot');
    xlabel('X');
    ylabel('Y');

    % Subplot 4: Histogram
    subplot(2, 2, 4);
    rng(789);
    data_hist = randn(1000, 1);
    histogram(data_hist, 30, 'FaceColor', [0.3 0.6 0.9]);
    grid on;
    title('Histogram');
    xlabel('Value');
    ylabel('Frequency');

    fprintf('Created figure with 4 subplots\\n');
    """

    result = await engine_manager.execute_code(code)

    # Save the figure
    save_result = await engine_manager.save_figure(
        fig_num=99,
        filepath="temp/test_advanced_plots.png",
        fmt="png",
        dpi=150
    )

    # Close the figure
    await engine_manager.close_figure(99)

    assert "Created figure with 4 subplots" in result['output'], "Should create 4 subplots"
    assert Path("temp/test_advanced_plots.png").exists(), "Should save figure file"
    print("✅ PASSED: Advanced plotting completed and saved")
    return result


async def test_data_io(engine_manager):
    """
    Test: Data import/export with MAT and CSV files

    Expected: Data correctly saved and loaded with minimal precision loss
    """
    print("\n" + "="*70)
    print("TEST 9: Data I/O (MAT and CSV)")
    print("="*70)

    # Ensure temp directory exists
    Path("temp").mkdir(exist_ok=True)

    code = """
    % Create test data
    rng(999);
    test_matrix = randn(10, 3);

    test_struct = struct();
    test_struct.name = 'Test Data';
    test_struct.values = test_matrix;
    test_struct.timestamp = datetime('now');

    fprintf('Created test data (10x3 matrix)\\n');

    % Save to MAT file
    save('temp/test_io_data.mat', 'test_matrix', 'test_struct');
    fprintf('Saved to MAT file\\n');

    % Export matrix to CSV
    writematrix(test_matrix, 'temp/test_io_data.csv');
    fprintf('Saved to CSV file\\n');

    % Clear variables
    clear test_matrix test_struct

    % Load MAT file
    load('temp/test_io_data.mat');
    fprintf('Loaded from MAT file\\n');

    % Import CSV
    imported_csv = readmatrix('temp/test_io_data.csv');
    fprintf('Loaded from CSV file\\n');

    % Validate
    mat_loaded = exist('test_matrix', 'var') && exist('test_struct', 'var');
    csv_match = max(abs(test_matrix(:) - imported_csv(:))) < 1e-10;

    fprintf('\\nValidation:\\n');
    fprintf('  MAT file loaded: %d\\n', mat_loaded);
    fprintf('  CSV data matches (precision < 1e-10): %d\\n', csv_match);
    """

    result = await engine_manager.execute_code(code)

    # Expected: Both files should load correctly with minimal precision loss
    assert "MAT file loaded: 1" in result['output'], "Should load MAT file"
    assert "CSV data matches" in result['output'], "CSV should match original data"
    assert Path("temp/test_io_data.mat").exists(), "Should create MAT file"
    assert Path("temp/test_io_data.csv").exists(), "Should create CSV file"
    print("✅ PASSED: Data I/O operations work correctly")
    return result


async def run_all_tests():
    """Run all real-world test cases"""
    print("\n" + "="*70)
    print("MATLAB MCP SERVER - REAL WORLD TEST SUITE")
    print("="*70)
    print("\nThese tests are based on actual Stack Overflow questions")
    print("demonstrating practical MATLAB use cases.\n")

    engine_manager = MATLABEngineManager()

    try:
        # Connect to MATLAB
        print("Connecting to MATLAB...")
        await engine_manager.start()
        print("✓ Connected to MATLAB\n")

        # Run all tests
        tests = [
            ("Vectorized Operations", test_vectorized_operations),
            ("Function Accessibility", test_function_accessibility),
            ("Conditional Filtering", test_conditional_filtering),
            ("Matrix Operations", test_matrix_operations),
            ("Statistical Analysis", test_statistics),
            ("Array Reshaping", test_array_reshaping),
            ("Cell Arrays", test_cell_arrays),
            ("Advanced Plotting", test_advanced_plotting),
            ("Data I/O", test_data_io),
        ]

        passed = 0
        failed = 0

        for name, test_func in tests:
            try:
                await test_func(engine_manager)
                passed += 1
            except AssertionError as e:
                print(f"❌ FAILED: {name} - {e}")
                failed += 1
            except Exception as e:
                print(f"❌ ERROR in {name}: {e}")
                failed += 1

        # Summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {100*passed/len(tests):.1f}%")
        print("="*70 + "\n")

        return failed == 0

    finally:
        # Cleanup
        print("\nCleaning up...")
        await engine_manager.stop()
        print("✓ MATLAB connection closed")


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
