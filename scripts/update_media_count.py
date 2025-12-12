import re
import os

def update_media_count(media_count_file, png_dir, jpg_dir, mov_dir, md_dir):
    with open(media_count_file, 'w') as f:
        f.write("# Media Count\n\n")

        # PNG Index
        f.write("## PNG Index\n\n")
        png_files = sorted([p for p in os.listdir(png_dir) if p.endswith('.png')])
        for i, png_file in enumerate(png_files, 1):
            f.write(f"{i}. [{png_file}](../png/{png_file})\n")

        # JPG Index
        f.write("\n## JPG Index\n\n")
        jpg_files = sorted([j for j in os.listdir(jpg_dir) if j.endswith('.jpg')])
        for i, jpg_file in enumerate(jpg_files, 1):
            f.write(f"{i}. [{jpg_file}](../jpg/{jpg_file})\n")

        # MOV Index
        f.write("\n## MOV Index\n\n")
        mov_files = sorted([m for m in os.listdir(mov_dir) if m.endswith('.mov')])
        for i, mov_file in enumerate(mov_files, 1):
            f.write(f"{i}. [{mov_file}](../mov/{mov_file})\n")
    
    print("Media count report created.")

    with open(media_count_file, 'r') as f:
        media_count_content = f.read()

    new_content_lines = []
    for line in media_count_content.splitlines():
        new_content_lines.append(line)
        match = re.match(r"^\d+\. \[(.+)\]\(.+\)", line)
        if match:
            file_name = match.group(1).strip()
            references = []
            for root, _, files in os.walk(md_dir):
                for md_file in files:
                    if md_file.endswith('.md') and md_file != 'media_count.md':
                        md_file_path = os.path.join(root, md_file)
                        with open(md_file_path, 'r') as md_f:
                            for line_num, md_line in enumerate(md_f, 1):
                                if file_name in md_line:
                                    # make the md_file_path a link
                                    relative_path = os.path.relpath(md_file_path, os.path.dirname(media_count_file))
                                    references.append(f"[{md_file_path}:{line_num}]({relative_path})")
            if references:
                new_content_lines.append("**Referenced in:**")
                new_content_lines.append("```")
                new_content_lines.extend(references)
                new_content_lines.append("```\n")

    with open(media_count_file, 'w') as f:
        f.write("\n".join(new_content_lines))
    
    print("Media count report updated with references.")


if __name__ == "__main__":
    update_media_count(
        "repos/diy-make/reality-merge/md/media_count.md",
        "repos/diy-make/reality-merge/png",
        "repos/diy-make/reality-merge/jpg",
        "repos/diy-make/reality-merge/mov",
        "repos/diy-make/reality-merge/md"
    )