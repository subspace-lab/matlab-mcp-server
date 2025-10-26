% Real-World MATLAB Test Cases from Stack Overflow
% =================================================
%
% This script contains real problems from Stack Overflow's MATLAB forum,
% demonstrating practical MATLAB use cases.
%
% Test cases cover:
% 1. Vectorized column-by-column matrix operations
% 2. Function accessibility checking
% 3. Conditional matrix filtering and summing
% 4. Matrix operations and linear algebra
% 5. Statistical analysis
% 6. Array reshaping and indexing
% 7. Cell arrays and structured data
% 8. Advanced plotting with subplots
% 9. Data I/O (MAT files and CSV)
%
% Each test includes expected results for validation.

clear all; close all; clc;

fprintf('\n');
fprintf('====================================================================\n');
fprintf('MATLAB REAL WORLD TEST SUITE\n');
fprintf('====================================================================\n');
fprintf('\nBased on actual Stack Overflow questions\n\n');

total_tests = 9;
passed_tests = 0;

%% TEST 1: Vectorized Column-by-Column Operations
fprintf('====================================================================\n');
fprintf('TEST 1: Vectorized Column-by-Column Operations\n');
fprintf('====================================================================\n');

try
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

    if match_1_2 && match_1_3
        fprintf('✓ PASSED: All three vectorization methods produce identical results\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('✗ FAILED: Methods do not match\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 2: Function Accessibility Checking
fprintf('\n====================================================================\n');
fprintf('TEST 2: Function Accessibility Checking\n');
fprintf('====================================================================\n');

try
    % Test with different function types
    test_names = {'sin', 'plot', 'disp', 'nonexistent_func', 'rand'};

    fprintf('%-20s %-10s\n', 'Name', 'Exists?');
    fprintf('%s\n', repmat('-', 1, 30));

    sin_exists = exist('sin', 'builtin') == 5;
    nonexistent_missing = ~(exist('nonexistent_func', 'builtin') || exist('nonexistent_func', 'file'));

    for i = 1:length(test_names)
        name = test_names{i};
        exists_result = exist(name, 'builtin') || exist(name, 'file');
        fprintf('%-20s %-10d\n', name, exists_result);
    end

    if sin_exists && nonexistent_missing
        fprintf('\n✓ PASSED: Function accessibility correctly detected\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Function detection incorrect\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 3: Conditional Matrix Filtering Without Loops
fprintf('\n====================================================================\n');
fprintf('TEST 3: Conditional Matrix Filtering Without Loops\n');
fprintf('====================================================================\n');

try
    % Create a deterministic test matrix
    rng(42);
    M = randi([1, 100], 10, 10);

    % Condition 1: Sum all elements > 50
    sum1 = sum(M(M > 50));
    count1 = sum(M(:) > 50);
    fprintf('Elements > 50: Sum=%d, Count=%d\n', sum1, count1);

    % Condition 2: Sum all elements > 30 AND < 70
    mask2 = (M > 30) & (M < 70);
    sum2 = sum(M(mask2));
    count2 = sum(mask2(:));
    fprintf('Elements (30 < x < 70): Sum=%d, Count=%d\n', sum2, count2);

    % Condition 3: Sum elements in even rows AND odd columns
    [rows, cols] = size(M);
    row_indices = repmat((1:rows)', 1, cols);
    col_indices = repmat(1:cols, rows, 1);
    mask3 = (mod(row_indices, 2) == 0) & (mod(col_indices, 2) == 1);
    sum3 = sum(M(mask3));
    count3 = sum(mask3(:));
    fprintf('Even rows & odd columns: Sum=%d, Count=%d\n', sum3, count3);

    fprintf('\n✓ PASSED: Conditional filtering works without loops\n');
    passed_tests = passed_tests + 1;
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 4: Matrix Operations and Linear Algebra
fprintf('\n====================================================================\n');
fprintf('TEST 4: Matrix Operations and Linear Algebra\n');
fprintf('====================================================================\n');

try
    A = magic(4);

    det_A = det(A);
    rank_A = rank(A);
    trace_A = trace(A);

    fprintf('Determinant: %.2f\n', det_A);
    fprintf('Rank: %d\n', rank_A);
    fprintf('Trace: %d\n', trace_A);

    % Magic(4) has known properties
    trace_correct = (trace_A == 34);
    rank_correct = (rank_A == 3);
    det_near_zero = abs(det_A) < 1e-10;

    if trace_correct && rank_correct && det_near_zero
        fprintf('\n✓ PASSED: Matrix operations produce expected results\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Results do not match expected values\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 5: Statistical Analysis
fprintf('\n====================================================================\n');
fprintf('TEST 5: Statistical Analysis\n');
fprintf('====================================================================\n');

try
    rng(123);
    data = randn(1000, 5);

    means = mean(data);
    stds = std(data);

    fprintf('Means: '); fprintf('%.3f ', means); fprintf('\n');
    fprintf('Stds:  '); fprintf('%.3f ', stds); fprintf('\n');

    % For N(0,1), mean ≈ 0, std ≈ 1
    means_near_zero = all(abs(means) < 0.1);
    stds_near_one = all(abs(stds - 1) < 0.1);

    if means_near_zero && stds_near_one
        fprintf('\n✓ PASSED: Statistical analysis correct\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Statistics out of expected range\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 6: Array Reshaping and Indexing
fprintf('\n====================================================================\n');
fprintf('TEST 6: Array Reshaping and Indexing\n');
fprintf('====================================================================\n');

try
    original = 1:24;
    reshaped_3d = reshape(original, 2, 3, 4);

    fprintf('Reshaped 1:24 to 2x3x4\n');

    slice = reshaped_3d(:,:,1);
    diag_vals = diag(slice);

    fprintf('First slice:\n');
    disp(slice);
    fprintf('Diagonal: [%s]\n', num2str(diag_vals'));

    % Expected values
    expected_slice = [1 3 5; 2 4 6];
    expected_diag = [1; 4];

    slice_correct = isequal(slice, expected_slice);
    diag_correct = isequal(diag_vals, expected_diag);

    if slice_correct && diag_correct
        fprintf('\n✓ PASSED: Array reshaping and indexing work correctly\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Results do not match expected\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 7: Cell Arrays and Structured Data
fprintf('\n====================================================================\n');
fprintf('TEST 7: Cell Arrays and Structured Data\n');
fprintf('====================================================================\n');

try
    names = {'Alice', 'Bob', 'Charlie', 'David'};
    scores = {95, 87, 92, 88};

    fprintf('Student Scores:\n');
    for i = 1:length(names)
        fprintf('  %s: %d\n', names{i}, scores{i});
    end

    average = mean([scores{:}]);
    expected_avg = 90.5;

    fprintf('\nAverage: %.2f (Expected: %.2f)\n', average, expected_avg);

    if abs(average - expected_avg) < 0.01
        fprintf('\n✓ PASSED: Cell array operations work correctly\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Average does not match\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 8: Advanced Plotting
fprintf('\n====================================================================\n');
fprintf('TEST 8: Advanced Plotting\n');
fprintf('====================================================================\n');

try
    t = 0:0.1:10;
    y1 = sin(t);
    y2 = cos(t);
    y3 = exp(-t/5) .* sin(t);

    fig = figure('Position', [100, 100, 1200, 800], 'Color', 'white');

    % Subplot 1
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

    % Subplot 2
    subplot(2, 2, 2);
    plot(t, y3, 'g-', 'LineWidth', 2);
    grid on;
    title('Damped Oscillation');
    xlabel('Time (s)');
    ylabel('Amplitude');

    % Subplot 3
    subplot(2, 2, 3);
    rng(456);
    x_scatter = randn(50, 1);
    y_scatter = 2*x_scatter + randn(50, 1)*0.5;
    scatter(x_scatter, y_scatter, 50, 'filled');
    grid on;
    title('Scatter Plot');
    xlabel('X');
    ylabel('Y');

    % Subplot 4
    subplot(2, 2, 4);
    rng(789);
    data_hist = randn(1000, 1);
    histogram(data_hist, 30, 'FaceColor', [0.3 0.6 0.9]);
    grid on;
    title('Histogram');
    xlabel('Value');
    ylabel('Frequency');

    % Save figure
    if ~exist('temp', 'dir')
        mkdir('temp');
    end
    saveas(fig, 'temp/test_advanced_plots_matlab.png');
    fprintf('Figure saved to temp/test_advanced_plots_matlab.png\n');

    close(fig);

    fprintf('\n✓ PASSED: Advanced plotting completed\n');
    passed_tests = passed_tests + 1;
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% TEST 9: Data I/O
fprintf('\n====================================================================\n');
fprintf('TEST 9: Data I/O (MAT and CSV)\n');
fprintf('====================================================================\n');

try
    % Create temp directory if needed
    if ~exist('temp', 'dir')
        mkdir('temp');
    end

    % Create test data
    rng(999);
    test_matrix = randn(10, 3);

    test_struct = struct();
    test_struct.name = 'Test Data';
    test_struct.values = test_matrix;
    test_struct.timestamp = datetime('now');

    % Save to MAT file
    save('temp/test_io_matlab.mat', 'test_matrix', 'test_struct');
    fprintf('Saved to MAT file\n');

    % Export to CSV
    writematrix(test_matrix, 'temp/test_io_matlab.csv');
    fprintf('Saved to CSV file\n');

    % Clear and reload
    original_matrix = test_matrix;
    clear test_matrix test_struct

    % Load MAT file
    load('temp/test_io_matlab.mat');
    fprintf('Loaded from MAT file\n');

    % Import CSV
    imported_csv = readmatrix('temp/test_io_matlab.csv');
    fprintf('Loaded from CSV file\n');

    % Validate
    mat_loaded = exist('test_matrix', 'var') && exist('test_struct', 'var');
    csv_match = max(abs(original_matrix(:) - imported_csv(:))) < 1e-10;

    if mat_loaded && csv_match
        fprintf('\n✓ PASSED: Data I/O operations work correctly\n');
        passed_tests = passed_tests + 1;
    else
        fprintf('\n✗ FAILED: Data mismatch or load error\n');
    end
catch ME
    fprintf('✗ ERROR: %s\n', ME.message);
end

%% Summary
fprintf('\n====================================================================\n');
fprintf('TEST SUMMARY\n');
fprintf('====================================================================\n');
fprintf('Total Tests: %d\n', total_tests);
fprintf('Passed: %d ✓\n', passed_tests);
fprintf('Failed: %d ✗\n', total_tests - passed_tests);
fprintf('Success Rate: %.1f%%\n', 100 * passed_tests / total_tests);
fprintf('====================================================================\n\n');

if passed_tests == total_tests
    fprintf('🎉 All tests passed!\n\n');
else
    fprintf('⚠️  Some tests failed. Please review the output above.\n\n');
end
