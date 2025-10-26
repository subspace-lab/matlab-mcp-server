% Simple MATLAB script to test CLI file execution
x = 1:10;
fprintf('Created vector x with %d elements\n', length(x));

mean_val = mean(x);
std_val = std(x);

fprintf('Mean: %.2f\n', mean_val);
fprintf('Standard deviation: %.2f\n', std_val);

% Create a magic square
M = magic(3);
disp('Magic square:');
disp(M);

fprintf('Sum of first row: %d\n', sum(M(1,:)));
