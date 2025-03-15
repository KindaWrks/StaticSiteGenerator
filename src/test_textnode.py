import unittest

from src.textnode import extract_markdown_images
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


if __name__ == "__main__":
    unittest.main()