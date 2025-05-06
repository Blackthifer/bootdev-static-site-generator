from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

def textnode_to_htmlnode(textnode):
    match textnode.text_type:
        case TextType.NORMAL:
            return LeafNode(None, textnode.text)
        case TextType.BOLD:
            return LeafNode("b", textnode.text)
        case TextType.ITALIC:
            return LeafNode("i", textnode.text)
        case TextType.CODE:
            return LeafNode("code", textnode.text)
        case TextType.LINK:
            return LeafNode("a", textnode.text, {"href": textnode.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
        case _:
            raise ValueError("invalid text type")

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