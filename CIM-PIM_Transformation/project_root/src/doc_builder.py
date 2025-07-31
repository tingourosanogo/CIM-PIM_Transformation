import pprint
import logging
from typing import Dict
from .config import DocConfig
from .exceptions import DocumentationError
from src.sections.structure import StructureSection

# Configurer le logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DocumentationBuilder:
    def __init__(self, config: DocConfig):
        self.config = config
        logger.info("Builder initialisé avec config: %s", config) # Les messages affichés à virer après le travail 

    def build(self, parser) -> str:
        """Version instrumentée avec vérifications"""
        try:
            # 1. Vérification parser
            if not hasattr(parser, 'parse_to_structure'):
                raise AttributeError("Le parser doit implémenter parse_to_structure()")
            
            # 2. Parsing
            data = parser.parse_to_structure()
            logger.debug("Données parsées: %s", data)
            
            # 3. Validation données
            if not data or not isinstance(data.get('entities'), list):
                raise ValueError("Données parsées invalides")
            
            # 4. Génération
            section = StructureSection(
                data=data,
                config=self.config.structure.__dict__
            )
            content = section.generate()
            
            # 5. Validation sortie
            if not content or not content.strip():
                raise ValueError("Contenu Markdown vide")
                
            return content
            
        except Exception as e:
            logger.error("Échec de génération", exc_info=True)
            raise DocumentationError(f"Erreur lors de la génération: {str(e)}")