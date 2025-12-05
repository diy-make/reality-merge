import argparse
import os
from src.google_auth import get_google_drive_service

# --- CONFIGURATION ---
FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"

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
            pageSize=10,
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


# --- MAIN CLI ---

def main():
    parser = argparse.ArgumentParser(description="Reality Merge CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- Drive Command ---
    drive_parser = subparsers.add_parser("drive", help="Google Drive integration")
    drive_subparsers = drive_parser.add_subparsers(dest="drive_command", help="Drive commands")

    # List command
    list_parser = drive_subparsers.add_parser("list", help="List files in the Drive folder")
    list_parser.set_defaults(func=lambda args: list_drive_files(FOLDER_ID))

    # --- Argument Parsing ---
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
