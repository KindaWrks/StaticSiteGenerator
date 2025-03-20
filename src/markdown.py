import os

from textnode import TextNode, markdown_to_blocks, block_to_block_type, text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode


def split_markdown_into_blocks(markdown):
    return markdown_to_blocks(markdown)


def determine_block_type(block):
    return block_to_block_type(block)


def text_to_children(text_or_nodes):
    children = []

    # If it's a string, convert it to TextNodes using inline_markdown_to_textnodes
    if isinstance(text_or_nodes, str):
        text_nodes = inline_markdown_to_textnodes(text_or_nodes)
    else:
        # Use the provided list of TextNodes
        text_nodes = text_or_nodes

    # Process each TextNode - same logic for both cases
    for text_node in text_nodes:
        if text_node.text_type == "text":
            children.append(LeafNode(None, text_node.text))
        elif text_node.text_type == "italic":
            # Create a parent node with 'i' tag for italic text
            children.append(ParentNode("i", [LeafNode(None, text_node.text)]))
        elif text_node.text_type == "bold":
            # Create a parent node with 'b' tag for bold text
            children.append(ParentNode("b", [LeafNode(None, text_node.text)]))
        elif text_node.text_type == "code":
            # Create a parent node with 'code' tag for code
            children.append(ParentNode("code", [LeafNode(None, text_node.text)]))
        elif text_node.text_type == "link":
            # Create an 'a' tag with href attribute for links
            children.append(ParentNode("a", [LeafNode(None, text_node.text)], {"href": text_node.url}))
        elif text_node.text_type == "image":
            # Create an 'img' tag with src and alt attributes for images
            children.append(LeafNode("img", None, {"src": text_node.url, "alt": text_node.text}))
    return children

def inline_markdown_to_textnodes(text):
    nodes = []
    i = 0

    while i < len(text):

        # Handle inline code with backticks
        if text[i] == '`' and i + 1 < len(text):
            end = text.find('`', i + 1)
            if end != -1:
                # If there's text before the code, add it as regular text
                if i > 0:
                    nodes.append(TextNode(text[:i], "text"))

                # Add the code text
                nodes.append(TextNode(text[i + 1:end], "code"))

                # Continue processing the rest of the text
                text = text[end + 1:]
                i = 0
                continue

        # Handle links [text](url)
        if text[i] == '[':
            closing_bracket = text.find(']', i)
            if closing_bracket != -1 and closing_bracket + 1 < len(text) and text[closing_bracket + 1] == '(':
                opening_paren = closing_bracket + 1
                closing_paren = text.find(')', opening_paren)
                if closing_paren != -1:
                    # If there's text before the link, add it as regular text
                    if i > 0:
                        nodes.append(TextNode(text[:i], "text"))

                    # Add the link
                    link_text = text[i + 1:closing_bracket]
                    url = text[opening_paren + 1:closing_paren]
                    nodes.append(TextNode(link_text, "link", url))

                    # Continue processing the rest of the text
                    text = text[closing_paren + 1:]
                    i = 0
                    continue

        if text[i:i + 2] == '![' and i + 2 < len(text):
            closing_bracket = text.find(']', i)
            if closing_bracket != -1 and closing_bracket + 1 < len(text) and text[closing_bracket + 1] == '(':
                opening_paren = closing_bracket + 1
                closing_paren = text.find(')', opening_paren)
                if closing_paren != -1:
                    # If there's text before the image, add it as regular text
                    if i > 0:
                        nodes.append(TextNode(text[:i], "text"))

                    # Add the image
                    alt_text = text[i + 2:closing_bracket]
                    url = text[opening_paren + 1:closing_paren]
                    nodes.append(TextNode(alt_text, "image", url))

                    # Continue processing the rest of the text
                    text = text[closing_paren + 1:]
                    i = 0
                    continue

        # Handle bold with double asterisks
        if text[i:i+2] == '**' and i + 2 < len(text):
            end = text.find('**', i + 2)
            if end != -1:
                # If there's text before the bold, add it as regular text
                if i > 0:
                    nodes.append(TextNode(text[:i], "text"))

                # Add the bold text
                nodes.append(TextNode(text[i + 2:end], "bold"))

                # Continue processing the rest of the text
                text = text[end + 2:]
                i = 0
                continue

        # Handle italic with underscore
        if text[i] == '_' and i + 1 < len(text):
            end = text.find('_', i + 1)
            if end != -1:
                # If there's text before the italic, add it as regular text
                if i > 0:
                    nodes.append(TextNode(text[:i], "text"))

                # Add the italic text
                nodes.append(TextNode(text[i + 1:end], "italic"))

                # Continue processing the rest of the text
                text = text[end + 1:]
                i = 0
                continue

        # Handle other inline elements similarly...
        i += 1

    # Add any remaining text
    if text:
        nodes.append(TextNode(text, "text"))

    return nodes

