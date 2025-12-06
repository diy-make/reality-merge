import argparse
import os
from datetime import datetime, timezone
from googleapiclient.http import MediaFileUpload
from src.google_auth import get_google_drive_service

# --- CONFIGURATION ---
ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"
SYNC_FOLDER_NAME = "GitHub_with_secrets_push_only"
# Exclude the .git directory and our sensitive token file from being uploaded
EXCLUDE_DIRS = ['.git', '.venv', '__pycache__', 'notion']
EXCLUDE_FILES = ['token.json', '.secrets.baseline']

# --- FUNCTIONS ---

def list_drive_files(folder_id):
    """Lists files in a specific Google Drive folder."""
    service = get_google_drive_service()
    if not service:
        return

    try:
        query = f"'{folder_id}' in parents"
        results = service.files().list(
            q=query,
            pageSize=100,
            fields="nextPageToken, files(id, name)"
        ).execute()
        
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(f"- {item['name']} ({item['id']})")

    except Exception as e:
        print(f"An error occurred while listing files: {e}")

def find_or_create_folder(service, folder_name, parent_id):
    """Finds a folder by name in a parent, or creates it if it doesn't exist."""
    query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    items = results.get('files', [])
    if items:
        folder_id = items[0]['id']
        print(f"Found existing folder: '{folder_name}' ({folder_id})")
        return folder_id
    else:
        print(f"Creating folder: '{folder_name}'...")
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        return folder.get('id')

def sync_directory(service, local_path, parent_drive_id):
    """Recursively syncs a local directory to a Google Drive folder."""
    print(f"Syncing local path: {local_path}")

    # Get remote items
    query = f"'{parent_drive_id}' in parents and trashed=false"
    results = service.files().list(fields="files(id, name, modifiedTime, mimeType)").execute()
    remote_items = {item['name']: {'id': item['id'], 'modifiedTime': item['modifiedTime']} for item in results.get('files', [])}

    # Iterate over local items
    for item_name in os.listdir(local_path):
        local_item_path = os.path.join(local_path, item_name)

        if os.path.isdir(local_item_path):
            if item_name in EXCLUDE_DIRS:
                continue
            
            if item_name in remote_items:
                # Folder exists, recurse
                sync_directory(service, local_item_path, remote_items[item_name]['id'])
            else:
                # Folder doesn't exist, create it and recurse
                print(f"Creating remote directory: {item_name}")
                file_metadata = {'name': item_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_drive_id]}
                new_folder = service.files().create(body=file_metadata, fields='id').execute()
                sync_directory(service, local_item_path, new_folder.get('id'))
        
        elif os.path.isfile(local_item_path):
            if item_name in EXCLUDE_FILES:
                continue

            file_metadata = {'name': item_name, 'parents': [parent_drive_id]}
            media = MediaFileUpload(local_item_path)
            
            if item_name in remote_items:
                # File exists, check modification time
                remote_mtime_str = remote_items[item_name]['modifiedTime']
                remote_mtime = datetime.fromisoformat(remote_mtime_str.replace('Z', '+00:00'))
                local_mtime_utc = datetime.fromtimestamp(os.path.getmtime(local_item_path), tz=timezone.utc)

                if local_mtime_utc > remote_mtime:
                    print(f"Updating remote file: {item_name}")
                    service.files().update(fileId=remote_items[item_name]['id'], media_body=media).execute()
                else:
                    # print(f"Skipping unchanged file: {item_name}")
                    pass
            else:
                # File doesn't exist, upload it
                print(f"Uploading new file: {item_name}")
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()


def handle_upload(args):
    """Wrapper function to handle the one-way push sync."""
    service = get_google_drive_service()
    if not service:
        return
    
    sync_root_id = find_or_create_folder(service, SYNC_FOLDER_NAME, ROOT_FOLDER_ID)
    if sync_root_id:
        sync_directory(service, '.', sync_root_id)
        print("\nSync complete.")


# --- MAIN CLI ---

def main():
    parser = argparse.ArgumentParser(description="Reality Merge CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Drive Command ---
    drive_parser = subparsers.add_parser("drive", help="Google Drive integration")
    drive_subparsers = drive_parser.add_subparsers(dest="drive_command", help="Drive commands")

    # List command
    list_parser = drive_subparsers.add_parser("list", help="List files in the Drive folder")
    list_parser.set_defaults(func=lambda args: list_drive_files(ROOT_FOLDER_ID))

    # Upload command
    upload_parser = drive_subparsers.add_parser("upload", help="Sync the current directory to Google Drive (one-way push)")
    upload_parser.set_defaults(func=handle_upload)


    # --- Argument Parsing ---
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
