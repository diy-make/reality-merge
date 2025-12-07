from google_auth import get_google_drive_service
from reality_merge import find_or_create_folder

ROOT_FOLDER_ID = "1falCGVO_jTZTpp8IH619nU71JIT8ZRB3"
USERS = ["apemake", "vdharvey", "ptayab", "Galanafai"]

def main():
    """
    Sets up the initial Google Drive folder structure.
    """
    service = get_google_drive_service()
    if not service:
        print("Could not get Google Drive service. Aborting.")
        return

    print("--- Creating root folders ---")
    users_folder_id = find_or_create_folder(service, "users", ROOT_FOLDER_ID)
    find_or_create_folder(service, "shared", ROOT_FOLDER_ID)

    if users_folder_id:
        print("\n--- Creating user folders ---")
        for user in USERS:
            user_folder_id = find_or_create_folder(service, user, users_folder_id)
            if user_folder_id:
                find_or_create_folder(service, "inbox", user_folder_id)
                find_or_create_folder(service, "backup", user_folder_id)
    
    print("\nFolder structure setup complete.")

if __name__ == "__main__":
    main()

