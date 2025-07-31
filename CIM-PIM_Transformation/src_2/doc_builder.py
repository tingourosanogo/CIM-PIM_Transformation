# src/doc_builder.py
class DocBuilder:
    @staticmethod
    def build_structure_section(classes: list) -> str:
        """Génère le Markdown pour la section 'Structure'."""
        md = ["## 2. Section Structure\n"]
        for cls in classes:
            md.append(f"### Entité : {cls['name']}\n")
            
            # Section Attributs
            if cls.get('attributes'):
                md.append("#### Attributs\n")
                for attr in cls['attributes']:
                    md.append(f"- `{attr['name']}` : {attr.get('type', 'Non typé')}\n")
            
            # Section Processus/Méthodes
            if cls.get('operations'):
                md.append("\n#### Processus\n")
                for meth in cls['operations']:
                    md.append(f"- **{meth['name']}**\n")
                    md.append(f"  - Comportement : *À décrire manuellement*\n")
                    
                    # Gestion sécurisée des paramètres
                    params = meth.get('parameters', [])
                    if params:
                        md.append(f"  - Paramètres : {', '.join(params)}\n")
                    else:
                        md.append("  - Paramètres : *Aucun paramètre spécifié*\n")
        
        return "\n".join(md)