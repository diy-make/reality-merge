import argparse
import json
from google_auth import get_google_drive_service
from reality_merge import handle_download, download_google_doc_as_md

def main():
    parser = argparse.ArgumentParser(description="Download files from Google Drive.")
    parser.add_argument("--files", required=True, help="JSON string of files to download.")
    parser.add_argument("--output-dir", default="shared", help="The directory to download the files to.")
    args = parser.parse_args()

    files_to_download = json.loads(args.files)
    service = get_google_drive_service()

    if not service:
        print("Could not get Google Drive service. Aborting.")
        return

    for f in files_to_download:
        download_args = argparse.Namespace(file_id=f['id'])
        if f.get('mimeType') == 'application/vnd.google-apps.document':
            download_google_doc_as_md(download_args, output_dir=args.output_dir)
        else:
            handle_download(download_args, service=service, output_dir=args.output_dir)

if __name__ == "__main__":
    main()
