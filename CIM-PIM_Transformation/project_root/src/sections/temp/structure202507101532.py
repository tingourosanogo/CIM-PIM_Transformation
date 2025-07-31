from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto
from .base import BaseSection
import logging
import textwrap

logger = logging.getLogger(__name__)

class StructureSection(BaseSection):
    """Génère la documentation structurelle à partir du modèle XMI"""
    
    # Constantes pour les messages par défaut
    DEFAULT_DESC = "*Description à compléter*"
    MISSING_DATA = "*A compléter*"
    EMPTY_SECTION = "*Section vide*"
    
    def generate(self) -> str:
        """Point d'entrée principal avec gestion d'erreur globale"""
        try:
            if not self._has_valid_data():
                return self._format_main_section("Structure", "Aucune donnée structurelle valide trouvée")

            entities_content = []
            for entity in self.data['entities']:
                try:
                    entity_content = self._build_entity(entity)
                    if entity_content:
                        entities_content.append(entity_content)
                except Exception as e:
                    logger.error(f"Erreur génération entité: {str(e)}")
                    entities_content.append(f"<!-- Erreur génération entité -->")

            if not entities_content:
                return self._format_main_section("Structure", "Aucune entité valide à documenter")

            return self._format_main_section(
                "Structure et dynamique", 
                "\n\n".join(entities_content)
            )
            
        except Exception as e:
            logger.critical(f"Erreur critique: {str(e)}")
            return self._format_main_section("Structure", "Erreur de génération de la section")

    def _build_entity(self, entity: Dict) -> str:
        """Construit la documentation pour une classe UML"""
        sections = [
            f"## Entité : {entity.get('name', 'Sans nom')}",
            self._build_description(entity),
            self._build_attributes_section(entity),
            self._build_operations_section(entity),
            self._build_dynamics(entity)
        ]
        return "\n\n".join(filter(None, sections))

    def _build_description(self, entity: Dict) -> str:
        """Section description avec image optionnelle"""
        content = [
            "### Documentation",
            f"*Description de l'entité:*\n\n{entity.get('documentation', self.DEFAULT_DESC)}"
        ]
        
        if entity.get('image'):
            content.append(f"\n![](media/{entity['image']})")
            
        return "\n".join(content)

    def _build_attributes_section(self, entity: Dict) -> str:
        """Section attributs organisée selon le format demandé"""
        attrs = entity.get('attributes', [])
        if not attrs:
            return None

        # Catégorisation des attributs basée sur le nom ou les stéréotypes
        shared_fixed = []
        shared_var = []
        individual_fixed = []
        individual_var = []
        
        for attr in attrs:
            if '_s' in attr.get('name', ''):  # Convention pour les partagés
                shared_var.append(attr)
            elif attr.get('is_derived', False):  # Attributs calculés
                individual_var.append(attr)
            else:  # Par défaut considérés comme individuels fixes
                individual_fixed.append(attr)

        content = ["### Attributs"]
        
        if shared_fixed:
            content.append("\n**Attributs partagés (fixes):**")
            content.append(self._build_attributes_table(shared_fixed))
            
        if shared_var:
            content.append("\n**Variables partagées:**")
            content.append(self._build_attributes_table(shared_var))
            
        if individual_fixed:
            content.append("\n**Attributs individuels (fixes):**")
            content.append(self._build_attributes_table(individual_fixed))
            
        if individual_var:
            content.append("\n**Variables individuelles:**")
            content.append(self._build_attributes_table(individual_var))

        return "\n".join(content)

    def _build_attributes_table(self, attributes: List[Dict]) -> str:
        """Génère une table Markdown pour les attributs"""
        if not attributes:
            return self.EMPTY_SECTION

        headers = "| **Paramètre** | **Commentaire** | **Unité** |\n|---------------|-----------------|-----------|"
        rows = []
        
        for attr in attributes:
            rows.append(
                f"| `{attr.get('name', '?')}` | "
                f"{attr.get('description', self.MISSING_DATA)} | "
                f"{attr.get('type', self.MISSING_DATA)} |"
            )
        
        return headers + "\n" + "\n".join(rows)

    def _build_operations_section(self, entity: Dict) -> Optional[str]:
        """Section pour les opérations/méthodes (transformées en Processus)"""
        operations = entity.get('operations', [])
        if not operations:
            return None

        content = ["### Processus"]
        for op in operations:
            op_content = [
                f"#### Processus : {op.get('name', 'Sans nom')}",
                f"**Description** : {op.get('documentation', self.DEFAULT_DESC)}",
                self._build_operation_parameters(op),
                self._build_operation_behavior(op)
            ]
            content.append("\n\n".join(filter(None, op_content)))

        return "\n\n".join(content)

    def _build_operation_parameters(self, operation: Dict) -> str:
        """Table des paramètres pour une opération"""
        params = operation.get('parameters', [])
        if not params:
            return f"**Paramètres** : {self.MISSING_DATA}"

        headers = "| **Variables** | **Entité** | **Définition** | **Unité** |\n|----------------|------------|-----------------|-----------|"
        rows = []
        
        for param in params:
            rows.append(
                f"| {param.get('name', '?')} | "
                f"{param.get('type', self.MISSING_DATA)} | "
                f"{param.get('direction', self.MISSING_DATA)} | "
                f"{self.MISSING_DATA} |"
            )
        
        return "**Paramètres** :\n" + headers + "\n" + "\n".join(rows)

    def _build_operation_behavior(self, operation: Dict) -> Optional[str]:
        """Section comportement avec équation et code"""
        behavior = operation.get('body', '')
        if not behavior.strip():
            return None

        content = ["**Comportement** :"]
        
        # Extraction d'équation depuis la documentation si disponible
        doc = operation.get('documentation', '')
        if 'équation:' in doc:
            eq_start = doc.find('équation:') + len('équation:')
            equation = doc[eq_start:].split('\n')[0].strip()
            content.append(f"\n- Équation : `{equation}`")
            
        content.append(f"\n```python\n{textwrap.dedent(behavior).strip()}\n```")
        
        return "\n".join(content)

    def _build_dynamics(self, entity: Dict) -> Optional[str]:
        """Section dynamiques optionnelle"""
        if not any(op.get('name', '').lower().startswith('process') for op in entity.get('operations', [])):
            return None
            
        return "### Dynamiques\n\n*Description des dynamiques globales*"

    def _has_valid_data(self) -> bool:
        """Valide la présence des données minimales"""
        return isinstance(self.data.get('entities'), list) and len(self.data['entities']) > 0

    def _format_main_section(self, title: str, content: str) -> str:
        """Formatte une section principale avec titre"""
        return f"# {title}\n\n{content.strip()}"
