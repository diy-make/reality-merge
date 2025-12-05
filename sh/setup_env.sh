#!/bin/bash

# This script runs the Python-based virtual environment setup.

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "Running environment setup from $PROJECT_ROOT..."

# Run the Python setup script
python3 "$PROJECT_ROOT/setup.py"
