#!/bin/bash
# MATLAB MCP Server - Configuration Helper
#
# This script:
# 1. Auto-detects MATLAB installation
# 2. Displays the MCP configuration for you to copy
#
# You manually add the configuration to your Claude Code config file.
# The actual installation is handled automatically by uvx when Claude Code starts.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/subspace-lab/matlab-mcp-server/main/install-matlab-mcp.sh | bash
#   # OR
#   ./install-matlab-mcp.sh

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Print banner
echo ""
echo "=========================================="
echo "  MATLAB MCP Server - Setup"
echo "=========================================="
echo ""

# Detect platform
detect_platform() {
    case "$(uname -s)" in
        Darwin*)
            PLATFORM="macos"
            ARCH=$(uname -m)
            if [ "$ARCH" = "arm64" ]; then
                MATLAB_ARCH="maca64"
            else
                MATLAB_ARCH="maci64"
            fi
            LIB_PATH_VAR="DYLD_LIBRARY_PATH"
            ;;
        Linux*)
            PLATFORM="linux"
            MATLAB_ARCH="glnxa64"
            LIB_PATH_VAR="LD_LIBRARY_PATH"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            PLATFORM="windows"
            MATLAB_ARCH="win64"
            LIB_PATH_VAR="PATH"
            ;;
        *)
            log_error "Unsupported platform: $(uname -s)"
            exit 1
            ;;
    esac

    log_success "Detected platform: $PLATFORM ($MATLAB_ARCH)"
}

# Find MATLAB installation
find_matlab() {
    log_info "Searching for MATLAB installation..."

    MATLAB_PATH=""

    case "$PLATFORM" in
        macos)
            # Check /Applications for recent versions first
            for version in R2026a R2025b R2025a R2024b R2024a R2023b R2023a; do
                if [ -d "/Applications/MATLAB_${version}.app" ]; then
                    MATLAB_PATH="/Applications/MATLAB_${version}.app"
                    MATLAB_VERSION="$version"
                    break
                fi
            done
            ;;
        linux)
            # Check common Linux installation paths
            for base_path in "/usr/local/MATLAB" "/opt/MATLAB" "$HOME/MATLAB"; do
                if [ -d "$base_path" ]; then
                    for version in R2026a R2025b R2025a R2024b R2024a R2023b R2023a; do
                        if [ -d "$base_path/$version" ]; then
                            MATLAB_PATH="$base_path/$version"
                            MATLAB_VERSION="$version"
                            break 2
                        fi
                    done
                fi
            done
            ;;
        windows)
            # Check Program Files
            for base_path in "/c/Program Files/MATLAB" "/c/Program Files (x86)/MATLAB"; do
                if [ -d "$base_path" ]; then
                    for version in R2026a R2025b R2025a R2024b R2024a R2023b R2023a; do
                        if [ -d "$base_path/$version" ]; then
                            MATLAB_PATH="$base_path/$version"
                            MATLAB_VERSION="$version"
                            break 2
                        fi
                    done
                fi
            done
            ;;
    esac

    if [ -z "$MATLAB_PATH" ]; then
        log_error "MATLAB installation not found!"
        echo ""
        echo "Please install MATLAB or set MATLAB_PATH manually:"
        echo "  export MATLAB_PATH=/path/to/MATLAB"
        echo "  $0"
        exit 1
    fi

    log_success "Found MATLAB $MATLAB_VERSION: $MATLAB_PATH"

    # Set library path
    MATLAB_LIB_PATH="$MATLAB_PATH/bin/$MATLAB_ARCH"
    if [ ! -d "$MATLAB_LIB_PATH" ]; then
        log_warning "MATLAB library path not found: $MATLAB_LIB_PATH"
    else
        log_success "Found MATLAB libraries: $MATLAB_LIB_PATH"
    fi
}

# Display MCP configuration
display_mcp_config() {
    log_info "MATLAB MCP Server configuration ready!"

    # Determine config file path
    case "$PLATFORM" in
        macos)
            MCP_CONFIG_PATH="~/.config/claude/mcp.json"
            ;;
        linux)
            MCP_CONFIG_PATH="~/.config/claude/mcp.json"
            ;;
        windows)
            MCP_CONFIG_PATH="%APPDATA%\\claude\\mcp.json"
            ;;
    esac

    echo ""
    echo "=========================================="
    echo "  Configuration"
    echo "=========================================="
    echo ""
    echo "Add this to your Claude Code config file at:"
    echo -e "  ${BLUE}$MCP_CONFIG_PATH${NC}"
    echo ""
    echo -e "${GREEN}Copy this configuration:${NC}"
    echo ""
    echo "{"
    echo "  \"mcpServers\": {"
    echo "    \"matlab\": {"
    echo "      \"command\": \"uvx\","
    echo "      \"args\": [\"matlab-mcp-server\"],"
    echo "      \"env\": {"
    echo "        \"$LIB_PATH_VAR\": \"$MATLAB_LIB_PATH\""
    echo "      }"
    echo "    }"
    echo "  }"
    echo "}"
    echo ""
    log_info "If you already have an mcp.json file, add the 'matlab' entry to the existing 'mcpServers' object."
}

# Main setup flow
main() {
    detect_platform
    find_matlab
    display_mcp_config

    # Print next steps
    echo ""
    echo "=========================================="
    echo "  Next Steps"
    echo "=========================================="
    echo ""
    log_success "MATLAB detected: $MATLAB_VERSION at $MATLAB_PATH"
    echo ""
    echo "1. Copy the configuration above to your Claude Code config file"
    echo ""
    echo "2. Restart Claude Code"
    echo ""
    echo "3. Test the MATLAB MCP server in Claude Code:"
    echo -e "   ${BLUE}> Execute MATLAB code: disp('Hello from MATLAB!')${NC}"
    echo ""
    echo "Note: The first time Claude Code starts, uvx will automatically:"
    echo "  - Download matlab-mcp-server from PyPI"
    echo "  - Install matlabengine and all dependencies"
    echo "  - Start the MATLAB MCP server"
    echo ""
    echo "This may take a minute on first launch."
    echo ""
    echo "For more info: https://github.com/subspace-lab/matlab-mcp-server"
    echo ""
}

# Run main setup
main
