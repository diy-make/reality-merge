#!/bin/bash

# This script ensures the environment is set up and then runs the
# one-way "push" sync to Google Drive.

# Get the directory of this script to find other project files
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "--- Step 1: Setting up environment ---"
bash "$SCRIPT_DIR/setup_env.sh"

echo ""
echo "--- Step 2: Ensuring Google Drive Authentication ---"
# This will trigger the browser-based auth flow if token.json is missing or expired
bash "$SCRIPT_DIR/authenticate_gdrive.sh"

echo ""
echo "--- Step 3: Syncing project to Google Drive ---"
echo "This may take a while depending on the size of the project and your internet connection."
# Activate venv and run the upload command
source "$SCRIPT_DIR/../.venv/bin/activate"
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/../py
python3 "$SCRIPT_DIR/../py/reality_merge.py" drive upload --user apemake

echo ""
echo "Sync script finished."
