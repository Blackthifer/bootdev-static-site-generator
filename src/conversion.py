import re
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
        
def text_to_textnodes(text):
    delimiter_pos_list = [(text.find("_"), "_", TextType.ITALIC),
                          (text.find("**"), "**", TextType.BOLD),
                          (text.find("`"), "`", TextType.CODE)
                         ]
    list_sorted = sorted(delimiter_pos_list, key=(lambda x: x[0]))
    nodes = [TextNode(text, TextType.NORMAL)]
    for tuple in list_sorted:
        nodes = split_nodes_delimiter(nodes, tuple[1], tuple[2])
    return split_nodes_image(split_nodes_link(nodes))

def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    block = ""
    for line in lines:
        if line == "":
            blocks += [block.strip("\n")] if block != "" else []
            block = ""
            continue
        block += line.strip() + "\n"
    if block.strip("\n") != "":
        blocks += [block.strip("\n")]
    return blocks
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_single_node(node):
        regex = "" 
        match delimiter:
            case "_":
                regex = r"(?<!\S)_.+?_(?!\S)"
            case "**":
                regex = r"(?<!\S)\*\*.+?\*\*(?!\S)"
            case "`":
                regex = r"(?<!\S)`.+?`(?!\S)"
            case _:
                return [node]
        matches = re.findall(regex, node.text)
        if matches == []:
            return [node]
        new_nodes = []
        text = node.text
        for match in matches:
            match_pos = text.find(match)
            match_length = len(match)
            if match_pos == 0:
                new_nodes += [TextNode(match.strip(delimiter), text_type)]
                text = text[match_length:]
            else:
                new_nodes += [TextNode(text[:match_pos], node.text_type), TextNode(match.strip(delimiter), text_type)]
                text = text[match_pos + match_length:]
        if len(text) > 0:
            new_nodes += [TextNode(text, node.text_type)]
        return new_nodes

    return reduce(lambda a, l: a + l,
                  list(map(lambda n: split_single_node(n), old_nodes)),
                  []
                )

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    def split_single_node(node):
        matches = extract_markdown_images(node.text)
        if matches == []:
            return [node]
        new_nodes = []
        text = node.text
        for match in matches:
            full_match = f"![{match[0]}]({match[1]})"
            match_pos = text.find(full_match)
            match_length = len(full_match)
            if match_pos == 0:
                new_nodes += [TextNode(match[0], TextType.IMAGE, match[1])]
                text = text[match_length:]
            else:
                new_nodes += [TextNode(text[:match_pos], node.text_type), TextNode(match[0], TextType.IMAGE, match[1])]
                text = text[match_pos + match_length:]
        if len(text) > 0:
            new_nodes += [TextNode(text, node.text_type)]
        return new_nodes

    return reduce(lambda a, l: a + l,
                  list(map(lambda n: split_single_node(n), old_nodes)),
                  []
                )

def split_nodes_link(old_nodes):
    def split_single_node(node):
        matches = extract_markdown_links(node.text)
        if matches == []:
            return [node]
        new_nodes = []
        text = node.text
        for match in matches:
            full_match = f"[{match[0]}]({match[1]})"
            match_pos = text.find(full_match)
            match_length = len(full_match)
            if match_pos == 0:
                new_nodes += [TextNode(match[0], TextType.LINK, match[1])]
                text = text[match_length:]
            else:
                new_nodes += [TextNode(text[:match_pos], node.text_type), TextNode(match[0], TextType.LINK, match[1])]
                text = text[match_pos + match_length:]
        if len(text) > 0:
            new_nodes += [TextNode(text, node.text_type)]
        return new_nodes
    
    return reduce(lambda a, l: a + l,
                  list(map(lambda n: split_single_node(n), old_nodes)),
                  []
                )