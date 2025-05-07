import unittest
from nodeconversion import *
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
        
    def test_delimiter_at_ends(self):
        node = TextNode("**bold text in normal node**", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("bold text in normal node", TextType.BOLD)])
    
    def test_nested(self):
        node = TextNode("text with _italic text including **bold** text_", TextType.NORMAL)
        self.assertEqual(split_nodes_delimiter(split_nodes_delimiter([node], "_", TextType.ITALIC), "**", TextType.BOLD),
                         [TextNode("text with ", TextType.NORMAL),
                          TextNode("italic text including ", TextType.ITALIC),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" text", TextType.ITALIC)]
                        )
        
    def test_image(self):
        node = TextNode("This is text with an ![image](img1.png) and another ![second image](img2.png)", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.ITALIC),
                TextNode("image", TextType.IMAGE, "img1.png"),
                TextNode(" and another ", TextType.ITALIC),
                TextNode("second image", TextType.IMAGE, "img2.png")
            ],
            split_nodes_image([node])
            )

    def test_link(self):
        node = TextNode("This is text with a [link](www.link.com) and another [second link](www.secondlink.com)", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.BOLD),
                TextNode("link", TextType.LINK, "www.link.com"),
                TextNode(" and another ", TextType.BOLD),
                TextNode("second link", TextType.LINK, "www.secondlink.com")
            ],
            split_nodes_link([node])
            )
    
    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "_", TextType.ITALIC), [])
        self.assertEqual(split_nodes_image([]), [])
        self.assertEqual(split_nodes_link([]), [])
    
    def test_order_relevant(self):
        node = TextNode("including _italic_ and **bold** text", TextType.NORMAL)
        node2 = TextNode("including _italic with **bold** in it_ text", TextType.NORMAL)
        node3 = TextNode("including **bold with _italic_ in it** text", TextType.NORMAL)
        self.assertNotEqual(
            split_nodes_delimiter(split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC), "**", TextType.BOLD),
            split_nodes_delimiter(split_nodes_delimiter([node, node2, node3], "**", TextType.BOLD), "_", TextType.ITALIC)
        )

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        text2 = "![Image](img.png) at the start of text"
        self.assertEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], extract_markdown_images(text))
        self.assertEqual([("Image", "img.png")], extract_markdown_images(text2))
    
    def test_extract_link(self):
        text = "This is text with a [link](https://www.boot.dev)"
        text2 = "[Link](https://www.boot.dev) at the start of the text"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.boot.dev")])
        self.assertEqual(extract_markdown_links(text2), [("Link", "https://www.boot.dev")])
    
    def test_extract_multiple(self):
        text_img = "This is a text with ![one image](img1.png) and ![another image](img2.png)"
        text_link = "This is a text with [one link](www.link.com) and [another link](www.linkeee.com)"
        self.assertEqual(extract_markdown_images(text_img), [("one image", "img1.png"), ("another image", "img2.png")])
        self.assertEqual(extract_markdown_links(text_link), [("one link", "www.link.com"), ("another link", "www.linkeee.com")])
    
    def test_link_dont_match_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        self.assertEqual(extract_markdown_links(text), [])