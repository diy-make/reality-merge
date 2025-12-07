import json
from .google_auth import get_google_drive_service
from .reality_merge import find_or_create_folder, set_permissions

ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"

def main():
    """
    Sets the initial Google Drive folder permissions for all users.
    """
    service = get_google_drive_service()
    if not service:
        print("Could not get Google Drive service. Aborting.")
        return

    with open('users.json', 'r') as f:
        users = json.load(f)

    print("--- Setting permissions ---")
    
    # Get the 'users' and 'shared' folder IDs
    users_folder_id = find_or_create_folder(service, "users", ROOT_FOLDER_ID)
    shared_folder_id = find_or_create_folder(service, "shared", ROOT_FOLDER_ID)

    if users_folder_id and shared_folder_id:
        for username, email in users.items():
            print(f"\n--- Setting permissions for {username} ({email}) ---")
            user_folder_id = find_or_create_folder(service, username, users_folder_id)
            if user_folder_id:
                set_permissions(service, user_folder_id, email)
            set_permissions(service, shared_folder_id, email)

    print("\nPermissions setup complete.")

if __name__ == "__main__":
    main()

