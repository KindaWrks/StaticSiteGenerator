import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()