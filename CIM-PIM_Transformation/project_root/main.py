#!/usr/bin/env python3
# main.py
import logging
from pathlib import Path
from src.parsers.uml_parser import UMLParser
from src.doc_builder import DocumentationBuilder
from src.config import DocConfig


# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Début de la génération...")
        
        # 1. Vérification du fichier d'entrée
        input_path = Path("project_root/src/input/modele_conceptuel.xmi")
        if not input_path.exists():
            raise FileNotFoundError(f"Fichier XMI introuvable: {input_path}")
        logger.info(f"Fichier d'entrée trouvé: {input_path}") # Les messages affichés à virer après le travail 

        # 2. Parsing
        parser = UMLParser(str(input_path))
        logger.info("Parsing XMI réussi") # Les messages affichés à virer après le travail 

        # 3. Configuration
        config = DocConfig(
            title="Documentation Technique",
            authors=[{"name": "Équipe", "affiliation": "Société"}]
        )

        # 4. Génération
        builder = DocumentationBuilder(config)
        markdown = builder.build(parser)
        logger.info("Génération Markdown terminée") # Les messages affichés à virer après le travail 

        # 5. Écriture
        output_path = Path("project_root/src/output/docs.md")
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        logger.info(f"Documentation sauvegardée dans: {output_path}") # Les messages affichés à virer après le travail 

    except Exception as e:
        logger.error(f"Échec: {str(e)}", exc_info=True) # Les messages affichés à virer après le travail 

if __name__ == "__main__":
    main()