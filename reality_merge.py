import argparse
import os
import io
from datetime import datetime, timezone
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from src.google_auth import get_credentials, get_google_drive_service

# --- CONFIGURATION ---
ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"
SYNC_FOLDER_NAME = "main_gemini_only_including_gitignore"
# Exclude directories and files from the upload
EXCLUDE_DIRS = ['.git', '.venv', '__pycache__', 'notion']
EXCLUDE_FILES = ['token.json', '.secrets.baseline']

# --- HELPER FUNCTIONS ---
def _execute_with_retry(request, max_retries=3):
    """Executes a Google API request with a retry mechanism for timeouts."""
    retries = 0
    while True:
        try:
            return request.execute()
        except TimeoutError:
            retries += 1
            if retries > max_retries:
                print("\nOperation failed after multiple timeouts.")
                raise
            print(f"\nOperation timed out. Retrying... (Attempt {retries})")

# --- CORE FUNCTIONS ---

def list_drive_files(folder_id, retry=True):
    """Lists files in a specific Google Drive folder."""
    try:
        service = get_google_drive_service()
        if not service:
            return []

        print(f"Listing files in folder ID: {folder_id}")
        query = f"'{folder_id}' in parents and trashed=false"
        request = service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        )
        results = _execute_with_retry(request)
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(f"- {item['name']} ({item['id']})")
        return items

    except HttpError as err:
        if err.resp.status in [403, 404] and retry:
            print("\n--- ERROR: Could not access Google Drive folder. ---")
            print("This may be due to stale permissions or an incorrect folder ID.")
            print("Attempting to fix by re-authenticating...")
            
            token_path = 'token.json'
            if os.path.exists(token_path):
                os.remove(token_path)
                print("Removed old authentication token.")

            print("Please follow the browser authentication steps again.")
            new_service = get_google_drive_service(force_reauth=True)
            if new_service:
                return list_drive_files(folder_id, retry=False)
        else:
            print(f"An error occurred while listing files: {err}")
        return []

def find_or_create_folder(service, folder_name, parent_id):
    """Finds a folder by name in a parent, or creates it if it doesn't exist."""
    query = f"name='{folder_name}' and '{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    request = service.files().list(
        q=query, 
        fields="files(id)", 
        supportsAllDrives=True, 
        includeItemsFromAllDrives=True
    )
    results = _execute_with_retry(request)
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
        create_request = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True)
        folder = _execute_with_retry(create_request)
        return folder.get('id')

def sync_directory(service, local_path, parent_drive_id):
    """Recursively syncs a local directory to a Google Drive folder."""
    print(f"Syncing local path: '{local_path}'")

    query = f"'{parent_drive_id}' in parents and trashed=false"
    list_request = service.files().list(
        fields="files(id, name, modifiedTime, mimeType)", 
        supportsAllDrives=True, 
        includeItemsFromAllDrives=True,
        q=query
    )
    results = _execute_with_retry(list_request)
    remote_items = {item['name']: {'id': item['id'], 'modifiedTime': item['modifiedTime']} for item in results.get('files', [])}

    for item_name in os.listdir(local_path):
        local_item_path = os.path.join(local_path, item_name)

        if os.path.isdir(local_item_path):
            if item_name in EXCLUDE_DIRS or item_name.startswith('.'):
                continue
            
            if item_name in remote_items:
                sync_directory(service, local_item_path, remote_items[item_name]['id'])
            else:
                print(f"Creating remote directory: '{local_item_path}'")
                file_metadata = {'name': item_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [parent_drive_id]}
                create_request = service.files().create(body=file_metadata, fields='id', supportsAllDrives=True)
                new_folder = _execute_with_retry(create_request)
                sync_directory(service, local_item_path, new_folder.get('id'))
        
        elif os.path.isfile(local_item_path):
            if item_name in EXCLUDE_FILES or item_name.startswith('.'):
                continue

            media = MediaFileUpload(local_item_path, resumable=True)
            
            if item_name in remote_items:
                remote_mtime_str = remote_items[item_name]['modifiedTime']
                remote_mtime = datetime.fromisoformat(remote_mtime_str.replace('Z', '+00:00'))
                local_mtime_utc = datetime.fromtimestamp(os.path.getmtime(local_item_path), tz=timezone.utc)

                if local_mtime_utc > remote_mtime:
                    print(f"Updating remote file: '{local_item_path}'")
                    update_request = service.files().update(fileId=remote_items[item_name]['id'], media_body=media, supportsAllDrives=True)
                    _execute_with_retry(update_request)
            else:
                print(f"Uploading new file: '{local_item_path}'")
                file_metadata = {'name': item_name, 'parents': [parent_drive_id]}
                create_request = service.files().create(body=file_metadata, media_body=media, fields='id', supportsAllDrives=True)
                _execute_with_retry(create_request)

