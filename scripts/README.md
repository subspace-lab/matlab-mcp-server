# Utility Scripts

This directory contains utility and demo scripts for working with MATLAB sessions.

## Setup and Configuration

### `setup_matlab_env.py`
Auto-detect MATLAB installation and configure environment variables.

```bash
uv run scripts/setup_matlab_env.py
```

This script:
- Searches for MATLAB installations on your system
- Detects the correct architecture (Intel/Apple Silicon/Linux)
- Creates a `.env` file with proper library paths
- Guides you through selecting from multiple MATLAB versions

**When to use:**
- First time setup
- After installing a new MATLAB version
- If you encounter "library not found" errors
- When MATLAB is in a non-default location

**What it creates:**
A `.env` file that you can use with:
```bash
uv run --env-file .env matlab-cli -c "disp('Hello')"
```

## Session Management

### `check_sessions.py`
Check for active shared MATLAB sessions and display their details.

```bash
uv run scripts/check_sessions.py
```

Shows:
- List of all shared sessions
- Session details (version, workspace, directory)
- Connection examples

## Demo Scripts

### `demo_in_your_matlab.py`
Demonstrates connecting to an existing MATLAB session and adding content to it.

**Prerequisites:** You must first create a shared session in MATLAB:
```matlab
matlab.engine.shareEngine('MATLAB_98037')
```

Then run:
```bash
uv run scripts/demo_in_your_matlab.py
```

This will:
- Connect to your running MATLAB session
- Add variables to the workspace
- Send messages to the Command Window
- Create plots

### `setup_current_matlab.py`
Setup script to add demo content to a currently running MATLAB GUI.

**Instructions:**
1. Open MATLAB GUI manually
2. In MATLAB Command Window: `matlab.engine.shareEngine('MyMATLAB')`
3. Run this script:
   ```bash
   uv run scripts/setup_current_matlab.py
   ```

### `python_creates_gui_session.py`
Interactive demo showing Python creating a MATLAB GUI session that you can interact with.

```bash
uv run scripts/python_creates_gui_session.py
```

Features:
- Python starts MATLAB with GUI
- Creates a shared session
- Demonstrates bidirectional communication
- Interactive prompts for testing

## GUI Starters

### `quick_gui_test.py`
Quick test script to start MATLAB GUI and set a variable.

```bash
uv run scripts/quick_gui_test.py
```

Simple demo showing:
- Starting MATLAB with desktop mode
- Setting workspace variables
- Sending messages to Command Window

### `start_gui.py`
Start MATLAB with visible GUI - minimal example.

```bash
uv run scripts/start_gui.py
```

Creates a shared session named "MyGUI" and adds demo variables.

### `start_gui_session.py`
Start MATLAB GUI session with more setup and interactive options.

```bash
uv run scripts/start_gui_session.py
```

Includes:
- Demo variables and plots
- Welcome message in Command Window
- Option to keep session running or close

### `start_matlab_gui.py`
Most comprehensive GUI starter with extensive demo content.

```bash
uv run scripts/start_matlab_gui.py
```

Features:
- Multiple subplots (sine, cosine, bar chart, histogram)
- Comprehensive demo variables
- Detailed instructions for usage
- Interactive close/keep-alive option

## Usage Patterns

### Quick Check
```bash
# See what sessions are available
uv run scripts/check_sessions.py
```

### Start a New GUI Session
```bash
# For quick testing
uv run scripts/quick_gui_test.py

# For comprehensive demo
uv run scripts/start_matlab_gui.py
```

### Work with Existing Session
```bash
# If you already have MATLAB open
uv run scripts/setup_current_matlab.py

# Or connect and manipulate
uv run scripts/demo_in_your_matlab.py
```

### Learn Bidirectional Communication
```bash
# Interactive demo
uv run scripts/python_creates_gui_session.py
```

## Notes

All scripts add `src/` to the Python path to import the `matlab_mcp_server` module, so they can be run from the project root without installing the package.
