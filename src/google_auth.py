import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---

# Define scopes for Google Drive API.
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, '..', 'token.json')
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, '..', 'client_secret.json')

# --- FUNCTIONS ---

def get_google_drive_service(force_reauth=False):
    """Handles authentication and builds a Google Drive API service object."""
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
                creds = None # Force re-authentication
        
        if not creds:
            if not os.path.exists(CLIENT_SECRET_PATH):
                print(f"ERROR: client_secret.json not found at '{CLIENT_SECRET_PATH}'")
                print("Please download it from your Google Cloud project and place it in the project root.")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        print("Successfully authenticated with Google Drive API.")
        return service
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def main():
    """Main function to trigger the authentication flow."""
    print("Attempting to authenticate with Google Drive...")
    get_google_drive_service()

if __name__ == "__main__":
    main()
