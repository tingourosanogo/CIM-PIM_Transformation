from lxml import etree

# 1. Charger le XML
xml = etree.parse("FirstStep/input_1.xmi")

# 2. G�n�rer le Markdown
markdown_content = []

# M�tadonn�es (YAML front matter pour Jekyll/Hugo, optionnel)
markdown_content.append("---")
markdown_content.append(f"title: {xml.xpath('//metadata/title/text()')[0]}")
markdown_content.append(f"author: {xml.xpath('//metadata/author/text()')[0]}")
markdown_content.append("---\n")

# Chapitres
for chapter in xml.xpath("//chapters/chapter"):
    chap_title = chapter.xpath("title/text()")[0]
    chap_content = chapter.xpath("content/text()")[0]
    markdown_content.append(f"# {chap_title}\n\n{chap_content}\n")  # # = H1 en Markdown

# 3. �crire dans un fichier .md
with open("FirstStep/output.md", "w", encoding='utf-8') as f:
    f.write("\n".join(markdown_content))

print("Fichier Markdown : output.md")