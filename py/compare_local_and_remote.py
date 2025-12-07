import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Compare local and remote file lists.")
    parser.add_argument("--remote-files", required=True, help="JSON string of remote files.")
    parser.add_argument("--local-dir", default="shared", help="The local directory to compare against.")
    args = parser.parse_args()

    remote_files = json.loads(args.remote_files)
    local_files = [f for f in os.listdir(args.local_dir) if os.path.isfile(os.path.join(args.local_dir, f))]

    new_files = []
    for remote_file in remote_files:
        if remote_file['name'] not in local_files:
            new_files.append(remote_file)

    print(json.dumps(new_files))

if __name__ == "__main__":
    main()
