from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto
from .base import BaseSection
from ..exceptions import SectionGenerationError

import logging
# Configurer le logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AttributeType(Enum):
    SHARED = auto()
    INDIVIDUAL = auto()
    DERIVED = auto()

class StructureSection(BaseSection):
    def generate(self) -> str:
        try:
            if not self._safe_get(self.data, 'entities'):
                return "## Structure\n\n*Aucune entité trouvée*"

            content = ["## Structure du Modèle"]
            for entity in self.data['entities']:
                content.append(self._build_entity(entity))
            
            return "\n\n".join(content)
        except Exception as e:
            raise SectionGenerationError("Structure", e)

    def _build_entity(self, entity: Dict) -> str:
        sections = [
            f"### {entity['name']}",
            self._build_attributes(entity),
            self._build_processes(entity)
        ]
        logger.debug("Contenu généré pour l'entité %s:\n%s", entity['name'], sections) # Les messages affichés à virer après le travail 
        return "\n\n".join(filter(None, sections))

    def _build_attributes(self, entity: Dict) -> str:
        attrs = self._safe_get(entity, 'attributes', [])
        if not attrs:
            return None

        content = ["#### Attributs"]
        for attr in attrs:
            content.append(f"- `{attr['name']}`: {attr['type']}" + 
                          (" (dérivé)" if attr.get('is_derived') else ""))
        
        return "\n".join(content)

    def _build_processes(self, entity: Dict) -> str:
        processes = self._safe_get(entity, 'processes', [])
        if not processes:
            return None

        content = ["#### Processus"]
        for proc in processes:
            params = ", ".join(proc['parameters'])
            content.append(f"- **{proc['name']}**({params})")
        
        return "\n".join(content)