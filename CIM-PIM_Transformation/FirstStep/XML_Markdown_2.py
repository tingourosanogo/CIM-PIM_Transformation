from lxml import etree
import textwrap

def parse_xml_to_markdown(xml_path: str, output_path: str):
    # Load the XML
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # 1. Generate the metadata (YAML front matter)
    metadata = {
        "title": root.xpath("//metadata/title/text()")[0],
        "author": root.xpath("//metadata/author/text()")[0],
        "date": root.xpath("//metadata/date/text()")[0],
        "tags": ", ".join(root.xpath("//metadata/tags/tag/text()"))
    }
    yaml_front_matter = "\n".join([
        "---",
        f"title: {metadata['title']}",
        f"author: {metadata['author']}",
        f"date: {metadata['date']}",
        f"tags: [{metadata['tags']}]",
        "---\n"
    ])

    # 2. Process the main content
    markdown_content = [yaml_front_matter]

    for section in root.xpath("//content/section"):
        # Section title (level 2)
        title = section.xpath("title/text()")[0]
        markdown_content.append(f"## {title}\n")

        # Paragraphs and nested elements
        for element in section.xpath("*[not(self::title)]"):
            if element.tag == "paragraph":
                text = process_inline_tags(element)
                markdown_content.append(f"{text}\n")
            elif element.tag == "list":
                list_type = element.get("type", "unordered")
                markdown_list = []
                for item in element.xpath("item"):
                    item_text = process_inline_tags(item)
                    prefix = "- " if list_type == "unordered" else "1. "
                    markdown_list.append(f"{prefix}{item_text}")
                markdown_content.append("\n".join(markdown_list) + "\n")

    # 3. Write in the Markdown file
    with open(output_path, "w", encoding='utf-8') as f:
        f.write("\n".join(markdown_content))

def process_inline_tags(element) -> str:
    """Manages inline tags (bold, italic, lien, code)."""
    text = ""
    for child in element.iter():  
        if child.tag in ["bold", "italic", "link", "code"]:
            if child.tag == "bold":
                text += f"**{child.text.strip()}**" if child.text else ""
            elif child.tag == "italic":
                text += f"*{child.text.strip()}*" if child.text else ""
            elif child.tag == "link":
                url = child.get("url", "")
                text += f"[{child.text.strip()}]({url})" if child.text else ""
            elif child.tag == "code":
                text += f"`{child.text.strip()}`" if child.text else ""
        elif child.text:  # Raw text excluding tags
            text += f" {child.text.strip()} "
        if child.tail:  # Text after a closing tag (ex: </bold>)
            text += child.tail.strip()
    return text

# Execution
if __name__ == "__main__":
    parse_xml_to_markdown("FirstStep/input_2.xml", "FirstStep/output_advanced.md")
    print("Markdown output : output_advanced.md")