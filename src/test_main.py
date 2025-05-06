import unittest
from main import textnode_to_htmlnode
from textnode import *
from leafnode import LeafNode

class TestMain(unittest.TestCase):
    def test_normal_text(self):
        node = TextNode("just text", TextType.NORMAL)
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), "just text")

    def test_bold_text(self):
        node = TextNode("bold text", TextType.BOLD)
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), "<b>bold text</b>")

    def test_italic_text(self):
        node = TextNode("italic text", TextType.ITALIC)
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), "<i>italic text</i>")

    def test_code_text(self):
        node = TextNode("code text", TextType.CODE)
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), "<code>code text</code>")

    def test_link_text(self):
        node = TextNode("a link", TextType.LINK, "link.io")
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), '<a href="link.io">a link</a>')

    def test_image_text(self):
        node = TextNode("an image", TextType.IMAGE, "img.png")
        leafnode = textnode_to_htmlnode(node)
        self.assertEqual(leafnode.to_html(), '<img src="img.png" alt="an image"></img>')