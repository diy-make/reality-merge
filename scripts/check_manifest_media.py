import re

def check_media_in_manifest(manifest_file, media_count_file):
    with open(manifest_file, 'r') as f:
        manifest_content = f.read()

    with open(media_count_file, 'r') as f:
        media_count_content = f.read()

    missing_files = []
    for match in re.finditer(r"\*\*(\d+)\. `(png|jpg)/(.+)`\*\*", manifest_content):
        file_name = match.group(3)
        if file_name not in media_count_content:
            missing_files.append(file_name)

    if missing_files:
        print("The following media files from the manifest are not in the media count report:")
        for file in missing_files:
            print(file)
    else:
        print("All media files in the manifest are present in the media count report.")

if __name__ == "__main__":
    check_media_in_manifest("repos/diy-make/reality-merge/md/file_manifest.md", "repos/diy-make/reality-merge/md/media_count.md")
