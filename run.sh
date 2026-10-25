#!/usr/bin/env bash
# ==============================================================================
# CV Maker — Professional Offline Resume Studio Launcher
# ==============================================================================

set -e

# Resolve directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Ensure UTF-8 locale to prevent compose table / xkbcommon issues
export LC_ALL="${LC_ALL:-en_US.UTF-8}"
export LANG="${LANG:-en_US.UTF-8}"

# Wayland / Chromium Ozone optimization flags
export QT_WEBENGINE_CHROMIUM_FLAGS="${QT_WEBENGINE_CHROMIUM_FLAGS:---enable-features=UseOzonePlatform --ozone-platform=wayland --log-level=3}"

# Detect Python executable (.venv preferred)
if [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PYTHON_EXEC="$SCRIPT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_EXEC="$(command -v python3)"
else
    echo "Error: Python 3 was not found on your system."
    exit 1
fi

echo "🚀 Starting CV Maker Studio using: $PYTHON_EXEC"
exec "$PYTHON_EXEC" -m cvmaker "$@"
