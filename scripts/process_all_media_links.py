import re
import os

def process_all_media_links(all_links_file, media_count_file, base_repo_path):
    with open(all_links_file, 'r') as f:
        all_links_content = f.read()

    # Read media_count.md once to build a lookup for existing media
    with open(media_count_file, 'r') as f:
        current_media_count_content = f.read()
    
    # To store new references before writing back
    new_references_to_add = {} # {media_name: [list_of_references]}

    for md_file_section in all_links_content.split('## Links in '):
        if not md_file_section.strip():
            continue

        parts = md_file_section.strip().split('\n', 1)
        md_file_full_path = parts[0].strip() # e.g., repos/diy-make/reality-merge/md/day_1/Screenshots.md
        links_section = parts[1] if len(parts) > 1 else ""

        for line_num, link_line in enumerate(links_section.splitlines(), 1):
            # Regex to find markdown image links
            match_md_img = re.search(r'\((?:\.\./)+(png|jpg)/([^)]+?)\)', link_line)

            if match_md_img:
                media_type = match_md_img.group(1)
                file_name = match_md_img.group(2)
                
                # Ensure the media file is represented in new_references_to_add
                if file_name not in new_references_to_add:
                    new_references_to_add[file_name] = []
                
                # Add reference if not already present for this media file
                reference_entry = f"{md_file_full_path}:{line_num}"
                if reference_entry not in new_references_to_add[file_name]:
                    new_references_to_add[file_name].append(reference_entry)

    # Now, reconstruct media_count.md based on original content and new references
    final_media_count_content_lines = []
    
    # Process existing entries in order
    for line in current_media_count_content.splitlines():
        final_media_count_content_lines.append(line)
        match = re.search(r'^\d+\. repos/diy-make/reality-merge/(png|jpg)/(.+)', line)
        if match:
            media_name_from_line = match.group(2)
            if media_name_from_line in new_references_to_add:
                final_media_count_content_lines.append("**Referenced in:**")
                final_media_count_content_lines.append("```")
                for ref in new_references_to_add[media_name_from_line]:
                    final_media_count_content_lines.append(ref)
                final_media_count_content_lines.append("```")

    # Write the updated content back to media_count.md
    with open(media_count_file, 'w') as f:
        f.write("\n".join(final_media_count_content_lines))
    
    print("Media count report updated.")


if __name__ == "__main__":
    process_all_media_links("all_links.txt", "repos/diy-make/reality-merge/md/media_count.md", "repos/diy-make/reality-merge")
