#!/bin/bash

# This script runs the Google Drive authentication flow.

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "Changing to project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT" || exit

echo "Running authentication..."

# Run the Python authentication script
.venv/bin/python src/google_auth.py
