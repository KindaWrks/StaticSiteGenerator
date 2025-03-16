from src.textnode import TextNode, markdown_to_blocks, block_to_block_type, text_to_textnodes
from src.htmlnode import HTMLNode


def split_markdown_into_blocks(markdown):
    return markdown_to_blocks(markdown)


def determine_block_type(block):
    return block_to_block_type(block)


def text_to_children(text):
    # This likely needs more processing to convert TextNodes to HTMLNodes
    text_nodes = text_to_textnodes(text)
    # You'll need to convert these TextNodes to HTMLNodes
    # and return a list of HTMLNode objects
    return text_nodes


def markdown_to_html_node(markdown):
    # Create a parent div node
    parent = HTMLNode("div", None, None, [])

    # Split markdown into blocks
    blocks = split_markdown_into_blocks(markdown)

    # Process each block
    for block in blocks:
        # Determine block type
        block_type = determine_block_type(block)

        if block_type == "paragraph":
            # Create paragraph node
            children = text_to_children(block)
            paragraph_node = HTMLNode("p", None, None, children)
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
            heading_node = HTMLNode(f"h{level}", None, None, children)
            parent.children.append(heading_node)

        elif block_type == "code":
            # Code blocks don't process markdown
            # Remove the ``` markers and preserve the content
            code_text = block.strip('`').strip()
            # For code blocks, don't process markdown - use TextNode directly
            text_node = TextNode(code_text, "text")
            code_node = HTMLNode("code", None, None, [text_node])
            pre_node = HTMLNode("pre", None, None, [code_node])
            parent.children.append(pre_node)

        elif block_type == "quote":
            # Process quote blocks
            # Remove the > symbols
            quote_text = block.lstrip('>').strip()
            children = text_to_children(quote_text)
            quote_node = HTMLNode("blockquote", None, None, children)
            parent.children.append(quote_node)

        elif block_type == "unordered_list":
            # Process unordered lists
            list_node = HTMLNode("ul", None, None, [])

            # Split the block into list items
            items = block.split("\n")
            for item in items:
                if item.strip():  # Skip empty lines
                    # Remove the - or * and process
                    item_text = item.lstrip('-').lstrip('*').strip()
                    children = text_to_children(item_text)
                    item_node = HTMLNode("li", None, None, children)
                    list_node.children.append(item_node)

            parent.children.append(list_node)

        elif block_type == "ordered_list":
            # Process ordered lists
            list_node = HTMLNode("ol", None, None, [])

            # Split the block into list items
            items = block.split("\n")
            for item in items:
                if item.strip():  # Skip empty lines
                    # Remove the numbers and period
                    parts = item.split(".", 1)
                    if len(parts) > 1:
                        item_text = parts[1].strip()
                        children = text_to_children(item_text)
                        item_node = HTMLNode("li", None, None, children)
                        list_node.children.append(item_node)

            parent.children.append(list_node)

    return parent