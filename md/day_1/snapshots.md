# Day 1 Snapshots

---

**1. GitHub Push Rejected due to File Size**
![A screenshot showing a git push being rejected due to a large file size.](../png/github-push-rejected-file-size.png)
*This screenshot captures the moment the Git LFS experiment failed. The user's `git push` was rejected by the remote server because a file exceeded the size limit, even with LFS.*
*   **Key Takeaway:** Git LFS is not a silver bullet for large file management on all platforms. The hybrid cloud approach (Git + Google Drive) was validated by this failure.

---

**2. Google Drive OAuth Consent Screen**
![A screenshot of the Google Drive OAuth consent screen.](../png/gdrive-oauth-consent-screen.png)
*This screenshot shows the Google Drive OAuth consent screen, where the user is prompted to authorize the `reality-merge` application to access their Google account.*
*   **Key Takeaway:** The application uses OAuth 2.0 for secure, user-authorized access to Google Drive.

---

**3. Google Drive Authentication Script Execution**
![A screenshot of the authentication script execution in the terminal.](../png/gdrive-auth-script-execution.png)
*This screenshot shows the successful execution of the `sh/authenticate_gdrive.sh` script. The script provides a URL for the user to complete the authentication flow and confirms that the authentication was successful.*
*   **Key Takeaway:** The authentication process is handled by a script that guides the user through the necessary steps.

---

**4. Google Drive CLI `list` Command Test**
![A screenshot of the `drive list` command being tested in the terminal.](../png/gdrive-cli-list-command-test.png)
*This screenshot shows a successful test of the `reality_merge.py drive list` command, which lists the files in a Google Drive folder. This confirms that the CLI tool can successfully communicate with the Google Drive API.*
*   **Key Takeaway:** The CLI tool provides a `list` command to inspect the contents of a Google Drive folder.

---

**5. Google Drive CLI `sync` Command in Action**
![A screenshot of the `drive upload` command syncing the project to Google Drive.](../png/gdrive-sync-in-action.png)
*This screenshot shows the `drive upload` command being used to sync the local project to Google Drive. This demonstrates the core functionality of the hybrid cloud solution.*
*   **Key Takeaway:** The CLI tool provides an `upload` command to sync local files to Google Drive.

---

**6. Google Drive Download Success**
![A screenshot showing a successful download from Google Drive.](../png/gdrive-download-success.png)
*This screenshot shows a successful download of a file from Google Drive using the CLI tool. This demonstrates the other half of the sync functionality.*
*   **Key Takeaway:** The CLI tool can successfully download files from Google Drive.