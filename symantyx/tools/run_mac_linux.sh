#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command -v python3 &>/dev/null || { echo "python3 not found"; exit 1; }
python3 -c "import tkinter" 2>/dev/null || {
    echo "tkinter missing:  sudo apt install python3-tk  (Ubuntu)"
    echo "                  brew install python-tk       (macOS)"
    exit 1
}
python3 "$SCRIPT_DIR/symantyx_path_builder.py"
