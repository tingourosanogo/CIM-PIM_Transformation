# src/doc_builder.py
class DocBuilder:
    @staticmethod
    def build_structure_section(classes: list) -> str:
        """Génère le Markdown pour la section 'Structure'."""
        md = ["## 2. Section Structure\n"]
        for cls in classes:
            md.append(f"### Entité : {cls['name']}\n")
            md.append("#### Attributs\n")
            for attr in cls["attributes"]:
                md.append(f"- `{attr['name']}` : {attr.get('type', 'Non typé')}\n")
            md.append("\n#### Processus\n")
            for meth in cls["methods"]:
                md.append(f"- **{meth['name']}**\n")
                md.append(f"  - Comportement : *À décrire manuellement*\n")
                md.append(f"  - Paramètres : {', '.join(meth['parameters'])}\n")
        return "\n".join(md)