import re
from textnode import *
from nodeconversion import split_nodes_delimiter, split_nodes_image, split_nodes_link

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