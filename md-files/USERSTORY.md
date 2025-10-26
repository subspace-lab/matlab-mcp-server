# User Stories and Scenarios (MATLAB MCP Server)

## Personas
- **Claude Desktop User**: Conversational workflow; wants inline plots and quick results.
- **Claude Code User**: In-editor iteration; wants reproducible runs and tight workspace control.
- **Data Scientist/Researcher**: Data I/O, analysis, long runs, and artifact export.
- **MATLAB Power User**: GUI/shared sessions, toolbox/parallel features, profiling/tests.

---

## Scenario 1: Quick Compute + Plot (Claude Desktop)
- As a user, I ask “plot sin(x) from 0..10” and see the plot inline.
- Acceptance
  - Code runs successfully
  - Figure returned inline
  - Any variables validated if requested
- Tools
  - `execute_matlab`
  - `save_current_figure` or `export_figure_as_image`
  - `get_variable` (optional)
  - `get_matlab_version` (optional for env notes)

## Scenario 2: Debugging an Error (Claude Code)
- As a developer, I run a custom function, get an error, inspect workspace, fix path, rerun.
- Acceptance
  - Error text surfaced
  - Workspace variables visible
  - Path issues fixable quickly
- Tools
  - `execute_matlab`
  - `get_workspace_variables`
  - `get_variable`
  - `add_path`
  - `change_directory`
  - `get_help`

## Scenario 3: Data Analysis Pipeline (CSV → MATLAB → Results)
- As a data scientist, I import CSV, compute stats/plots, export results.
- Acceptance
  - Data imported into workspace
  - Outputs exported as CSV/PNG
  - Script re-runnable
- Tools
  - `import_data`
  - `execute_matlab` (or `execute_matlab_function`)
  - `export_data`
  - `save_current_figure` / `export_figure_as_image`
  - `save_mat_file`

## Scenario 4: Use Existing MATLAB GUI (Shared Session)
- As a power user, I control an already-open MATLAB GUI from Claude.
- Acceptance
  - Connect to shared session by name
  - See updates in Command Window/Workspace
- Tools
  - `get_session_info`
  - `list_shared_sessions`
  - `connect_to_shared_session` (optional)
  - `execute_matlab`
  - `get_workspace_variables`

## Scenario 5: Toolbox-Aware Assistance
- As a user, I run code that may require certain toolbox functions.
- Acceptance
  - Toolboxes listed/checked
  - Helpful guidance if missing
- Tools
  - `list_installed_toolboxes`
  - `check_toolbox`
  - `get_help`

## Scenario 6: Long-Running Job + Monitoring
- As a researcher, I run long computations and monitor progress without blocking.
- Acceptance
  - Non-blocking execution or progress logs
  - Ability to inspect intermediate variables
- Tools
  - `execute_matlab` (with optional async/streaming)
  - `get_variable`
  - `get_workspace_variables`
  - `save_current_figure` (periodic snapshots)

## Scenario 7: Reproducible Environment Checks
- As a developer, I need to capture environment context in results.
- Acceptance
  - MATLAB version, path, CWD returned on request
- Tools
  - `get_matlab_version`
  - `list_path`
  - `get_current_directory`

## Scenario 8: Profiling + Performance
- As a power user, I want to profile a function to optimize it.
- Acceptance
  - Profile results surfaced
  - Hotspots identifiable
- Tools
  - `profile_code`
  - `execute_matlab`

## Scenario 9: Unit Tests (MATLAB)
- As a developer, I run MATLAB unit tests and see pass/fail + diagnostics.
- Acceptance
  - Test discovery and detailed results
- Tools
  - `run_tests`

## Scenario 10: Parallel/Distributed Computing
- As a researcher, I want to use a parallel pool and monitor it.
- Acceptance
  - Pool lifecycle controlled
  - Status visible
- Tools
  - `start_parallel_pool`
  - `parallel_pool_status`
  - `stop_parallel_pool`

---

## Industry Scenarios

### Scenario 11: Quant Finance – VaR via Monte Carlo + Backtest
- As a quant, I compute portfolio Value-at-Risk via Monte Carlo and backtest against historical PnL.
- Acceptance
  - Simulated PnL distribution saved
  - VaR/ES computed and plotted
  - Backtest report exported
- Tools
  - `import_data` (prices/weights CSV)
  - `execute_matlab` (simulation and stats)
  - `export_data` (VaR report CSV)
  - `save_current_figure` / `export_figure_as_image` (distribution/backtest charts)
  - `list_installed_toolboxes`, `check_toolbox` (Econometrics/Statistics)

### Scenario 12: Finance – Time-Series Forecast (ARIMA/GARCH)
- As a risk analyst, I forecast volatility and returns using ARIMA/GARCH and compare models.
- Acceptance
  - Models fit with diagnostics
  - Forecast vs actual plot exported
  - Metrics table (RMSE, AIC) saved
- Tools
  - `import_data`
  - `execute_matlab` (model fit/forecast)
  - `export_data` (metrics)
  - `save_current_figure` (forecast plots)
  - `check_toolbox` (Econometrics Toolbox)

### Scenario 13: Control – PID Tuning + Step Response
- As a control engineer, I tune PID gains and verify with step/trajectory response.
- Acceptance
  - Plant model loaded/defined
  - Step/trajectory response plots exported
  - Gains documented
