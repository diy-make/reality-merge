import re
import os

def update_media_count(media_count_file, md_dir):
    with open(media_count_file, 'r') as f:
        media_count_content = f.read()

    new_content_lines = []
    for line in media_count_content.splitlines():
        new_content_lines.append(line)
        match = re.match(r"^\d+\. (.+)", line)
        if match:
            file_name = match.group(1).strip()
            new_content_lines.append("**Referenced in:**")
            new_content_lines.append("```")
            for root, _, files in os.walk(md_dir):
                for md_file in files:
                    if md_file.endswith('.md'):
                        md_file_path = os.path.join(root, md_file)
                        with open(md_file_path, 'r') as md_f:
                            for line_num, md_line in enumerate(md_f, 1):
                                if file_name in md_line:
                                    new_content_lines.append(f"{md_file_path}:{line_num}")
            new_content_lines.append("```\n")

    with open(media_count_file, 'w') as f:
        f.write("\n".join(new_content_lines))

    print("Media count report updated.")

if __name__ == "__main__":
    update_media_count("repos/diy-make/reality-merge/md/media_count.md", "repos/diy-make/reality-merge/md")