class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag 
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        converted = ""

        for i in self.props:
            converted += f' {i}="{self.props[i]}"'

        return converted

    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else:
            return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value,props=None):
        super().__init__(tag)
        self.value = value
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            return fr'{self.value}'
        else:
            if self.props == None:
                return f'<{self.tag}>{self.value}</{self.tag}>'
            else:
                return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return(f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
        self.value = None

    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.children}, {self.props})")
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent node must have a tag.")

        if self.children == None or self.children == []:
            raise ValueError("Parent node must have a children.")

        else:
            parent_conv = ""
            for child in self.children:
               parent_conv += child.to_html() 
        if self.props == None:
            return f"<{self.tag}>{parent_conv}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{parent_conv}</{self.tag}>"
