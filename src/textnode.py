from enum import Enum

from htmlnode import LeafNode
import re

class BlockType(Enum):
    Paragraph = "paragraph"
    Heading = "heading"
    Code = "code"
    Quote = "quote"
    Unordered_list = "unordered_list"
    Ordered_list = "ordered_list"


class TextType(Enum):
    Normal_text = "normal_text"
    Bold_text = "bold_text"
    Italic_text = "italic_text"
    Code_text = "code_text"
    Links = "links"
    Images = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.Normal_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.Bold_text:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.Italic_text:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.Code_text:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.Links:
        attributes = {"href": text_node.url}  # Define the attributes with "href" using the url
        return LeafNode("a", text_node.text, attributes)

    if text_node.text_type == TextType.Images:
        attributes = {
            "src": text_node.url,  # URL for the image
            "alt": text_node.text  # Alternative text for the image
        }
        return LeafNode("img", "", attributes)  # Note empty string for value


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.Normal_text:
            result.append(old_node)
            continue

        # Process text node
        text = old_node.text

        # Check if the delimiter appears in the text
        if delimiter not in text:
            result.append(old_node)
            continue

        # Find chunks that need to be processed
        chunks = []
        remaining_text = text

        while delimiter in remaining_text:
            # Find the first occurrence of delimiter
            start_index = remaining_text.find(delimiter)

            # Add text before delimiter as normal text if it exists
            if start_index > 0:
                chunks.append((remaining_text[:start_index], TextType.Normal_text))

            # Find the closing delimiter
            remaining_text = remaining_text[start_index + len(delimiter):]
            end_index = remaining_text.find(delimiter)

            if end_index == -1:
                # No closing delimiter found
                raise ValueError(f"No closing delimiter found for {delimiter}")

            # Add the text between delimiters with the specified text type
            chunks.append((remaining_text[:end_index], text_type))

            # Update remaining_text for next iteration
            remaining_text = remaining_text[end_index + len(delimiter):]

        # Add any remaining text as normal text
        if remaining_text:
            chunks.append((remaining_text, TextType.Normal_text))

        # Create TextNode objects from chunks and add to result
        for text_chunk, chunk_type in chunks:
            result.append(TextNode(text_chunk, chunk_type))

    return result


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)

    return matches


def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        # If not a text node, just add it to results
        if old_node.text_type != TextType.Normal_text:
            result.append(old_node)
            continue

        # Check if there's an image in this text node
        images = extract_markdown_images(old_node.text)

        # If no image found, keep the node as is
        if not images:
            result.append(old_node)
            continue

        # If image found, get the first one
        image_alt, image_url = images[0]
        image_markdown = f"![{image_alt}]({image_url})"

        # Split the text into before and after the image
        sections = old_node.text.split(image_markdown, 1)
        before_text = sections[0]

        # Add the before text as a node if not empty
        if before_text:
            result.append(TextNode(before_text, TextType.Normal_text))

        # Add the image as a node
        result.append(TextNode(image_alt, TextType.Images, image_url))

        # Handle the after text (which might contain more images)
        if len(sections) > 1:
            after_text = sections[1]
            if after_text:
                # Recursively check for more images in the after text
                after_nodes = split_nodes_image([TextNode(after_text, TextType.Normal_text)])
                result.extend(after_nodes)

    return result

def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        # If not a text node, just add it to results
        if old_node.text_type != TextType.Normal_text:
            result.append(old_node)
            continue

        # Check if there's a link in this text node
        links = extract_markdown_links(old_node.text)

        # If no link found, keep the node as is
        if not links:
            result.append(old_node)
            continue

        # If link found, get the first one
        link_text, link_url = links[0]
        link_markdown = f"[{link_text}]({link_url})"

        # Split the text into before and after the link
        sections = old_node.text.split(link_markdown, 1)
        before_text = sections[0]

        # Add the before text as a node if not empty
        if before_text:
            result.append(TextNode(before_text, TextType.Normal_text))

        # Add the link as a node
        result.append(TextNode(link_text, TextType.Links, link_url))

        # Handle the after text (which might contain more links)
        if len(sections) > 1:
            after_text = sections[1]
            if after_text:
                # Recursively check for more links in the after text
                after_nodes = split_nodes_link([TextNode(after_text, TextType.Normal_text)])
                result.extend(after_nodes)

    return result


def text_to_textnodes(text):
    # Start with the entire text as a single node
    nodes = [TextNode(text, TextType.Normal_text)]
    # Apply delimiter splitting for bold text
    nodes = split_nodes_delimiter(nodes, "**", TextType.Bold_text)
    # Apply delimiter splitting for italic text
    nodes = split_nodes_delimiter(nodes, "_", TextType.Italic_text)
    # Apply delimiter splitting for code blocks
    nodes = split_nodes_delimiter(nodes, "`", TextType.Code_text)
    # Apply image splitting
    nodes = split_nodes_image(nodes)
    # Apply link splitting
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    # Split the markdown into blocks using double \n as the delimiter
    blocks = markdown.split("\n\n")

    #We need to clean up each block and remove empty ones
    cleaned_blocks = []
    for block in blocks:
        cleaned_block = block.strip()
        # Only add non-empty blocks to our list
        if cleaned_block:
            cleaned_blocks.append(cleaned_block)

    return cleaned_blocks


def block_to_block_type(block):
    # Check for heading
    if block.startswith(("#", "##", "###", "####", "#####", "######")):
        pound_count = 0
        for char in block:
            if char == '#':
                pound_count += 1
            else:
                break

        if pound_count <= 6 and pound_count > 0 and block[pound_count] == ' ':
            return "heading"

    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return "code"

    # Split the block into lines
    lines = block.split("\n")

    # Check for quote block
    if all(line.startswith(">") for line in lines) and lines:  # Make sure there's at least one line
        return "quote"

    # Check for unordered list
    if all(line.startswith("- ") for line in lines) and lines:  # Make sure there's at least one line
        return "unordered_list"

    # Check for ordered list
    if lines:  # Make sure there's at least one line
        is_ordered = True
        for i, line in enumerate(lines):
            if not line.startswith(f"{i + 1}. "):
                is_ordered = False
                break

        if is_ordered:
            return "ordered_list"

    # If none of the above conditions are met, it's a paragraph
    return "paragraph"