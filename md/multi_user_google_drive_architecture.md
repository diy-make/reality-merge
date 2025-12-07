# Multi-User Google Drive Architecture

This document outlines the proposed architecture for a multi-user, multi-agent workflow using Google Drive as a shared file system, orchestrated by Gemini CLIs.

## 1. Core Concepts

-   **Multi-User Support:** The system is designed to support multiple users, each identified by their GitHub username.
-   **Google Drive as Shared Storage:** Google Drive serves as the central hub for file sharing and synchronization.
-   **Super Administrator vs. Non-Super Administrator Roles:** One user (and their Gemini agent) acts as a "super administrator" with full control over the Google Drive structure. Other users are "non-super administrators" with limited permissions.
-   **AI-Orchestrated:** Gemini CLI agents are responsible for orchestrating the file synchronization and processing tasks.

## 2. Google Drive Folder Structure

The following folder structure will be implemented within a single, shared Google Drive folder (the "root folder").

```
<root_folder>/
├── users/
│   ├── apemake/
│   │   ├── inbox/
│   │   └── backup/
│   ├── vdharvey/
│   │   ├── inbox/
│   │   └── backup/
│   └── ... (other users)
└── shared/
```

-   **`<root_folder>`:** The main project folder on Google Drive. The ID of this folder will be stored as a configuration variable.
-   **`users/`:** A directory containing subdirectories for each user.
-   **`users/{username}/`:** A directory for each user, named after their GitHub username.
-   **`users/{username}/inbox/`:** The user's "inbox" folder. Other users can place files here for the user's Gemini agent to process. The agent will download, process, and then delete files from this folder.
-   **`users/{username}/backup/`:** The user's backup folder. This is a one-way sync of their entire local project directory, including dotfiles and `.gitignore`.
-   **`shared/`:** A common folder that all users can read from and write to. Files in this folder are not deleted by the agents.

## 2.5. User Management

To manage permissions and namespaces effectively, the super administrator will maintain a list of all users. This list will map each user's GitHub username to their Google-hosted email address.

-   **Super Administrator's Responsibility:** The super administrator is responsible for maintaining this user list in a `.gitignore`'d `users.json` file and using it to grant the appropriate permissions on Google Drive.
-   **Non-Super Admin Agent's Responsibility:** During the onboarding process, a non-super-admin Gemini agent must prompt the user for their Google email address and communicate this information to the super administrator. This will be part of the `sh/initialize_user.sh` script's functionality.

## 3. Permissions Model

-   **Super Administrator:**
    -   Has full read/write access to the entire `<root_folder>` and all its subdirectories.
    -   Is responsible for creating and managing the `users/{username}/` directories for new users.
-   **Non-Super Administrators:**
    -   Have full read/write access to their own `users/{username}/` directory.
    -   Have read/write access to the `shared/` directory.
    -   Do not have access to other users' directories.

## 4. Orchestrator Logic (`py/reality_merge.py`)

The `py/reality_merge.py` script will be updated to differentiate between super-admin and non-super-admin roles. This will be determined by a configuration setting or an environment variable (e.g., `REALITY_MERGE_ROLE=super_admin`).

-   **Super Admin Mode:**
    -   Can create new user directories (`users/{username}/`).
    -   Can list and manage all files and folders.
-   **Non-Super Admin Mode:**
    -   Can only access its own user directory and the `shared/` directory.
    -   The script will be updated to use the user's GitHub username (from `git config user.name`) to determine the correct paths for `inbox/` and `backup/`.

## 5. New User Onboarding Workflow

The following steps will be documented in the `README.md` for new users like `vdharvey`:

1.  **Clone the `reality-merge` repository.**
2.  **Create a Google Cloud Project:**
    -   Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
    -   The project name should be `{repo_name}-{username}` (e.g., `reality-merge-vdharvey`).
3.  **Enable APIs:**
    -   Enable the "Google Drive API" and "Google Docs API".
4.  **Create OAuth 2.0 Credentials:**
    -   Create an OAuth 2.0 Client ID for a "Desktop app".
    -   Download the `client_secret.json` file and place it in the root of the `reality-merge` repository.
5.  **Run Initialization Script:**
    -   A new script, `sh/initialize_user.sh`, will be created.
    -   This script will:
        -   Prompt the user for their GitHub username.
        -   Store the username in the local git config (`git config user.name "..."`).
        -   Prompt the user for their Google-hosted email address.
        -   Communicate the GitHub username and Google email to the super-admin (e.g., by creating a file in the super-admin's `inbox/`).
        -   Guide the user through the initial Google Drive authentication process.

## 6. Documentation Plan

-   **`GEMINI.md`:**
    -   Will be updated with a high-level overview of this architecture.
    -   Will contain instructions for non-super-admin Gemini agents on how to perform their tasks:
        -   Checking their `inbox/`.
        -   Syncing their `backup/`.
        -   Interacting with the `shared/` folder.
-   **`README.md`:**
    -   Will be updated with a new "Onboarding a New User" section with detailed, step-by-step instructions.
-   **`md/multi_user_google_drive_architecture.md` (this file):**
    -   Will serve as the detailed technical reference for the architecture.

This detailed plan will be presented to the user for approval. Once approved, I will begin the implementation phase.
