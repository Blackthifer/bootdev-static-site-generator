import unittest
from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_to_html_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()

        self.assertEqual(str(cm.exception), "Leaf node needs a value!")
    
