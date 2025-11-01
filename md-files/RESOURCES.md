# MCP Resources Catalog

This document defines the MCP "resources" our server exposes for coding assistants.

## Design Context

**For Coding Assistants:** Resources provide read-only access to MATLAB environment state and documentation. The assistant can inspect these without executing code.

**Philosophy:**
- Expose MATLAB runtime state (version, toolboxes, workspace, session info)
- Provide user-facing documentation (README, guides)
- Do NOT expose internal planning docs (kept separate for development)

## Conventions

- URI scheme: `matlab://...` for dynamic MATLAB data; `docs://...` for user docs
- MIME types: `text/plain`, `text/markdown`, `application/json`
- Resources are listed via `list_resources` and fetched via `read_resource`
- All MATLAB resources are read-only snapshots

---

## Current Resources (v0.2.1)

These resources are implemented and available now:

### Documentation Resources

#### docs://readme
- What: Project README - Getting started guide
- Type: `text/markdown`
- Source: `README.md`

#### docs://guide
- What: Complete user guide with usage examples
- Type: `text/markdown`
- Source: `md-files/MATLAB_MCP_GUIDE.md`

#### docs://limitations
- What: Known limitations and workarounds
- Type: `text/markdown`
- Source: Generated in `resources.py`

### MATLAB Environment Resources

#### matlab://env/version
- What: MATLAB version and platform info
- Type: `text/plain`
- Example: `R2025b (maca64)`

#### matlab://env/toolboxes
- What: Installed toolboxes with versions and metadata
- Type: `application/json`
- Schema: `[{"name": str, "version": str, ...}]`

#### matlab://session/info
- What: Current session details
- Type: `application/json`
- Schema: `{"type": "shared"|"local", "name": str|null, "connected": bool}`

### Workspace Resources

#### matlab://workspace/snapshot
- What: Current workspace variables (name, class, size, preview)
- Type: `application/json`
- Schema: `[{"name": str, "class": str, "size": [int], "bytes": int}]`

---

## Planned Resources (Future Phases)

These resources are planned but not yet implemented:

### Phase 2: Enhanced Workspace Access

#### matlab://workspace/variable/{name}
- What: Value/summary of a specific variable
- Type: `application/json`
- Status: **Not implemented**

### Phase 2: Figure Resources

#### matlab://figure/current.png
- What: Current figure as image
- Type: `image/png`
- Status: **Not implemented** (use `figure` tool instead)

#### matlab://figure/{n}.png
- What: Figure N as image
- Type: `image/png`
- Status: **Not implemented** (use `figure` tool instead)

### Phase 3+: Domain-Specific Resources

#### matlab://control/step_response
- What: Latest step response data/plot reference
- Type: `application/json` (data) or `image/png`
- Status: **Planned** (Phase 3)

#### matlab://rf/sparameters
- What: Parsed S-parameters summary
- Type: `application/json`
- Status: **Planned** (Phase 3)

#### matlab://finance/forecast
- What: Latest forecast metrics snapshot
- Type: `application/json`
- Status: **Planned** (Phase 3)

---

## Future: Simulink Resources (Separate Server)

### simulink://model/{name}/signals
- What: Logged signals (list/metadata)
- Type: `application/json`
- Status: **Future** (separate matlab-simulink server)

### simulink://model/{name}/report/coverage
- What: Coverage report (path or inline summary)
- Type: `application/json` (summary) or `text/html` (report)
- Status: **Future** (separate matlab-simulink server)

### simulink://model/{name}/artifacts
- What: Build/sim artifacts listing
- Type: `application/json`
- Status: **Future** (separate matlab-simulink server)

---

## External References

- MCP Spec: `https://modelcontextprotocol.io/`
- MATLAB Engine for Python (PyPI): `https://pypi.org/project/matlabengine/`



