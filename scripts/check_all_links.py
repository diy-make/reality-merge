import re
import os
import requests

def check_all_links(all_links_file, base_repo_path, broken_links_file):
    with open(all_links_file, 'r') as f:
        all_links_content = f.read()

    broken_links = []
    
    for md_file_section in all_links_content.split('## Links in '):
        if not md_file_section.strip():
            continue

        parts = md_file_section.strip().split('\n', 1)
        md_file_full_path = parts[0].strip()
        links_section = parts[1] if len(parts) > 1 else ""

        for line_num, link_line in enumerate(links_section.splitlines(), 1):
            # Regex to find markdown links and direct URLs
            match_md = re.search(r'\[.*?\]\((.+?)\)', link_line)
            match_url = re.search(r'http[s]?://[^\s\)]+', link_line)
            
            link = None
            if match_md:
                link = match_md.group(1)
            elif match_url:
                link = match_url.group(0)

            if link:
                if link.startswith('http'):
                    try:
                        response = requests.head(link, timeout=5)
                        if response.status_code >= 400:
                            broken_links.append(f"Broken external link: {link} in {md_file_full_path}:{line_num}")
                    except requests.exceptions.RequestException as e:
                        broken_links.append(f"Could not check external link: {link} in {md_file_full_path}:{line_num} - {e}")
                else:
                    # Local link
                    # Construct the absolute path
                    # md_file_full_path is something like "repos/diy-make/reality-merge/md/day_1/summary.md"
                    # link is something like "../../png/image.png"
                    
                    # Need to resolve the relative path correctly from the base_repo_path
                    
                    # Get the directory of the markdown file relative to the base_repo_path
                    md_file_relative_dir = os.path.dirname(os.path.relpath(md_file_full_path, base_repo_path))
                    
                    # Join the markdown file's relative directory with the link
                    resolved_link_path = os.path.normpath(os.path.join(md_file_relative_dir, link))
                    
                    # Construct the full absolute path
                    full_local_path = os.path.join(base_repo_path, resolved_link_path)
                    
                    print(f"Checking local link: {link} from {md_file_full_path} -> resolved to {full_local_path}")
                    
                    if not os.path.exists(full_local_path):
                        broken_links.append(f"Broken local link: {link} in {md_file_full_path}:{line_num} (resolved to {full_local_path})")

    if broken_links:
        with open(broken_links_file, 'w') as f:
            for broken_link in broken_links:
                f.write(broken_link + '\n')
        print(f"Broken links found and saved to {broken_links_file}")
    else:
        print("All links are valid.")

if __name__ == "__main__":
    check_all_links("repos/diy-make/reality-merge/txt/all_links.txt", "repos/diy-make/reality-merge", "broken_links.txt")
