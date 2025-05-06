from htmlnode import HTMLNode
from functools import reduce

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node needs a tag!")
        if not self.children:
            raise ValueError("Parent node needs children!")
        return f"<{self.tag}{self.props_to_html()}>{reduce(lambda a, n: a + n.to_html(), self.children, "")}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"
        