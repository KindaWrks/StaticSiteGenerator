from src.textnode import TextNode


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
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
    def __init__(self, tag, value, attributes=None):
        # Call the parent constructor with super()
        # Make sure to pass the parameters in the correct order
        # HTMLNode.__init__(self, tag, value, children, props)
        super().__init__(tag, value, [], attributes)  # Note the order!

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")

        if self.tag is None:
            return self.value

        # Start building the HTML tag
        html = f"<{self.tag}"

        # Use self.props instead of self.attributes
        if self.props:
            for key, value in self.props.items():
                html += f' {key}="{value}"'

        # Close the opening tag, add the value, and add the closing tag
        html += f">{self.value}</{self.tag}>"

        return html