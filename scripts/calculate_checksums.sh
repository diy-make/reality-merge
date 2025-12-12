#!/bin/bash

# Directory containing the JPG files
jpg_dir="repos/diy-make/reality-merge/jpg"

# Calculate checksums and save to a file
find "$jpg_dir" -type f -name "*.jpg" -print0 | xargs -0 sha256sum > checksums.txt

echo "Checksums calculated and saved to checksums.txt"
