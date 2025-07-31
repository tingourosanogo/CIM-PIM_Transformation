from lxml import etree
import textwrap

def parse_xml_to_markdown(xml_path: str, output_path: str):
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # 1. Generate the metadata (YAML front matter)
    metadata = {
        "title": root.xpath("//metadata/title/text()")[0],
        "author": root.xpath("//metadata/author/text()")[0],
        "date": root.xpath("//metadata/date/text()")[0]
    }
    yaml_front_matter = textwrap.dedent(f"""\
    ---
    title: "{metadata['title']}"
    author: "{metadata['author']}"
    date: "{metadata['date']}"
    ---
    """)

    # 2. Process the main content
    markdown = [yaml_front_matter]
    for section in root.xpath("//content/section"):
        markdown.append(f"## {section.xpath('title/text()')[0]}\n")

        for element in section.xpath("*[not(self::title)]"):
            if element.tag == "paragraph":
                markdown.append(process_paragraph(element) + "\n")
            elif element.tag == "figure":
                markdown.append(process_figure(element))
            elif element.tag == "table":
                markdown.append(process_table(element))
            elif element.tag == "code-block":
                markdown.append(process_code_block(element))

    # 3. Write in the Markdown file
    with open(output_path, "w", encoding='utf-8') as f:
        f.write("\n".join(markdown))

def process_paragraph(element) -> str:
    text = ""
    for node in element.xpath(".//text() | .//*"):
        if isinstance(node, str):  # plain text
            text += f" {node.strip()} "
        else:
            if node.tag == "bold":
                text += f"**{node.text.strip()}**"
            elif node.tag == "italic":
                text += f"*{node.text.strip()}*"
            elif node.tag == "inline-math":
                text += f"${node.text.strip()}$"
            elif node.tag == "code":
                text += f"`{node.text.strip()}`"
            elif node.tag == "link":
                text += f"{node.text.strip()}]({node.get('url')})"
    return text

def process_figure(element) -> str:
    src = element.xpath("image/@src")[0]
    alt = element.xpath("image/@alt")[0]
    caption = element.xpath("caption/text()")[0]
    return f'![{alt}]({src})\n\n*{caption}*\n'

def process_table(element) -> str:
    headers = [h.text for h in element.xpath("header/column")]
    rows = [
        [process_paragraph(cell) for cell in row.xpath("cell")]
        for row in element.xpath("row")
    ]
    # Construction of the Markdown table
    table = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |"
    ]
    for row in rows:
        table.append("| " + " | ".join(row) + " |")
    return "\n".join(table) + "\n"

def process_code_block(element) -> str:
    lang = element.get("lang", "")
    code = element.text.strip() if element.text else ""
    return f"```{lang}\n{code}\n```\n"

if __name__ == "__main__":
    parse_xml_to_markdown("FirstStep/input_3.xml", "FirstStep/output_complex.md")
    print("Markdown generated : output_complex.md")