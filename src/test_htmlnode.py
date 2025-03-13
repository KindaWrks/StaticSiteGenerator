import unittest
from src.htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        # Test when props is None
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        # Test with a single property
        node = HTMLNode(props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(props={"href": "https://www.example.com", "target": "_blank"})
        # Note: The order of properties in a dictionary is not guaranteed,
        # so we need to check for both possible orders
        result = node.props_to_html()
        possible_results = [
            ' href="https://www.example.com" target="_blank"',
            ' target="_blank" href="https://www.example.com"'
        ]
        self.assertIn(result, possible_results)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()