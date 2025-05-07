import unittest
from blockconversion import *

class TestBlockToHTML(unittest.TestCase):
    def test_heading(self):
        text = "### heading\nwith newline"
        text2 = "# heading"
        text3 = "###### heading"
        text4 = "##not heading"
        text5 = " also not heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(text3), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(text4), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(text5), BlockType.HEADING)

    def test_code(self):
        text = "```some code in here```"
        text2 = "```\nsome code in here\nwith newlines\n```"
        text3 = "`not code`"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
        self.assertEqual(block_to_block_type(text2), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(text3), BlockType.CODE)
    
    def test_quote(self):
        text = ">single quote"
        text2 = ">multi\n>line\n>quote"
        text3 = "> still\n>     a\n>    quote"
        text4 = ">not\na\n>quote"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(text3), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type(text4), BlockType.QUOTE)
    
    def test_unordered_list(self):
        text = "- single item"
        text2 = "- multiple\n- items\n- in\n- list"
        text3 = "-not\n-a\n-list"
        text4 = "- also\nnot\na\n- list"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDEREDLIST)
        self.assertEqual(block_to_block_type(text2), BlockType.UNORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text3), BlockType.UNORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text4), BlockType.UNORDEREDLIST)
    
    def test_ordered_list(self):
        text = "1. single item"
        text2 = "1. item one\n2. item two\n3. item three etc"
        text3 = "1.not\n2.an\n3.ordered\n4.list"
        text4 = "1.not\nan\nordered\n4.list"
        text5 = "1. not\n1. an\n1. ordered\n1. list"
        text6 = "1. not2. an3. ordered\n4. list"
        self.assertEqual(block_to_block_type(text), BlockType.ORDEREDLIST)
        self.assertEqual(block_to_block_type(text2), BlockType.ORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text3), BlockType.ORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text4), BlockType.ORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text5), BlockType.ORDEREDLIST)
        self.assertNotEqual(block_to_block_type(text6), BlockType.ORDEREDLIST)