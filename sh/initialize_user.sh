#!/bin/bash

# This script initializes all users for the Reality Merge project.

echo "--- Reality Merge User Initialization ---"
echo "This script will guide you through setting up the users for the multi-user Google Drive workflow."
echo ""

# Ask for the number of team members
read -p "How many team members are there in total? " num_users
echo ""

# Get Super Administrator's information
echo "--- Super Administrator Setup ---"
echo "First, let's set up the Super Administrator. This user will have full control over the Google Drive folder structure."
read -p "Enter the GitHub username for the Super Administrator: " super_admin_github_username
git config user.name "$super_admin_github_username"
echo "Git local user.name for this session set to: $super_admin_github_username"
read -p "Enter the Google-hosted email address for the Super Administrator: " super_admin_google_email
echo ""

# Store super admin info (this part will be extended later to actually use the data)
echo "Super Administrator configured:"
echo "GitHub Username: $super_admin_github_username"
echo "Google Email: $super_admin_google_email"
echo ""

# Loop for remaining users
remaining_users=$((num_users - 1))
if [ "$remaining_users" -gt 0 ]; then
    echo "--- Normal User Setup ---"
    echo "Now, let's set up the remaining $remaining_users team members."
    echo "These users will have access to their own folders and the shared folder."
    echo ""
    for i in $(seq 1 $remaining_users); do
        echo "--- User $((i + 1)) ---"
        read -p "Enter GitHub username for User $((i + 1)): " github_username
        read -p "Enter Google-hosted email for User $((i + 1)): " google_email
        echo "User $((i + 1)) configured:"
        echo "GitHub Username: $github_username"
        echo "Google Email: $google_email"
        echo "------------------------------------------------------------------"
        echo "Please communicate the following information to the super-administrator:"
        echo "GitHub Username: $github_username"
        echo "Google Email: $google_email"
        echo "------------------------------------------------------------------"
        echo ""
    done
fi


# Guide through authentication for the current user (super-admin)
echo "--- Google Drive Authentication ---"
echo "Now, let's authenticate with Google Drive. This will be the authentication for the current user (Super Administrator)."
read -p "Press [Enter] to continue with Google Drive authentication..."
sh sh/authenticate_gdrive.sh

echo ""
echo "Initialization complete."