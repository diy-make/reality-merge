import re
import os

def find_unlisted_media(all_links_file, media_count_file):
    with open(all_links_file, 'r') as f:
        all_links_content = f.read()

    with open(media_count_file, 'r') as f:
        media_count_content = f.read()

    unlisted_media = set()

    for link in re.finditer(r'\((\.\./)+(png|jpg)/(.+)\)', all_links_content):
        file_name = link.group(3)
        if file_name not in media_count_content:
            unlisted_media.add(file_name)

    if unlisted_media:
        print("Unlisted media files:")
        for file in unlisted_media:
            print(file)
    else:
        print("All media files are listed.")

if __name__ == "__main__":
    find_unlisted_media("all_links.txt", "repos/diy-make/reality-merge/md/media_count.md")
