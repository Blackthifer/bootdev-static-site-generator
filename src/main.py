from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

def main():
    node = TextNode("weird image", TextType.IMAGE, "../content/weird.png")
    node2 = HTMLNode()
    node3 = ParentNode(None, None)
    node4 = LeafNode(None, None)
    print(node)
    print(node2)
    print(node3)
    print(node4)

main()