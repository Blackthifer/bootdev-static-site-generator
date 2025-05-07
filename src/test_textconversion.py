import unittest
from textconversion import *
from textnode import *

class TestTextToNodes(unittest.TestCase):
    def test_text_to_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text),
                         [TextNode("This is ", TextType.NORMAL),
                          TextNode("text", TextType.BOLD),
                          TextNode(" with an ", TextType.NORMAL),
                          TextNode("italic", TextType.ITALIC),
                          TextNode(" word and a ", TextType.NORMAL),
                          TextNode("code block", TextType.CODE),
                          TextNode(" and an ", TextType.NORMAL),
                          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                          TextNode(" and a ", TextType.NORMAL),
                          TextNode("link", TextType.LINK, "https://boot.dev"),
                         ])
    
    def test_text_to_node_nested(self):
        text = "This text includes _italic text with `code text with **bold** text in it` in it_ text"
        self.assertEqual(text_to_textnodes(text),
                         [TextNode("This text includes ", TextType.NORMAL),
                          TextNode("italic text with ", TextType.ITALIC),
                          TextNode("code text with ", TextType.CODE),
                          TextNode("bold", TextType.BOLD),
                          TextNode(" text in it", TextType.CODE),
                          TextNode(" in it", TextType.ITALIC),
                          TextNode(" text", TextType.NORMAL)
                          ])

class TestMarkdownToBlock(unittest.TestCase):
    def test_md_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        self.assertEqual(markdown_to_blocks(md),
                        ["This is **bolded** paragraph",
                         "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                         "- This is a list\n- with items"]
                        )
    
    def test_to_block_extra_whitespace(self):
        md = """

        First paragraph              
        Multiline           

        Second paragraph         


        Third paragraph          

        """
        self.assertEqual(markdown_to_blocks(md),
                         ["First paragraph\nMultiline",
                          "Second paragraph",
                          "Third paragraph"]
                        )

class TestMarkdownToNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )