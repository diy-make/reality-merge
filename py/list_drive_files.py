import argparse
import json
from google_auth import get_google_drive_service
from reality_merge import find_or_create_folder, _execute_with_retry

ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"

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
    parser = argparse.ArgumentParser(description="List files in the shared Google Drive folder.")
    parser.add_argument("--folder-name", default="shared", help="The name of the folder to list.")
    args = parser.parse_args()

    service = get_google_drive_service()
    if not service:
        print("Could not get Google Drive service. Aborting.")
        return

    folder_id = find_or_create_folder(service, args.folder_name, ROOT_FOLDER_ID)
    if folder_id:
        files = list_drive_files(service, folder_id)
        print(json.dumps(files))

if __name__ == "__main__":
    main()
