from functools import reduce
from textnode import *
from nodeconversion import split_nodes_delimiter, split_nodes_image, split_nodes_link, textnode_to_htmlnode
from leafnode import LeafNode
from parentnode import ParentNode
from blockconversion import BlockType, block_to_block_type

def text_to_textnodes(text):
    delimiter_pos_list = [(text.find("_"), "_", TextType.ITALIC),
                          (text.find("**"), "**", TextType.BOLD),
                          (text.find("`"), "`", TextType.CODE)
                         ]
    list_sorted = sorted(delimiter_pos_list, key=(lambda x: x[0]))
    text = text.replace("\n", " ")
    nodes = [TextNode(text, TextType.NORMAL)]
    for tuple in list_sorted:
        nodes = split_nodes_delimiter(nodes, tuple[1], tuple[2])
    return split_nodes_image(split_nodes_link(nodes))

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[1:].strip()
    raise Exception("Header not found")

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", reduce(lambda a, b: a + [block_to_nodes(b, block_to_block_type(b))], blocks, []))

def block_to_nodes(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return block_to_heading(block)
        case BlockType.CODE:
            return ParentNode("pre", [LeafNode("code", block.strip("`").lstrip("\n"))])
        case BlockType.QUOTE:
            return block_to_quote(block)
        case BlockType.UNORDEREDLIST:
            return block_to_unordered_list(block)
        case BlockType.ORDEREDLIST:
            return block_to_ordered_list(block)
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block))
        case _:
            raise ValueError("invalid block type")
    
def block_to_heading(block):
    no_hash = block.strip("#")
    head_nr = len(block) - len(no_hash)
    return ParentNode(f"h{head_nr}", text_to_children(no_hash.strip()))

def block_to_quote(block):
    lines = block.split("\n")
    new_block = "\n".join(list(map(lambda l: l.lstrip("> "), lines)))
    return ParentNode("blockquote", text_to_children(new_block))

def block_to_unordered_list(block):
    items = block.split("\n")
    items = list(map(lambda l: l[1:].lstrip(), items))
    return ParentNode("ul", reduce(lambda a, i: a + [ParentNode("li", text_to_children(i))], items, []))

def block_to_ordered_list(block):
    items = block.split("\n")
    items = list(map(lambda l: l[2:].lstrip(), items))
    return ParentNode("ol", reduce(lambda a, i: a + [ParentNode("li", text_to_children(i))], items, []))

def text_to_children(text):
    return reduce(lambda a, n: a + [textnode_to_htmlnode(n)], text_to_textnodes(text), [])