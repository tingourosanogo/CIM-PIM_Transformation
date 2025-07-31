# src/main.py
from xmi_parser import XMIParser
from doc_builder import DocBuilder

def main():
    parser = XMIParser("input/modele_conceptuel.xmi")
    classes = parser.get_classes()
    md = DocBuilder.build_structure_section(classes)
    
    with open("output/documentation2.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    main()