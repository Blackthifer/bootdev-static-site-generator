from functools import reduce
from textnode import *
from leafnode import LeafNode

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
            raise ValueError("invalid text type!")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return reduce(lambda a, l: a + l,
                  list(map(lambda n: [
                                    TextNode(n.text[:n.text.find(delimiter)], n.text_type),
                                    TextNode(n.text[n.text.find(delimiter) + len(delimiter):n.text.rfind(delimiter)], text_type),
                                    TextNode(n.text[n.text.rfind(delimiter) + len(delimiter):], n.text_type),
                                    ] if n.text.find(delimiter) >= 0 else [n],
                                    old_nodes)), []
                )