# --- COMMAND HANDLERS ---

def handle_upload(args, retry=True):
    """Wrapper function to handle the one-way push sync."""
    try:
        service = get_google_drive_service()
        if not service: return

        local_path = args.local_path
        dest_folder_name = args.dest_folder if args.dest_folder else SYNC_FOLDER_NAME
        
        print(f"--- Starting Sync ---")
        print(f"Local source: '{local_path}'")
        print(f"Remote destination: '{dest_folder_name}'")
        
        sync_root_id = find_or_create_folder(service, dest_folder_name, ROOT_FOLDER_ID)
        if sync_root_id:
            sync_directory(service, local_path, sync_root_id)
            print("\nSync complete.")

    except HttpError as err:
        if err.resp.status in [403, 404] and retry:
            print("\n--- ERROR: Permission or Not Found issue during sync. ---")
            print("Attempting to fix by re-authenticating...")
            
            token_path = 'token.json'
            if os.path.exists(token_path):
                os.remove(token_path)
                print("Removed old authentication token.")

            print("Please follow the browser authentication steps again.")
            new_service = get_google_drive_service(force_reauth=True)
            if new_service:
                handle_upload(args, retry=False)
        else:
            print(f"An error occurred during sync: {err}")

def handle_download(args, service=None):
    """Handles downloading a file from Google Drive."""
    if not service:
        service = get_google_drive_service()
        if not service: return

    file_id = args.file_id if hasattr(args, 'file_id') else args
    try:
        file_metadata = service.files().get(fileId=file_id, supportsAllDrives=True).execute()
        file_name = file_metadata['name']
        print(f"Starting download for '{file_name}'...")

        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        retries = 0
        while done is False:
            try:
                status, done = downloader.next_chunk()
                if status: print(f"Download {int(status.progress() * 100)}%.")
            except TimeoutError:
                retries += 1
                if retries > 3:
                    print("\nDownload failed after multiple timeouts.")
                    return False
                print(f"\nDownload timed out. Retrying... (Attempt {retries})")
        
        with open(file_name, 'wb') as f:
            f.write(fh.getvalue())
        print(f"\nSuccessfully downloaded '{file_name}'.")
        return True

    except HttpError as err:
        print(f"An error occurred while downloading the file: {err}")
        return False

def download_google_doc_as_md(args):
    # ... (existing function, no changes)
    creds = get_credentials()
    if not creds: return

    document_id = args.file_id
    try:
        docs_service = build("docs", "v1", credentials=creds)
        print(f"Fetching Google Doc: {document_id}")
        document = docs_service.documents().get(documentId=document_id).execute()
        
        doc_title = document.get('title', 'Untitled')
        file_name = f"{doc_title.replace(' ', '_')}.md"
        print(f"Converting '{doc_title}' to Markdown ('{file_name}')...")

        content = document.get('body').get('content')
        md_content = f"# {doc_title}\n\n"
        
        for element in content:
            if "paragraph" in element:
                p = element.get("paragraph")
                p_elements = p.get("elements")
                line_md = ""
                for elm in p_elements:
                    if "textRun" in elm:
                        text_run = elm.get("textRun")
                        text_content = text_run.get("content").strip('\n')
                        if not text_content: continue
                        
                        style = text_run.get("textStyle", {})
                        if style.get('link'):
                            url = style.get('link').get('url')
                            if url: text_content = f"[{text_content}]({url})"
                        if style.get('italic'): text_content = f"*{text_content}*"
                        if style.get('bold'): text_content = f"**{text_content}**"
                        line_md += text_content
                
                if not line_md.strip():
                    md_content += "\n"
                    continue

                p_style = p.get("paragraphStyle", {})
                named_style = p_style.get("namedStyleType")
                if p.get('bullet') is not None: md_content += f"* {line_md}\n"
                elif named_style == "TITLE": pass
                elif named_style == "SUBTITLE": md_content += f"## {line_md}\n\n"
                elif named_style == "HEADING_1": md_content += f"# {line_md}\n\n"
                elif named_style == "HEADING_2": md_content += f"## {line_md}\n\n"
                elif named_style == "HEADING_3": md_content += f"### {line_md}\n\n"
                else: md_content += f"{line_md}\n\n"
        
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"Successfully converted and saved to '{file_name}'.")

    except HttpError as err:
        print(f"An error occurred while converting the Google Doc: {err}")

