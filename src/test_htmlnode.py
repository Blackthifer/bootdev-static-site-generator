import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html(self):
        node = HTMLNode()
        node2 = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com" target="_blank"')
