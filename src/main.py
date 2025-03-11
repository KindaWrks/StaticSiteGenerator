from textnode import TextNode, TextType

def main():
    # Create a TextNode instance
    node = TextNode("This is some anchor text", TextType.Links, "https://www.boot.dev")
    # Print the node
    print(node)

if __name__ == "__main__":
    main()