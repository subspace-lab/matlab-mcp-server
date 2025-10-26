# MCP Resources Catalog

This document defines the MCP "resources" our server will expose for coding assistants.

## Design Context

**For Coding Assistants:** Resources provide read-only access to MATLAB environment state and documentation. The assistant can inspect these without executing code.

**Philosophy:**
- Expose MATLAB runtime state (version, toolboxes, workspace, session info)
- Provide user-facing documentation (README, guides)
- Do NOT expose internal planning docs (kept separate for development)

## Conventions

- URI scheme: `matlab://...` for dynamic MATLAB data; `docs://...` for user docs
- MIME types: `text/plain`, `text/markdown`, `application/json`, `image/png`
- Resources are listed via `list_resources` and fetched via `read_resource`
- All MATLAB resources are read-only snapshots

---

## Essentials (default resources)

### matlab://env/version
- What: MATLAB version and platform info
- Type: `text/plain`

### matlab://env/toolboxes
- What: Installed toolboxes with versions
- Type: `application/json`

### matlab://session/info
- What: Session details (shared name, uptime, pid)
- Type: `application/json`

### matlab://workspace/snapshot
- What: Current workspace variables (name, class, size, preview)
- Type: `application/json`

### matlab://workspace/variable/{name}
- What: Value/summary of a specific variable
- Type: `application/json`

### matlab://figure/current.png
- What: Current figure as image
- Type: `image/png`

### matlab://figure/{n}.png
- What: Figure N as image
- Type: `image/png`

### docs://readme
- What: Project README (rendered)
- Type: `text/markdown`

### docs://planning
- What: Planning & roadmap
- Type: `text/markdown`

### docs://tools
- What: MCP tool catalog
- Type: `text/markdown`

### docs://userstory
- What: Scenarios and personas
- Type: `text/markdown`

### docs://shared-sessions
- What: Shared sessions how-to
- Type: `text/markdown`

### docs://uv-environment
- What: uv environment explanation
- Type: `text/markdown`

---

## Optional/domain resources (enable with modes)

### matlab://control/step_response
- What: Latest step response data/plot reference
- Type: `application/json` (data) or `image/png`

### matlab://rf/sparameters
- What: Parsed S-parameters summary
- Type: `application/json`

### matlab://finance/forecast
- What: Latest forecast metrics snapshot
- Type: `application/json`

---

## Simulink (next phase, separate server)

### simulink://model/{name}/signals
- What: Logged signals (list/metadata)
- Type: `application/json`

### simulink://model/{name}/report/coverage
- What: Coverage report (path or inline summary)
- Type: `application/json` (summary) or `text/html` (report)

### simulink://model/{name}/artifacts
- What: Build/sim artifacts listing
- Type: `application/json`

---

## External References

- MCP Spec: `https://modelcontextprotocol.io/`
- MATLAB Engine for Python (PyPI): `https://pypi.org/project/matlabengine/`



