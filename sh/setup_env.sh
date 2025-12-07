#!/bin/bash

# This script runs the Python-based virtual environment setup.

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "Changing to project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT" || exit

echo "Running environment setup..."

# Run the Python setup script
python3 py/setup.py