def paragraph_to_html_node(paragraph):
    text_nodes = inline_markdown_to_textnodes(paragraph)
    children = text_to_children(text_nodes)
    return ParentNode("p", children)

def markdown_to_html_node(markdown):
    # Create a parent div node
    parent = ParentNode("div", [])

    # Split markdown into blocks
    blocks = split_markdown_into_blocks(markdown)

    # Process each block
    for block in blocks:
        # Determine block type
        block_type = determine_block_type(block)

        if block_type == "paragraph":
            # Create paragraph node
            paragraph_node = paragraph_to_html_node(block)
            parent.children.append(paragraph_node)

        elif block_type == "heading":
            # Determine heading level (h1, h2, etc.)
            # Count the # symbols at the start
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            level = min(level, 6)  # HTML only supports h1-h6

            # Remove the # symbols and process the rest
            heading_text = block.lstrip('#').strip()
            children = text_to_children(heading_text)
            heading_node = ParentNode(f"h{level}", children)
            parent.children.append(heading_node)

        elif block_type == "code":
            # Code blocks don't process markdown
            # Remove the ``` markers and preserve the content
            code_text = block.strip('`').strip()
            # Create a LeafNode instead of using a TextNode directly
            leaf_node = LeafNode("text", code_text)
            code_node = ParentNode("code", [leaf_node])
            pre_node = ParentNode("pre", [code_node])
            parent.children.append(pre_node)

        elif block_type == "quote":
            # Process quote blocks
            # Remove the > symbols
            quote_text = block.lstrip('>').strip()
            children = text_to_children(quote_text)
            quote_node = ParentNode("blockquote", children)
            parent.children.append(quote_node)

        elif block_type == "unordered_list":
            # Process unordered lists
            list_node = ParentNode("ul", [])

            # Split the block into list items
            items = block.split("\n")
            for item in items:
                if item.strip():  # Skip empty lines
                    # Remove the - or * and process
                    item_text = item.lstrip('-').lstrip('*').strip()
                    children = text_to_children(item_text)
                    item_node = ParentNode("li", children)
                    list_node.children.append(item_node)

            parent.children.append(list_node)

        elif block_type == "ordered_list":
            # Process ordered lists
            list_node = ParentNode("ol", [])

            # Split the block into list items
            items = block.split("\n")
            for item in items:
                if item.strip():  # Skip empty lines
                    # Remove the numbers and period
                    parts = item.split(".", 1)
                    if len(parts) > 1:
                        item_text = parts[1].strip()
                        children = text_to_children(item_text)
                        item_node = ParentNode("li", children)
                        list_node.children.append(item_node)

            parent.children.append(list_node)

    return parent


def extract_title(markdown):
    # Split the markdown into lines
    lines = markdown.split('\n')

    # Loop through each line
    for line in lines:
        # Check if this line starts with a single #
        if line.startswith('# '):
            # Return the title without the # and any whitespace
            return line.lstrip('# ').strip()

    # If we get here, no h1 was found
    raise Exception("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, basepath='/'):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r") as f:
        markdown_content = f.read()

    # Read template
    with open(template_path, "r") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown_content)

    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # Replace paths for GitHub Pages
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write to destination
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath='/'):
    # Step 1: Get all entries in the current directory
    entries = os.listdir(dir_path_content)

    # Step 2: Process each entry
    for entry in entries:
        # Create full paths
        content_path = os.path.join(dir_path_content, entry)

        # Step 3: Check if it's a file or directory
        if os.path.isfile(content_path):
            # If it's a markdown file
            if content_path.endswith('.md'):
                # Create corresponding path in dest directory
                # We need to preserve the relative path structure
                rel_path = os.path.relpath(content_path, dir_path_content)
                # Change extension from .md to .html
                dest_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))

                # Generate the page - pass the basepath!
                generate_page(content_path, template_path, dest_path, basepath)
        else:
            # It's a directory, so recursively process it
            # Create corresponding destination directory
            new_dest_dir = os.path.join(dest_dir_path, entry)

            # Recursive call - pass the basepath!
            generate_pages_recursive(content_path, template_path, new_dest_dir, basepath)