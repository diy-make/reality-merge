#!/bin/bash

# This script initializes a new user for the Reality Merge project.

echo "--- New User Initialization ---"

# Prompt for GitHub username
read -p "Enter your GitHub username: " github_username
git config user.name "$github_username"
echo "Git local user.name set to: $github_username"

# Prompt for Google email
read -p "Enter your Google-hosted email address: " google_email

# Communicate with super-admin (placeholder)
echo "------------------------------------------------------------------"
echo "Please communicate the following information to the super-administrator:"
echo "GitHub Username: $github_username"
echo "Google Email: $google_email"
echo "------------------------------------------------------------------"
echo "The super-administrator will then create your folders on Google Drive."
echo "Once your folders are created, you can proceed with authentication."
echo ""

# Guide through authentication
read -p "Press [Enter] to continue with Google Drive authentication..."
sh sh/authenticate_gdrive.sh

echo ""
echo "Initialization complete."
