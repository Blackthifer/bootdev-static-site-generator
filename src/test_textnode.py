import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a bold textnode", TextType.BOLD)
        node2 = TextNode("this is a bold textnode", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_init(self):
        node = TextNode("normal text without url", TextType.NORMAL)
        node2 = TextNode("text with link for no reason", TextType.ITALIC, "myurl.com")
        self.assertEqual(node.text, "normal text without url")
        self.assertEqual(node.text_type, TextType.NORMAL)
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)
        self.assertEqual(node2.url, "myurl.com")
    
    def test_repr(self):
        node = TextNode("link text here", TextType.LINK, "https://mypage.org")
        self.assertEqual(f"{node}", "TextNode(link text here, link, https://mypage.org)")

    

if __name__ == "__main__":
    unittest.main()