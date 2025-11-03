# MCP Client Setup Guide - All Supported Clients

Complete installation instructions for the MATLAB MCP server across all 16 supported MCP clients.

## Quick Navigation

**Most Popular (covered in README):**
- [Claude Code](../README.md#installation) - Official Anthropic CLI ✓
- [Claude Desktop](../README.md#installation) - Most popular MCP client ✓
- [Cursor](../README.md#installation) - AI-first code editor ✓
- [VS Code](../README.md#installation) - GitHub Copilot with MCP ✓
- [Codex](../README.md#installation) - Rust-based CLI ✓

**Additional Clients (this page):**
- [Cline](#cline)
- [Windsurf](#windsurf)
- [Continue](#continue)
- [Amp](#amp)
- [Gemini CLI](#gemini-cli)
- [Goose](#goose)
- [Kiro](#kiro)
- [LM Studio](#lm-studio)
- [opencode](#opencode)
- [Qodo Gen](#qodo-gen)
- [Warp](#warp)

---

## Standard Configuration

Most MCP clients use this standard format:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

**Platform-specific environment variables:**

- **macOS (Apple Silicon)**: `"DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"`
- **macOS (Intel)**: `"DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maci64"`
- **Linux**: `"LD_LIBRARY_PATH": "/usr/local/MATLAB/R2024b/bin/glnxa64"`
- **Windows**: Usually not needed (installer handles library paths)

**For local development:**

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/matlab-mcp-server",
        "run",
        "--env-file",
        ".env",
        "matlab-mcp"
      ]
    }
  }
}
```

---

## Cline

**Extension:** [Cline](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) (VS Code)

**Configuration:** Open VS Code Settings → Search for "Cline" or edit `.vscode/settings.json`:

```json
{
  "cline.mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**

1. Install Cline extension from VS Code marketplace
2. Add MCP server configuration to settings
3. Reload VS Code window (Cmd/Ctrl + Shift + P → "Reload Window")
4. Open Cline panel to verify MCP server loaded

---

## Windsurf

**Documentation:** [Windsurf MCP Guide](https://docs.windsurf.com/windsurf/cascade/mcp)

**Configuration Location:**

Follow Windsurf's MCP documentation to locate the configuration file for your platform.

**Configuration:**

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**
1. Locate Windsurf's MCP configuration file
2. Add the MATLAB MCP server configuration
3. Restart Windsurf

---

## Continue

**Extension:** [Continue](https://marketplace.visualstudio.com/items?itemName=Continue.continue) (VS Code)

**Configuration Location:** `.continue/config.json` in your home directory or project root

**Configuration Format:**

```json
{
  "mcpServers": [
    {
      "name": "matlab",
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  ]
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**

1. Install Continue extension from VS Code marketplace
2. Create/edit `.continue/config.json`
3. Add MATLAB MCP server to `mcpServers` array
4. Reload VS Code window (Cmd/Ctrl + Shift + P → "Reload Window")
5. Open Continue panel to verify

**Note:** Continue uses array format (multiple servers supported). Each server needs `name`, `command`, `args`, and optionally `env`.

---

## Amp

**CLI Setup:**

```bash
# macOS (Apple Silicon)
amp mcp add matlab --env DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025b.app/bin/maca64 -- uvx matlab-mcp-server

# Linux
amp mcp add matlab --env LD_LIBRARY_PATH=/usr/local/MATLAB/R2024b/bin/glnxa64 -- uvx matlab-mcp-server
```

**Or update settings.json:**

```json
{
  "amp.mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

---

## Gemini CLI

**Documentation:** [Gemini CLI MCP Guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md#configure-the-mcp-server-in-settingsjson)

**Configuration:**

Follow the Gemini CLI MCP install guide and use this configuration:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

---

## Goose

**UI Configuration:**

Go to `Advanced settings` → `Extensions` → `Add custom extension`.

Configure the following:
- **Name**: `matlab`
- **Type**: `STDIO`
- **Command**: `uvx matlab-mcp-server`
- **Environment Variables**:
  - macOS (Apple Silicon): `DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025b.app/bin/maca64`
  - macOS (Intel): `DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025b.app/bin/maci64`
  - Linux: `LD_LIBRARY_PATH=/usr/local/MATLAB/R2024b/bin/glnxa64`

Click "Add Extension".

---

## Kiro

**Documentation:** [Kiro MCP Documentation](https://kiro.dev/docs/mcp/)

**Configuration File:** `.kiro/settings/mcp.json`

**Configuration:**

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**
1. Create/edit `.kiro/settings/mcp.json`
2. Add MATLAB MCP server configuration
3. Restart Kiro

---

## LM Studio

**UI Configuration:**

Go to `Program` in the right sidebar → `Install` → `Edit mcp.json`.

**Configuration:**

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**
1. Open LM Studio
2. Navigate to Program → Install → Edit mcp.json
3. Add MATLAB MCP server configuration
4. Save and restart LM Studio

---

## opencode

**Documentation:** [opencode MCP Documentation](https://opencode.ai/docs/mcp-servers/)

**Configuration File:** `~/.config/opencode/opencode.json`

**Configuration:**

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "matlab": {
      "type": "local",
      "command": ["uvx", "matlab-mcp-server"],
      "enabled": true,
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**
1. Create/edit `~/.config/opencode/opencode.json`
2. Add MATLAB MCP server configuration
3. Restart opencode

---

## Qodo Gen

**Documentation:** [Qodo Gen Documentation](https://docs.qodo.ai/qodo-documentation/qodo-gen)

**Extension:** Available for VS Code and IntelliJ

**UI Configuration:**

1. Open Qodo Gen chat panel in your IDE
2. Navigate to: `Connect more tools` → `+ Add new MCP`
3. Paste the configuration:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

4. Click `Save`
5. Restart your IDE

---

## Warp

**Documentation:** [Warp MCP Guide](https://docs.warp.dev/knowledge-and-collaboration/mcp#adding-an-mcp-server)

**UI Method:**

Go to `Settings` → `AI` → `Manage MCP Servers` → `+ Add`.

**Slash Command Method:**

Use the `/add-mcp` slash command in the Warp prompt and paste:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64"
      }
    }
  }
}
```

Replace with your MATLAB path (see platform-specific environment variables above).

**Steps:**
1. Use `/add-mcp` command or go to Settings → AI → Manage MCP Servers
2. Add MATLAB MCP server configuration
3. Configuration is applied immediately (no restart needed)

---

## Finding Your MATLAB Library Path

If you don't know your MATLAB library path, run the configuration helper:

```bash
curl -fsSL https://raw.githubusercontent.com/subspace-lab/matlab-mcp-server/main/install-matlab-mcp.sh | bash
```

The script will:
- Auto-detect all MATLAB installations on your system
- Detect the correct architecture (Intel/Apple Silicon/Linux/Windows)
- Display the config with the correct paths
- You copy and paste it into your MCP client's config file

**Manual detection:**

```bash
# macOS
ls -d /Applications/MATLAB_R*.app/bin/mac*64

# Linux
ls -d /usr/local/MATLAB/R*/bin/glnxa64
```

---

## Verification

After configuration, verify your MATLAB MCP server is working:

### Manual Server Test

```bash
# Test the server runs (macOS Apple Silicon example)
DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025b.app/bin/maca64 uvx matlab-mcp-server

# Should show initialization messages, not errors
```

### Client Verification

**Claude Code:**

```bash
claude mcp list        # Should show matlab
claude mcp info matlab # Shows server details
```

**Other Clients:**

- Check client output logs for MCP server connection
- Verify tools appear in the client UI
- Test a query: "Execute MATLAB code: disp('Hello from MATLAB')"
- Check for the 8 MATLAB MCP tools in the tools list

---

## Troubleshooting

### Server Won't Start

1. **Verify `uv` is installed:**
   ```bash
   which uv
   uv --version
   ```

2. **Install uv if needed:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Check MATLAB library path exists:**
   ```bash
   # macOS
   ls -la /Applications/MATLAB_R2025b.app/bin/maca64

   # Linux
   ls -la /usr/local/MATLAB/R2024b/bin/glnxa64
   ```

4. **Test manually:**
   ```bash
   # macOS (Apple Silicon)
   DYLD_LIBRARY_PATH=/Applications/MATLAB_R2025b.app/bin/maca64 uvx matlab-mcp-server

   # Linux
   LD_LIBRARY_PATH=/usr/local/MATLAB/R2024b/bin/glnxa64 uvx matlab-mcp-server
   ```

5. **Validate JSON config:**
   ```bash
   cat config.json | jq .
   ```

### Tools Don't Appear

1. **Restart client after configuration**
   - Most clients require a full restart to load new MCP servers

2. **Check JSON is valid**
   - No syntax errors (missing commas, quotes, brackets)
   - Proper escaping of paths

3. **Review client logs**
   - Check for MCP connection errors
   - Look for MATLAB engine initialization errors

4. **Ensure server name is correct**
   - Use `matlab` consistently (case-sensitive in some clients)

### MATLAB Engine Errors

1. **MATLAB not found:**
   - Verify MATLAB is installed
   - Check library path points to correct version

2. **Library path errors:**
   - Ensure using correct variable (`DYLD_LIBRARY_PATH` vs `LD_LIBRARY_PATH`)
   - Path must be absolute, not relative
   - Check for correct architecture (maca64 vs maci64 vs glnxa64)

3. **Permission errors:**
   - Ensure MATLAB installation has proper permissions
   - Try running MATLAB directly to verify it works

### Platform-Specific Issues

**macOS:**
- Use `DYLD_LIBRARY_PATH` (not `LD_LIBRARY_PATH`)
- Check architecture: `uname -m` (arm64 = Apple Silicon, x86_64 = Intel)
- Apple Silicon uses `maca64`, Intel uses `maci64`

**Linux:**
- Use `LD_LIBRARY_PATH` (not `DYLD_LIBRARY_PATH`)
- Usually `glnxa64` architecture
- Check MATLAB installation path (may vary by distribution)

**Windows:**
- Library path usually not needed
- MATLAB installer typically handles this automatically
- If issues persist, check MATLAB installation in PATH

---

## Quick Reference Table

| Client | Config Location | Restart Required | Format | Notes |
|--------|----------------|------------------|--------|-------|
| Claude Code | `.mcp.json` (project) | No | JSON | CLI: `claude mcp add` |
| Claude Desktop | `~/Library/.../claude_desktop_config.json` | Yes | JSON | Most popular client |
| VS Code | User/Workspace settings | Window reload | JSON | GitHub Copilot required |
| Cursor | `~/Library/.../Cursor/mcp_config.json` | Yes | JSON | UI or file config |
| Codex | `~/.codex/config.toml` | Yes | TOML | CLI + manual env |
| Cline | `.vscode/settings.json` | Window reload | JSON | VS Code extension |
| Windsurf | See docs | Yes | JSON | Refer to Windsurf docs |
| Continue | `.continue/config.json` | Window reload | JSON | Array format |
| Amp | VS Code settings | Window reload | JSON | CLI available |
| Gemini CLI | See docs | Yes | JSON | Follow Gemini docs |
| Goose | UI configuration | No | UI | Advanced settings |
| Kiro | `.kiro/settings/mcp.json` | Yes | JSON | File config |
| LM Studio | UI configuration | Yes | JSON | Program → Install |
| opencode | `~/.config/opencode/opencode.json` | Yes | JSON | Custom schema |
| Qodo Gen | UI configuration | Yes | JSON | Chat panel config |
| Warp | UI or `/add-mcp` command | No | JSON | Terminal AI |

---

## Environment Variables

All clients support environment variables in the MCP server configuration:

```json
{
  "mcpServers": {
    "matlab": {
      "command": "uvx",
      "args": ["matlab-mcp-server"],
      "env": {
        "DYLD_LIBRARY_PATH": "/Applications/MATLAB_R2025b.app/bin/maca64",
        "MATLAB_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Common Environment Variables:**

- `DYLD_LIBRARY_PATH` (macOS) - Path to MATLAB libraries
- `LD_LIBRARY_PATH` (Linux) - Path to MATLAB libraries
- `MATLAB_LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARN, ERROR)

---

## Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [MATLAB MCP Server GitHub](https://github.com/subspace-lab/matlab-mcp-server)
- [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)

---

## Need Help?

- Check the main [README.md](../README.md) for overview and top 5 clients
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development setup
- See [MATLAB_MCP_GUIDE.md](MATLAB_MCP_GUIDE.md) for detailed usage examples
- Report issues on [GitHub Issues](https://github.com/subspace-lab/matlab-mcp-server/issues)

---

## Contributing

Found a better way to configure a client? Want to add support for a new client?

1. Fork the repository
2. Update this documentation
3. Test with the actual client
4. Submit a pull request

We welcome contributions to improve setup instructions and expand client support!
