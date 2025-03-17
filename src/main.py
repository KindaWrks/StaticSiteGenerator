import os
import shutil


def copy_static(src, dst):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst):
        os.mkdir(dst)

    # Get a list of all items in the source directory
    items = os.listdir(src)

    # Loop through each item
    for item in items:
        # Create full paths
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        # If the item is a file, copy it
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied file: {src_path} to {dst_path}")
        else:
            # If it's a directory, recursively copy it
            copy_static(src_path, dst_path)

def main():
    if os.path.exists("public"):
       shutil.rmtree("public")
    os.mkdir("public")
    copy_static("static", "public")


if __name__ == "__main__":
    main()