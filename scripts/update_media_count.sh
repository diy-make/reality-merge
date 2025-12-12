#!/bin/bash

# The media count file
media_count_file="repos/diy-make/reality-merge/md/media_count.md"

# Directories containing the media files
png_dir="repos/diy-make/reality-merge/png"
jpg_dir="repos/diy-make/reality-merge/jpg"

# Directory to search for markdown files
md_dir="repos/diy-make/reality-merge/md"

# Clear the report file
> "$media_count_file"

# Add PNG header
echo "# PNG Index" >> "$media_count_file"
echo "" >> "$media_count_file"

# Find all PNG files, sort them, and add to the report with index and references
find "$png_dir" -name "*.png" | sort | nl -w1 -s'. ' >> "$media_count_file"
find "$png_dir" -name "*.png" -print0 | xargs -0 -I {} bash -c 'echo; echo "**Referenced in:**"; echo "```"; grep -r -n "$(basename "{}")" "$md_dir" --exclude=media_count.md; echo "```"' >> "$media_count_file"


# Add JPG header
echo "" >> "$media_count_file"
echo "# JPG Index" >> "$media_count_file"
echo "" >> "$media_count_file"

# Find all JPG files, sort them, and add to the report with index and references
find "$jpg_dir" -name "*.jpg" | sort | nl -w1 -s'. ' >> "$media_count_file"
find "$jpg_dir" -name "*.jpg" -print0 | xargs -0 -I {} bash -c 'echo; echo "**Referenced in:**"; echo "```"; grep -r -n "$(basename "{}")" "$md_dir" --exclude=media_count.md; echo "```"' >> "$media_count_file"


echo "Media count report updated."