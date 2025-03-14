from enum import Enum
from src.htmlnode import LeafNode

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


