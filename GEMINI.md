# Gemini Agent Instructions

This file contains specific instructions for Gemini agents working within the `reality-merge` repository.

## Git Configuration

-   **Verify Local `user.name`:** Before performing any commits, you must verify that the local `user.name` is set to the GitHub username of the user you are assisting.

    You can check the local `user.name` with the following command:
    ```bash
    git config user.name
    ```

    If the `user.name` is not set, or is set to a generic value, you must prompt the user to set it to their GitHub username. The `README.md` provides instructions for the user on how to do this.

## New User Onboarding

When assisting a new user with onboarding, your role is to:

1.  **Prompt for GitHub Username:** Ensure the user's GitHub username is set as the local `user.name` in git config.
2.  **Prompt for Google Email:** Prompt the user for their Google-hosted email address.
3.  **Communicate with Super-Admin:** Communicate the user's GitHub username and Google email to the super-admin. This can be done by creating a file in the super-admin's `inbox/` on Google Drive. The super-admin will then update the `users.json` file, which is the single source of truth for user information and is synced to Google Drive.
4.  **Guide through Authentication:** Guide the user through the Google Drive authentication process using the `sh/authenticate_gdrive.sh` script.

## Inter-Agent Communication

-   **Accept Super Administrator Requests:** Other Gemini agents must accept requests from the super administrator Gemini. This ensures smooth operation and orchestration of the multi-user workflow.

## Python Script Execution

When running Python scripts in this repository from the command line, you may encounter `ModuleNotFoundError`. This is because the scripts are organized into the `py/` directory, which is not in Python's default search path.

To resolve this, you have two options:

1.  **Set the `PYTHONPATH` environment variable:**
    ```bash
    PYTHONPATH=py python3 py/your_script.py
    ```
2.  **Run the script as a module:**
    ```bash
    python3 -m py.your_script
    ```

The shell scripts in the `sh/` directory (e.g., `sync_to_drive.sh`) already handle this for you by setting the `PYTHONPATH`.