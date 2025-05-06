from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from conversion import textnode_to_htmlnode

def main():
    node = TextNode("weird image", TextType.IMAGE, "../content/weird.png")
    node2 = HTMLNode()
    node3 = ParentNode(None, None)
    node4 = LeafNode(None, None)
    link_node = textnode_to_htmlnode(TextNode("my page", TextType.LINK, "https://blackthifer.github.com"))
    image_node = textnode_to_htmlnode(TextNode("my picture", TextType.IMAGE, "https://blackthifer.github.com/picture.jpg"))
    print(link_node)
    print(image_node)
    print(node)
    print(node2)
    print(node3)
    print(node4)

main()