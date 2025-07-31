from lxml import etree
import textwrap

def parse_xml_to_markdown(xml_path: str, output_path: str, lang: str = "en"):
    encodings = ['utf-8', 'iso-8859-1', 'windows-1252']
    for enc in encodings:
        try:
            with open(xml_path, 'r', encoding=enc) as f:
                tree = etree.parse(f)
            break
        except UnicodeDecodeError:
            continue
    root = tree.getroot()

    # 1. Metadata (YAML front matter)
    metadata = {
        "title": root.xpath(f"//metadata/title/{lang}/text()")[0],
        "author": root.xpath("//metadata/author/text()")[0],
        "date": root.xpath("//metadata/date/text()")[0],
        "lang": lang
    }
    yaml_front_matter = textwrap.dedent(f"""\
    ---
    title: "{metadata['title']}"
    author: "{metadata['author']}"
    date: "{metadata['date']}"
    lang: "{metadata['lang']}"
    ---
    """)

    # 2. Process the main content
    markdown = [yaml_front_matter]
    citations = {}  # Store citations for the bibliography

    for section in root.xpath("//content/section"):
        # section title
        title = section.xpath(f"title/{lang}/text()")[0]
        markdown.append(f"## {title}\n")

        # Content
        for element in section.xpath("*[not(self::title)]"):
            if element.tag == "paragraph":
                markdown.append(process_paragraph(element, lang, citations) + "\n")
            elif element.tag == "mermaid":
                markdown.append(process_mermaid(element, lang))
            elif element.tag == "biblio":
                process_biblio(element, lang, citations)

    # 3. Add the bibliography if necessary
    if citations:
        markdown.append("## References\n" if lang == "en" else "## Références\n")
        for key, ref in citations.items():
            markdown.append(f"- **[{key}]** {ref}\n")

    # 4. Write in the Markdown file
    with open(output_path, "w", encoding='utf-8') as f:
        f.write("\n".join(markdown))

def process_paragraph(element, lang: str, citations: dict) -> str:
    text = ""
    for node in element.xpath(f"./{lang}//text() | ./{lang}/*"):
        if isinstance(node, str):  # plain text
            text += f" {node.strip()} "
        else:
            if node.tag == "bold":
                text += f"**{node.text.strip()}**"
            elif node.tag == "cite":
                key = node.get("key")
                citations[key] = ""  # Filled later by process_biblio()
                text += f"[{key}]"
    return text

def process_mermaid(element, lang: str) -> str:
    diagram = element.xpath(f"{lang}/text()")[0].strip()
    return f"```mermaid\n{diagram}\n```\n"

def process_biblio(element, lang: str, citations: dict):
    for entry in element.xpath("entry"):
        key = entry.get("key")
        citations[key] = entry.xpath(f"{lang}/text()")[0].strip()

if __name__ == "__main__":
    # Generate the EN and FR versions
    parse_xml_to_markdown("FirstStep/input_4.xml", "FirstStep/output_en.md", lang="en")
    parse_xml_to_markdown("FirstStep/input_4.xml", "FirstStep/output_fr.md", lang="fr")
    print("Markdown generated : output_en.md, output_fr.md")