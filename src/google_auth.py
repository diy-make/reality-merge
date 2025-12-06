import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---

# Define scopes required for the application
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents.readonly"
]

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, '..', 'token.json')
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, '..', 'client_secret.json')

# --- FUNCTIONS ---

def get_credentials(force_reauth=False):
    """Handles user authentication and returns valid credentials."""
    creds = None
    if not force_reauth and os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Attempting to re-authenticate from scratch.")
                creds = None
        
        if not creds:
            if not os.path.exists(CLIENT_SECRET_PATH):
                print(f"ERROR: client_secret.json not found at '{CLIENT_SECRET_PATH}'")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    
    return creds

def get_google_drive_service(force_reauth=False):
    """Builds and returns a Google Drive API service object."""
    creds = get_credentials(force_reauth=force_reauth)
    if not creds:
        return None
    try:
        service = build("drive", "v3", credentials=creds)
        print("Successfully authenticated with Google Drive API.")
        return service
    except HttpError as err:
        print(f"An error occurred building the Drive service: {err}")
        return None

def main():
    """Main function to trigger the authentication flow."""
    print("Attempting to get Google credentials...")
    get_credentials()
    print("Authentication flow complete.")

if __name__ == "__main__":
    main()
