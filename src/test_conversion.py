import unittest
from conversion import textnode_to_htmlnode, split_nodes_delimiter
from textnode import *
from leafnode import LeafNode

class TestTextToHTML(unittest.TestCase):
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
    
    def test_no_texttype(self):
        node = TextNode("what?", None)
        with self.assertRaises(ValueError) as cm:
            textnode_to_htmlnode(node)
        
        self.assertEqual(str(cm.exception), "invalid text type!")

class TestSplitNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("text including **bold** text", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("text including ", TextType.NORMAL),
                                                                              TextNode("bold", TextType.BOLD),
                                                                              TextNode(" text", TextType.NORMAL)])
    
    def test_italic(self):
        node = TextNode("text including _italic_ text", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [TextNode("text including ", TextType.NORMAL),
                                                                              TextNode("italic", TextType.ITALIC),
                                                                              TextNode(" text", TextType.NORMAL)])
    
    def test_code(self):
        node = TextNode("text including `code` text", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [TextNode("text including ", TextType.NORMAL),
                                                                              TextNode("code", TextType.CODE),
                                                                              TextNode(" text", TextType.NORMAL)])
    
    def test_multiple_nodes(self):
        node = TextNode("text including **bold** text", TextType.NORMAL)
        node2 = TextNode("text including _italic_ text", TextType.NORMAL)
        node3 = TextNode("text including **bold** text again", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD), [TextNode("text including ", TextType.NORMAL),
                                                                                            TextNode("bold", TextType.BOLD),
                                                                                            TextNode(" text", TextType.NORMAL),
                                                                                            TextNode("text including _italic_ text", TextType.NORMAL),
                                                                                            TextNode("text including ", TextType.NORMAL),
                                                                                            TextNode("bold", TextType.BOLD),
                                                                                            TextNode(" text again", TextType.NORMAL)])
    
    def test_nested(self):
        node = TextNode("italic text including **bold** text", TextType.ITALIC)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("italic text including ", TextType.ITALIC),
                                                                              TextNode("bold", TextType.BOLD),
                                                                              TextNode(" text", TextType.ITALIC)])
    
    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "_", TextType.ITALIC), [])
    
    def test_order_relevant(self):
        node = TextNode("including _italic_ and **bold** text", TextType.NORMAL)
        node2 = TextNode("including _italic with **bold** in it_ text", TextType.NORMAL)
        node3 = TextNode("including **bold with _italic_ in it** text", TextType.NORMAL)
        self.assertNotEqual(
            split_nodes_delimiter(split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC), "**", TextType.BOLD),
            split_nodes_delimiter(split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD), "_", TextType.ITALIC)
        )