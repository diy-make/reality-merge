#!/bin/bash
md_dir="repos/diy-make/reality-merge/md"
output_file="all_links.txt"
> "$output_file"
find "$md_dir" -name "*.md" -print0 | while IFS= read -r -d $'
' md_file; do
  echo "## Links in $md_file" >> "$output_file"
  grep -o -E '\!\\[.*?\\]\((?:\\.\\.\/)+(png|jpg)\\/(.+?)\\)' "$md_file" | sed -E 's/!\\[.*?\\]\((.*)\\/\\1/' >> "$output_file"
  grep -o -E '\[.*?\\]\((?:\\.\\.\/)+(png|jpg)\\/(.+?)\\)' "$md_file" | sed -E 's/\[.*?\\]\((.*)\\/\\1/' >> "$output_file"
  grep -o -E 'http[s]?://[^)]+' "$md_file" >> "$output_file"
  echo "" >> "$output_file"
done
echo "All links extracted to $output_file"