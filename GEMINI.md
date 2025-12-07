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
3.  **Communicate with Super-Admin:** Communicate the user's GitHub username and Google email to the super-admin, who will then update their local `users.json` file. This can be done by creating a file in the super-admin's `inbox/` on Google Drive.
4.  **Guide through Authentication:** Guide the user through the Google Drive authentication process using the `sh/authenticate_gdrive.sh` script.