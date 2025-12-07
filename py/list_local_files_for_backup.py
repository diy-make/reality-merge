#!/usr/bin/env python3

import subprocess

def list_local_files():
    """
    Lists all local files in the repository that are candidates for backup.
    It respects the .gitignore file.
    """
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    return result.stdout.splitlines()

if __name__ == '__main__':
    files = list_local_files()
    for f in files:
        print(f)
