import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "child")])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        
        self.assertEqual(str(cm.exception), "Parent node needs a tag!")

    def test_to_html_no_child(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        
        self.assertEqual(str(cm.exception), "Parent node needs children!")

    def test_to_html_multi_children(self):
        child_node = LeafNode("p", "Child one")
        child_node2 = LeafNode("p", "Child two")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><p>Child one</p><p>Child two</p></div>")