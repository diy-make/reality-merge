import re
import os

def update_media_count(media_count_file, md_dir):
    with open(media_count_file, 'r') as f:
        media_count_content = f.read()

    new_content_lines = []
    
    # Create a dictionary to store references for each media file
    media_references = {}

    # First pass: collect all references
    for root, _, files in os.walk(md_dir):
        for md_file in files:
            if md_file.endswith('.md') and md_file != 'media_count.md':
                md_file_path = os.path.join(root, md_file)
                with open(md_file_path, 'r') as md_f:
                    for line_num, md_line in enumerate(md_f, 1):
                        # Find all media files in the line
                        for media_type in ['png', 'jpg', 'mov']:
                            for match in re.finditer(r'(\d+-\S+\.' + media_type + r'|photo\S+\.' + media_type + r')', md_line):
                                file_name = match.group(1)
                                if file_name not in media_references:
                                    media_references[file_name] = set()
                                media_references[file_name].add(f"{md_file_path}:{line_num}")

    # Second pass: write the new media_count.md
    for line in media_count_content.splitlines():
        new_content_lines.append(line)
        match = re.match(r"^\d+\. (.+)", line)
        if match:
            file_name = match.group(1).strip()
            if file_name in media_references:
                new_content_lines.append("**Referenced in:**")
                new_content_lines.append("```")
                new_content_lines.extend(sorted(list(media_references[file_name])))
                new_content_lines.append("```\n")

    with open(media_count_file, 'w') as f:
        f.write("\n".join(new_content_lines))

    print("Media count report updated.")

if __name__ == "__main__":
    update_media_count("repos/diy-make/reality-merge/md/media_count.md", "repos/diy-make/reality-merge/md")
