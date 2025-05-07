import re
from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered list"
    ORDEREDLIST = "ordered list"
    PARAGRAPH = "paragraph"

def block_to_block_type(block):
    if re.fullmatch(r"#{1,6} .*.", block, re.DOTALL):
        return BlockType.HEADING
    if re.fullmatch(r"```.+?```", block, re.DOTALL):
        return BlockType.CODE
    lines = block.split("\n")
    if len(list(filter(lambda l: l.startswith(">"), lines))) == len(lines):
        return BlockType.QUOTE
    if len(list(filter(lambda l: l.startswith("- "), lines))) == len(lines):
        return BlockType.UNORDEREDLIST
    if check_block_is_ordered_list(lines):
        return BlockType.ORDEREDLIST
    return BlockType.PARAGRAPH

def check_block_is_ordered_list(lines):
    for i in range(0, len(lines)):
        if not lines[i].startswith(f"{i + 1}. "):
            return False
    return True