import unittest

from src.textnode import extract_markdown_images, text_to_textnodes, markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType, text_node_to_html_node, extract_markdown_links, extract_markdown_images, split_nodes_image

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold_text)
        node2 = TextNode("This is a text node", TextType.Bold_text)
        node3 = TextNode("", TextType.Links)
        self.assertEqual(node, node2)

    def test_noeq(self):
        node = TextNode("This is plain text", TextType.Normal_text)
        node2 = TextNode("This is bold text", TextType.Bold_text)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.Normal_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.Normal_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.Normal_text),
                TextNode("image", TextType.Images, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.Normal_text),
                TextNode(
                    "second image", TextType.Images, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


def test_text_to_textnodes():
    # Test case 1: Plain text with no formatting
    plain_text = "This is just plain text with no formatting."
    plain_result = text_to_textnodes(plain_text)
    assert len(plain_result) == 1
    assert plain_result[0].text == plain_text
    assert plain_result[0].text_type == TextType.Normal_text
    assert plain_result[0].url is None

    # Test case 2: Text with only one type of formatting (bold)
    bold_text = "This has a **bold** word in it."
    bold_result = text_to_textnodes(bold_text)
    assert len(bold_result) == 3
    assert bold_result[0].text == "This has a "
    assert bold_result[0].text_type == TextType.Normal_text
    assert bold_result[1].text == "bold"
    assert bold_result[1].text_type == TextType.Bold_text
    assert bold_result[2].text == " word in it."
    assert bold_result[2].text_type == TextType.Normal_text

    # Test case 3: Text with images and links
    media_text = "Check out this ![image](https://example.com/image.jpg) and this [link](https://example.com)."
    media_result = text_to_textnodes(media_text)
    assert len(media_result) == 4
    assert media_result[0].text == "Check out this "
    assert media_result[0].text_type == TextType.Normal_text
    assert media_result[1].text == "image"
    assert media_result[1].text_type == TextType.Images
    assert media_result[1].url == "https://example.com/image.jpg"
    assert media_result[2].text == " and this "
    assert media_result[2].text_type == TextType.Normal_text

    # Test case 4: Complex text with multiple formatting types
    complex_text = "This is **bold** with _italic_ and `code` plus ![image](https://example.com/pic.jpg) and [link](https://example.com)"
    complex_result = text_to_textnodes(complex_text)
    assert len(complex_result) == 9
    assert complex_result[0].text == "This is "
    assert complex_result[0].text_type == TextType.Normal_text
    assert complex_result[1].text == "bold"
    assert complex_result[1].text_type == TextType.Bold_text
    assert complex_result[2].text == " with "
    assert complex_result[2].text_type == TextType.Normal_text
    assert complex_result[3].text == "italic"
    assert complex_result[3].text_type == TextType.Italic_text
    assert complex_result[4].text == " and "
    assert complex_result[4].text_type == TextType.Normal_text
    assert complex_result[5].text == "code"
    assert complex_result[5].text_type == TextType.Code_text
    assert complex_result[6].text == " plus "
    assert complex_result[6].text_type == TextType.Normal_text
    assert complex_result[7].text == "image"
    assert complex_result[7].text_type == TextType.Images
    assert complex_result[7].url == "https://example.com/pic.jpg"
    assert complex_result[8].text == " and "
    assert complex_result[8].text_type == TextType.Normal_text
    assert complex_result[9].text == "link"
    assert complex_result[9].text_type == TextType.Links
    assert complex_result[9].url == "https://example.com"

def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )


class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        # Test simple paragraph
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.Paragraph)
        # Test multi-line paragraph
        self.assertEqual(block_to_block_type("This is a\nmulti-line paragraph"), BlockType.Paragraph)
        # Test paragraph that might be confused with other types
        self.assertEqual(block_to_block_type("This has # but is not a heading"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type("This has - but not at start of line"), BlockType.Paragraph)

    def test_heading(self):
        # Test single-level heading
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.Heading)
        # Test multi-level headings
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.Heading)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.Heading)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.Heading)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.Heading)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.Heading)
        # Test invalid headings (should be paragraphs)
        self.assertEqual(block_to_block_type("#Heading without space"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.Paragraph)

    def test_code(self):
        # Test simple code block
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.Code)
        # Test code block with language
        self.assertEqual(block_to_block_type("```python\ndef example():\n    return True\n```"), BlockType.Code)
        # Test empty code block
        self.assertEqual(block_to_block_type("```\n```"), BlockType.Code)
        # Test code block with special characters
        self.assertEqual(block_to_block_type("```\n# This is a comment\nprint('Hello world!')\n```"), BlockType.Code)

    def test_quote(self):
        # Test simple quote
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.Quote)
        # Test multi-line quote
        self.assertEqual(block_to_block_type(">This is a\n>multi-line quote"), BlockType.Quote)
        # Test quote with formatting
        self.assertEqual(block_to_block_type(">**Bold** quote"), BlockType.Quote)
        # Test quote with nested content
        self.assertEqual(block_to_block_type(">Quote with\n>- a list item"), BlockType.Quote)

    def test_unordered_list(self):
        # Test simple unordered list
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.Unordered_list)
        # Test multi-item unordered list
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.Unordered_list)
        # Test unordered list with formatting
        self.assertEqual(block_to_block_type("- **Bold** item\n- *Italic* item"), BlockType.Unordered_list)
        # Test unordered list with nested content
        self.assertEqual(block_to_block_type("- Item with\n- Item with > quote"), BlockType.Unordered_list)

    def test_ordered_list(self):
        # Test simple ordered list
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.Ordered_list)
        # Test multi-item ordered list
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.Ordered_list)
        # Test ordered list with formatting
        self.assertEqual(block_to_block_type("1. **Bold** item\n2. *Italic* item"), BlockType.Ordered_list)
        # Test ordered list with nested content
        self.assertEqual(block_to_block_type("1. Item with text\n2. Item with more text"), BlockType.Ordered_list)
        # Test invalid ordered list (should be paragraph)
        self.assertEqual(block_to_block_type("1. First item\n3. Skipped number"), BlockType.Paragraph)

    def test_edge_cases(self):
        # Test empty string (should be paragraph)
        self.assertEqual(block_to_block_type(""), BlockType.Paragraph)

        # Test mixed content that should be identified as paragraph
        self.assertEqual(block_to_block_type("Paragraph\n# Not a heading"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type("Paragraph\n- Not a list"), BlockType.Paragraph)

        # Test cases where format is almost correct but not quite
        self.assertEqual(block_to_block_type("####### Too many #"), BlockType.Paragraph)  # 7 hashtags is too many
        self.assertEqual(block_to_block_type("``\nNot a code block\n``"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type(">First line\nSecond line without >"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type("- First item\nSecond line without -"), BlockType.Paragraph)
        self.assertEqual(block_to_block_type("1. First item\nSecond line without number"), BlockType.Paragraph)

    if __name__ == "__main__":
        unittest.main()