- Tools
  - `execute_matlab` (tf/ss, pidtune, step, lsim)
  - `save_current_figure`
  - `export_data` (gains/results)
  - `check_toolbox` (Control System Toolbox)

### Scenario 14: Control – System Identification from Experimental Data
- As an engineer, I estimate a plant model from I/O data and validate it.
- Acceptance
  - Data imported and preprocessed
  - Identified model parameters saved
  - Fit percentage and residuals plotted
- Tools
  - `import_data` (I/O logs)
  - `execute_matlab` (iddata, tfest/ssest, compare)
  - `save_current_figure`
  - `export_data`
  - `check_toolbox` (System Identification Toolbox)

### Scenario 15: RF – S‑Parameters Analysis (.s2p) + Smith Chart
- As an RF engineer, I load S-parameters, visualize return loss, and display Smith charts.
- Acceptance
  - .s2p imported and parsed
  - |S11|, |S21| plots exported
  - Smith chart image returned inline
- Tools
  - `import_data` (.s2p)
  - `execute_matlab` (rfplot, smithchart)
  - `export_figure_as_image` / `save_current_figure`
  - `check_toolbox` (RF Toolbox)

### Scenario 16: RF – Filter Design and Verification
- As an RF designer, I synthesize a filter, simulate passband/stopband, and export graphs.
- Acceptance
  - Designed filter specs saved
  - Magnitude/phase/group delay plots exported
- Tools
  - `execute_matlab` (designfilt/eq, filter response)
  - `save_current_figure`
  - `export_data`
  - `check_toolbox` (Signal Processing/RF Toolboxes)

### Scenario 17: Signal Processing/Telecom – Spectral Analysis
- As a DSP engineer, I perform FFT-based spectral analysis and windowing comparisons.
- Acceptance
  - PSD/FFT plots exported
  - Window comparison table saved
- Tools
  - `import_data`
  - `execute_matlab` (fft, pwelch)
  - `save_current_figure`
  - `export_data`

### Scenario 18: Biomedical Imaging – DICOM Preprocessing
- As a researcher, I load DICOM, denoise/segment, and export overlays.
- Acceptance
  - DICOM loaded and anonymized if needed
  - Segmentation mask saved
  - Overlay image exported
- Tools
  - `import_data` (DICOM)
  - `execute_matlab` (image processing pipeline)
  - `export_figure_as_image` / `save_current_figure`
  - `save_mat_file` (masks/metadata)
  - `check_toolbox` (Image Processing Toolbox)

### Scenario 19: Power/Energy – Load Profile + Harmonics
- As a power systems engineer, I analyze load profiles and harmonic content.
- Acceptance
  - THD metrics computed and saved
  - Time/frequency plots exported
- Tools
  - `import_data`
  - `execute_matlab` (spectral/THD computations)
  - `save_current_figure`
  - `export_data`

### Scenario 20: Automotive/Aerospace – Sensor Fusion (Kalman Filter)
- As an ADAS engineer, I fuse IMU/GNSS data with a Kalman filter and validate trajectories.
- Acceptance
  - Filter parameters and covariances saved
  - Trajectory truth vs estimate plot exported
- Tools
  - `import_data`
  - `execute_matlab` (Kalman filter, navigation equations)
  - `save_current_figure`
  - `export_data`
  - `check_toolbox` (Navigation/Signal Processing)

## Deferred: Simulink Scenarios (Next Phase)

### Scenario S1: Run Simulink Model + Log Signals
- As a model-based designer, I run a Simulink model, sweep parameters, and log signals for analysis.
- Acceptance
  - Model loads and simulates with given stop time/solver
  - Signals logged and exported
  - Parameter sweep results saved
- Tools (Simulink server)
  - `sim_run(model, params?, stop_time?, solver?)`
  - `sim_get_signals(model, signals?)`
  - `sim_export_artifacts(model, path, fmt?)`

### Scenario S2: Parameter Tuning via set_param
- As an engineer, I adjust block parameters and re-run simulations to meet specs.
- Acceptance
  - Parameters updated (set_param)
  - Response metrics computed and exported
- Tools (Simulink server)
  - `sim_set_param(model, block, name, value)`
  - `sim_run(model)`
  - `sim_get_signals(model)`

### Scenario S3: Test Harness and Coverage
- As a tester, I run test harnesses, collect coverage, and export reports.
- Acceptance
  - Tests executed; pass/fail recorded
  - Coverage metrics exported (html/xml)
- Tools (Simulink server)
  - `sim_run_tests(model, suite?)`
  - `sim_export_coverage(model, path)`

### Scenario S4: Code Generation (Embedded Coder)
- As an embedded engineer, I build code from a model and collect build artifacts.
- Acceptance
  - Code generated successfully
  - Build logs and artifacts exported
- Tools (Simulink server)
  - `sim_build_code(model, config?)`
  - `sim_export_artifacts(model, path)`

---

## Cross-Cutting Tooling (Most Scenarios)
- `execute_matlab`
- `get_workspace_variables`, `get_variable`, `set_variable`, `clear_workspace`
- `add_path`, `list_path`, `change_directory`, `get_current_directory`
- `save_current_figure`, `export_figure_as_image`, `close_figures`
- `import_data`, `export_data`, `load_mat_file`, `save_mat_file`
- `get_matlab_version`, `list_installed_toolboxes`, `check_toolbox`
- `get_help`


