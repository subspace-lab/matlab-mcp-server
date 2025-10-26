# MCP Tools Catalog

This document defines the tool surface area for the MATLAB MCP server, designed specifically for integration with coding assistants.

## Design Context

**Target Users:** AI coding assistants (Claude Code, Cursor, GitHub Copilot, etc.)

**Assumption:** The coding assistant already has:
- File system tools (Read, Write, Edit, Glob, etc.)
- Directory management capabilities
- Text processing and code manipulation tools

**Therefore, this MCP server focuses on:**
- MATLAB computational operations
- Workspace management (variables in MATLAB memory)
- Data interchange (files ↔ MATLAB workspace)
- Visualization and plotting
- MATLAB-specific documentation access
- Session management (connect to running MATLAB instances)

## Session Awareness

All MATLAB tools operate on the **currently connected session**:
- By default, MCP Server creates its own MATLAB session
- Use `session` tool to list and connect to other sessions (e.g., user's MATLAB GUI)
- Switching sessions changes the workspace, figures, and execution context for all tools

**Example workflow:**
1. User opens MATLAB GUI and shares it: `matlab.engine.shareEngine('MyGUI')`
2. Assistant lists sessions: `session(op="list")` → `["MyGUI", ...]`
3. Assistant connects: `session(op="connect", session_name="MyGUI")`
4. All subsequent tools now operate on the MyGUI session

## Conventions

- Parameters shown with `?` are optional.
- Multi-op tools accept an `op` field to select a sub-operation.
- Keep token footprint low by exposing only Essentials by default and enabling groups on demand.

---

## Essentials (default)

### execute_matlab
- Purpose: Execute MATLAB code and return output/errors.
- Schema (inputs): `{ code: string }`

### workspace
- Purpose: Workspace get/set/list/clear.
- Schema: `{ op: "get"|"set"|"list"|"clear", var?: string, value?: any, type_hint?: string }`

### figure
- Purpose: Save/export/close figures.
- Schema: `{ op: "save"|"export"|"close", fig?: number, fmt?: "png"|"jpg"|"svg"|"pdf"|"fig", dpi?: number, path?: string }`

### data_io
- Purpose: Bridge between file system (managed by assistant) and MATLAB workspace.
- Schema: `{ op: "import"|"export"|"load_mat"|"save_mat", path: string, var?: string, fmt?: string }`
- Note: Assistant creates/manages files; this tool moves data between files and MATLAB memory.
- Workflow example:
  1. Assistant writes CSV using Write tool
  2. MATLAB imports CSV into workspace using data_io
  3. MATLAB processes data
  4. MATLAB exports results using data_io
  5. Assistant reads result file using Read tool

### env
- Purpose: Version and toolbox info.
- Schema: `{ op: "version"|"list_toolboxes"|"check_toolbox", name?: string }`

### get_help
- Purpose: Retrieve MATLAB documentation or search results for a function/topic on demand.
- Schema: `{ op?: "help"|"lookfor"|"which", name: string }` (default `op: "help"`)
- Behavior:
  - op=help → `help <name>` (usage, arguments, examples)
  - op=lookfor → `lookfor <name>` (keyword search across topics)
  - op=which → `which -all <name>` (path + toolbox hints)
- Examples:
  - `{ "op": "help", "name": "fft" }`
  - `{ "op": "lookfor", "name": "Kalman" }`
  - `{ "op": "which", "name": "butter" }`

---

## Meta-tools

### session
- Purpose: Manage MATLAB session connections (list, connect, switch sessions).
- Schema: `{ op: "list"|"connect"|"current", session_name?: string }`
- Behavior:
  - op=list → List all available shared MATLAB sessions
  - op=connect → Connect to a specific shared session (requires session_name)
  - op=current → Get current session info (name, type, connection status)
- Impact: **Switching sessions affects all other tools** (workspace, figure, execute_matlab, etc.)
- Error handling: Failed connection attempts preserve the current session
- Examples:
  - `{ "op": "list" }` → Returns: `["MyGUI", "PythonCreated"]`
  - `{ "op": "connect", "session_name": "MyGUI" }` → Connects to user's MATLAB GUI
  - `{ "op": "current" }` → Returns current session info

### route_intent
- Purpose: Lightweight routing to choose mode/group.
- Schema: `{ query: string }`
- Returns: `{ mode: string, confidence: number }`

### select_mode
- Purpose: Enable a tool group for the session.
- Schema: `{ mode: string }`

Notes: `list_tools` returns Essentials plus any enabled groups.

---

## Optional Groups (disabled by default)

### plotting
- figure (extended params), close_figures, current_figure

### data_io
- import_data, export_data, load_mat_file, save_mat_file (fine-grained variants)

### workspace+
- list_workspace, get_variable, set_variable, clear_workspace (unbundled forms)

### toolboxes
- list_installed_toolboxes, check_toolbox

### Domain groups
- control: helpers for frequency/step response, pidtune
- rf: S-parameters helpers, smith chart export
- finance: ARIMA/GARCH forecast wrappers

---

## Simulink (next phase, separate server)

Expose these from a `matlab-simulink` server to avoid bloating core tokens:

- sim_run(model, params?, stop_time?, solver?)
- sim_set_param(model, block, name, value)
- sim_get_signals(model, signals?)
- sim_export_artifacts(model, path, fmt?)
- sim_run_tests(model, suite?)
- sim_export_coverage(model, path)
- sim_build_code(model, config?)

---

## list_tools Behavior
- Returns Essentials + enabled groups.
- Simulink tools appear only when the Simulink server is registered.

## Rollout Order
1. Essentials + meta-tools
2. plotting, data_io, workspace+
3. toolboxes and domain groups
4. Simulink server

---

## Appendix: Session Management Implementation

### Overview

The `session` tool enables connecting to running MATLAB instances, allowing MCP Server to access user's MATLAB GUI workspaces.

### Design Decisions

**Tool Classification**: Meta-tools
- Changes the MCP Server's connection state
- Similar to `route_intent` and `select_mode`
- Not a data processing tool

**Minimal Implementation**: Three operations only
- `list` - List all shared MATLAB sessions
- `connect` - Connect to a specific session
- `current` - Get current session information

**Error Handling**: Preserve current session on connection failure
- Better user experience
- Avoids unexpected disconnections

### Implementation Details

#### Code Location
- `src/matlab_mcp_server/engine.py` (Lines 702-822)
  - `list_sessions()` - Static method
  - `connect_to_session(session_name)` - Instance method
  - `get_current_session()` - Instance method

- `src/matlab_mcp_server/tools.py` (Lines 192-210, 479-508)
  - Tool definition and handler

#### Session Tracking
```python
# Added to MatlabEngine class
self._is_shared: bool = False
self._session_name: Optional[str] = None
```

### Tools Affected by Session Switching

When using `session(op="connect")`, these tools operate on the new session:

| Tool | Impact |
|------|--------|
| `workspace` | Access new session's variables |
| `execute_matlab` | Execute code in new session |
| `figure` | Operate on new session's figures |
| `data_io` | Import/export to new session |
| `env` | Same (MATLAB version unchanged) |
| `get_help` | Same (documentation unchanged) |

### Known Limitations

1. **Non-Shared Sessions Not Visible**
   - Only sessions shared via `matlab.engine.shareEngine()` are listable

2. **Python-to-Python Connection Limitation**
   - ✅ Can connect: Python → MATLAB GUI (primary use case)
   - ❌ Cannot connect: Python → Python-created session
   - This is a MATLAB Engine API limitation

3. **Connection Delay**
   - Remote session connections may take several seconds

### Usage Examples

**In MATLAB GUI** (to share session):
```matlab
matlab.engine.shareEngine('MyGUI')
```

**In Python** (to connect):
```python
from matlab_mcp_server.engine import MatlabEngine

# List available sessions
sessions = MatlabEngine.list_sessions()
# Returns: {"success": true, "sessions": ["MyGUI"], "count": 1}

# Connect to user's session
engine = MatlabEngine()
engine.connect_to_session('MyGUI')

# Now operate on that session
workspace = engine.list_workspace()
```

**Via MCP Tool**:
```json
{"op": "list"}
{"op": "connect", "session_name": "MyGUI"}
{"op": "current"}
```

### Testing

See `tests/test_engine.py` (Lines 377-507) and `tests/test_server.py` (Lines 222-289).

Note: Some tests are skipped due to MATLAB API limitations, but the primary use case (connecting to MATLAB GUI) is manually verified and works correctly.


