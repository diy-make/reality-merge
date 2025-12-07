# Gemini Agent Instructions

This file contains specific instructions for Gemini agents working within the `reality-merge` repository.

## Git Configuration

-   **Verify Local `user.name`:** Before performing any commits, you must verify that the local `user.name` is set to the GitHub username of the user you are assisting.

    You can check the local `user.name` with the following command:
    ```bash
    git config user.name
    ```

    If the `user.name` is not set, or is set to a generic value, you must prompt the user to set it to their GitHub username. The `README.md` provides instructions for the user on how to do this.