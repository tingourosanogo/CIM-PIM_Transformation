from lxml import etree
import subprocess

# 1. Charger le XML
xml = etree.parse("input.xml")

# 2. Générer le LaTeX dynamiquement
latex_content = []
latex_content.append(r"""
\documentclass{book}
\usepackage[utf8]{inputenc}
\begin{document}
""")

# Métadonnées (titre, auteur)
title = xml.xpath("//metadata/title/text()")[0]
author = xml.xpath("//metadata/author/text()")[0]
latex_content.append(f"\\title{{{title}}}\n\\author{{{author}}}\n\\maketitle\n")

# Chapitres
for chapter in xml.xpath("//chapters/chapter"):
    chap_title = chapter.xpath("title/text()")[0]
    chap_content = chapter.xpath("content/text()")[0]
    latex_content.append(f"\\chapter{{{chap_title}}}\n{chap_content}\n")

latex_content.append(r"\end{document}")

# 3. Écrire dans un fichier .tex
with open("output.tex", "w", encoding='utf-8') as f:
    f.write("\n".join(latex_content))

# 4. Compiler en PDF
subprocess.run(["pdflatex", "output.tex"], capture_output=True, check=True)
print("PDF sorti : output.pdf")
