#!/usr/bin/env python3

import subprocess
import argparse
import json
from google_auth import get_google_drive_service
from reality_merge import find_or_create_folder, _execute_with_retry

ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"

def list_local_files():
    """
    Lists all local files in the repository that are candidates for backup.
    It respects the .gitignore file.
    """
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    return result.stdout.splitlines()

def list_drive_files(service, folder_id):
    """Lists files in a specific Google Drive folder."""
    query = f"'{folder_id}' in parents and trashed=false"
    request = service.files().list(
        q=query,
        pageSize=1000,
        fields="files(id, name, mimeType, size)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True
    )
    results = _execute_with_retry(request)
    return results.get('files', [])

def main():
    parser = argparse.ArgumentParser(description="Compare local files with the remote backup on Google Drive.")
    parser.add_argument("--folder-name", default="backup", help="The name of the folder to compare.")
    args = parser.parse_args()

    service = get_google_drive_service()
    if not service:
        print("Could not get Google Drive service. Aborting.")
        return

    folder_id = find_or_create_folder(service, args.folder_name, ROOT_FOLDER_ID)
    if folder_id:
        remote_files_list = list_drive_files(service, folder_id)
        remote_files = {f['name'] for f in remote_files_list}
        
        local_files = set(list_local_files())
        
        new_files = local_files - remote_files
        
        print(f"Found {len(new_files)} new files to upload:")
        for f in sorted(new_files):
            print(f)

if __name__ == "__main__":
    main()
