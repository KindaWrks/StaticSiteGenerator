class HTMLNode:
    def __init__(self, tag=None, attributes=None, value=None, children=None, props=None):
        self.tag = tag
        self.attributes = attributes or {}  # Initialize to an empty dict if None
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""

        result = ""
        
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value="", attributes=None):
        super().__init__(tag, attributes)
        self.value = value

    def to_html(self):
        if self.tag is None:
            return self.value

        attributes_html = ""
        for attr, value in self.attributes.items():
            attributes_html += f' {attr}="{value}"'

        return f"<{self.tag}{attributes_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, attributes=None):
        super().__init__(tag, attributes)  # Make sure to call the parent's __init__
        self.children = children or []

    def to_html(self):
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        attributes_html = ""
        for attr, value in self.attributes.items():
            attributes_html += f' {attr}="{value}"'

        return f"<{self.tag}{attributes_html}>{children_html}</{self.tag}>"