#!/usr/bin/env python3

import argparse
import os
from googleapiclient.http import MediaFileUpload
from google_auth import get_google_drive_service
from reality_merge import find_or_create_folder, _execute_with_retry
from compare_local_and_remote_backup import list_local_files, list_drive_files

ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"

def upload_files(service, files_to_upload, parent_drive_id):
    """Uploads a list of files to a Google Drive folder."""
    for file_path in files_to_upload:
        print(f"Uploading new file: '{file_path}'")
        file_metadata = {'name': os.path.basename(file_path), 'parents': [parent_drive_id]}
        media = MediaFileUpload(file_path, resumable=True)
        create_request = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True)
        _execute_with_retry(create_request)

def main():
    parser = argparse.ArgumentParser(description="Upload new files to the remote backup on Google Drive.")
    parser.add_argument("--folder-name", default="backup", help="The name of the folder to upload to.")
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
        
        if new_files:
            upload_files(service, sorted(new_files), folder_id)
            print("\nUpload complete.")
        else:
            print("No new files to upload.")

if __name__ == "__main__":
    main()