def handle_move(args):
    # ... (existing function, no changes)
    service = get_google_drive_service()
    if not service: return

    file_id, folder_id = args.file_id, args.folder_id
    try:
        file = service.files().get(fileId=file_id, fields='parents', supportsAllDrives=True).execute()
        previous_parents = ",".join(file.get('parents'))
        file = service.files().update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields='id, parents',
            supportsAllDrives=True
        ).execute()
        print(f"Successfully moved file ID '{file_id}' to folder ID '{folder_id}'.")
    except HttpError as err:
        print(f"An error occurred while moving the file: {err}")

def handle_delete(args):
    """Handles deleting a file from Google Drive."""
    service = get_google_drive_service()
    if not service: return

    file_id = args.file_id if hasattr(args, 'file_id') else args
    try:
        service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        print(f"Successfully deleted file ID '{file_id}'.")
        return True
    except HttpError as err:
        print(f"An error occurred while deleting the file: {err}")
        return False

def handle_process(args):
    """Downloads all files from a folder and then deletes them."""
    service = get_google_drive_service()
    if not service: return

    folder_id = args.folder_id
    print(f"--- Starting to process folder '{folder_id}' ---")
    
    files_to_process = list_drive_files(folder_id)
    if not files_to_process:
        print("No files to process.")
        return

    for file in files_to_process:
        file_id = file['id']
        # Mimic argparse object for handle_download
        download_args = argparse.Namespace(file_id=file_id)
        print("-" * 20)
        if handle_download(download_args, service=service):
            # Only delete if download was successful
            handle_delete(file_id)
    
    print("\n--- Finished processing folder. ---")


# --- MAIN CLI ---

def main():
    parser = argparse.ArgumentParser(description="Reality Merge CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    drive_parser = subparsers.add_parser("drive", help="Google Drive integration")
    drive_subparsers = drive_parser.add_subparsers(dest="drive_command", help="Drive commands")

    list_parser = drive_subparsers.add_parser("list", help="List files in the Drive folder")
    list_parser.add_argument("folder_id", nargs='?', default=ROOT_FOLDER_ID, help="The ID of the folder to list (defaults to ROOT_FOLDER_ID)")
    list_parser.set_defaults(func=lambda args: list_drive_files(args.folder_id))

    upload_parser = drive_subparsers.add_parser("upload", help="Sync a local directory to a Google Drive folder")
    upload_parser.add_argument("local_path", default='.', nargs='?', help="Local directory to upload (defaults to current dir)")
    upload_parser.add_argument("--dest", dest="dest_folder", default=None, help=f"Destination folder name (defaults to {SYNC_FOLDER_NAME})")
    upload_parser.set_defaults(func=handle_upload)

    download_parser = drive_subparsers.add_parser("download", help="Download a binary file from Google Drive")
    download_parser.add_argument("file_id", help="The ID of the file to download")
    download_parser.set_defaults(func=handle_download)

    download_doc_parser = drive_subparsers.add_parser("download_doc", help="Download a Google Doc as Markdown")
    download_doc_parser.add_argument("file_id", help="The ID of the Google Doc to download")
    download_doc_parser.set_defaults(func=download_google_doc_as_md)

    move_parser = drive_subparsers.add_parser("move", help="Move a file to a new folder in Google Drive")
    move_parser.add_argument("file_id", help="The ID of the file to move")
    move_parser.add_argument("folder_id", help="The ID of the destination folder")
    move_parser.set_defaults(func=handle_move)

    delete_parser = drive_subparsers.add_parser("delete", help="Delete a file from Google Drive")
    delete_parser.add_argument("file_id", help="The ID of the file to delete")
    delete_parser.set_defaults(func=handle_delete)

    process_parser = drive_subparsers.add_parser("process", help="Downloads and then deletes all files in a folder")
    process_parser.add_argument("folder_id", help="The ID of the folder to process")
    process_parser.set_defaults(func=handle_process)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
