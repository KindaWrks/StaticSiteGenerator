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




