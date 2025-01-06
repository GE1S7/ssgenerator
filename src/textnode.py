from enum import Enum
from htmlnode import LeafNode

TextType = Enum('TextType', ['NORMAL', 'BOLD', 'ITALIC', 'LINK', 'IMAGE','CODE'])

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def text_node_to_html_node(self):
        if self.text_type == TextType.NORMAL:
            return LeafNode(None, self.text)

        elif self.text_type == TextType.BOLD:
            return LeafNode("b", self.text)

        elif self.text_type == TextType.ITALIC:
            return LeafNode("i", self.text)

        elif self.text_type == TextType.CODE:
            return LeafNode("code", self.text)

        elif self.text_type == TextType.LINK:
            return LeafNode("a", self.text, {"href":self.url})

        elif self.text_type == TextType.IMAGE:
            return LeafNode('img', "", {'src':self.url, 'alt':self.text})

        raise ValueError("Invalid text type")
#TODO add some tests


    # TextType.TEXT: This should become a LeafNode with no tag, just a raw text value.
    # TextType.BOLD: This should become a LeafNode with a "b" tag and the text
    # TextType.ITALIC: "i" tag, text
    # TextType.CODE: "code" tag, text
    # TextType.LINK: "a" tag, anchor text, and "href" prop
    # TextType.IMAGE: "img" tag, empty string value, "src" and "alt" props ("src" is the image URL, "alt" is the alt text)



