import os

def create_media_count(media_count_file, png_dir, jpg_dir, mov_dir):
    with open(media_count_file, 'w') as f:
        f.write("# Media Count\n\n")

        # PNG Index
        f.write("## PNG Index\n\n")
        png_files = sorted([p for p in os.listdir(png_dir) if p.endswith('.png')])
        for i, png_file in enumerate(png_files, 1):
            f.write(f"{i}. {png_file}\n")

        # JPG Index
        f.write("\n## JPG Index\n\n")
        jpg_files = sorted([j for j in os.listdir(jpg_dir) if j.endswith('.jpg')])
        for i, jpg_file in enumerate(jpg_files, 1):
            f.write(f"{i}. {jpg_file}\n")

        # MOV Index
        f.write("\n## MOV Index\n\n")
        mov_files = sorted([m for m in os.listdir(mov_dir) if m.endswith('.mov')])
        for i, mov_file in enumerate(mov_files, 1):
            f.write(f"{i}. {mov_file}\n")
    
    print("Media count report created.")

if __name__ == "__main__":
    create_media_count("repos/diy-make/reality-merge/md/media_count.md", "repos/diy-make/reality-merge/png", "repos/diy-make/reality-merge/jpg", "repos/diy-make/reality-merge/mov")

