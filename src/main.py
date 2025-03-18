import os
import shutil
from markdown import generate_page

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Get all entries in the content directory
    entries = os.listdir(dir_path_content)

    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir_path, exist_ok=True)

    # Process each entry
    for entry in entries:
        # Create full paths
        entry_path = os.path.join(dir_path_content, entry)

        # If it's a file and has .md extension
        if os.path.isfile(entry_path) and entry.endswith('.md'):
            # Create the destination path, changing .md to .html
            rel_path = os.path.relpath(entry_path, dir_path_content)
            dest_file_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

            # Generate the HTML page
            generate_page(entry_path, template_path, dest_file_path)
            print(f"Generated: {dest_file_path}")

        # If it's a directory, recursively process it
        elif os.path.isdir(entry_path):
            # Create the corresponding directory in the destination
            dest_subdir = os.path.join(dest_dir_path, entry)

            # Recursively process the subdirectory
            generate_pages_recursive(entry_path, template_path, dest_subdir)

def main():
    # Step 1: Delete anything in the public directory
    if os.path.exists("public"):
        shutil.rmtree("public")

    # Step 2: Create public directory if it doesn't exist
    os.makedirs("public", exist_ok=True)

    # Step 3: Copy all static files from static to public
    if os.path.exists("static"):
        copy_static("static", "public")

    # Step 4: Generate the page from content/index.md
    content_dir = "content"
    template_path = "template.html"
    public_dir = "public"

    generate_pages_recursive(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()