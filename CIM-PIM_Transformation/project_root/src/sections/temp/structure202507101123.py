from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum, auto
from .base import BaseSection
from ..exceptions import SectionGenerationError
import logging
import textwrap

logger = logging.getLogger(__name__)

class AttributeType(Enum):
    SHARED = ("Partagé", auto())
    INDIVIDUAL = ("Individuel", auto())
    DERIVED = ("Calculé", auto())

    @property
    def label(self):
        return self.value[0]

@dataclass
class EntityProcess:
    name: str
    description: str
    parameters: List[str]
    input_attrs: List[str]
    output_attrs: List[str]
    governing_equation: Optional[str] = None
    code_snippet: Optional[str] = None

class StructureSection(BaseSection):
    """Section de documentation structurelle avec gestion avancée du formatage"""
    
    NEWLINE = "\n"
    DOUBLE_NEWLINE = "\n\n"
    SECTION_PADDING = 1  # Nombre de lignes vides entre sections

    def generate(self) -> str:
        """Génère la section avec gestion robuste des espaces"""
        try:
            if not self._safe_get(self.data, 'entities'):
                return self._format_section("Structure", "*Aucune entité trouvée*")

            entities_content = []
            for entity in self.data['entities']:
                entity_content = self._build_entity(entity)
                if entity_content.strip():
                    entities_content.append(entity_content)

            return self._format_section(
                "Structure du Modèle", 
                self.DOUBLE_NEWLINE.join(entities_content)
            )
            
        except Exception as e:
            raise SectionGenerationError("Structure", e)

    def _build_entity(self, entity: Dict) -> str:
        """Construit le contenu d'une entité avec gestion des espaces"""
        sections = [
            self._format_entity_header(entity),
            self._build_entity_description(entity),
            self._build_attributes_section(entity),
            self._build_processes_section(entity),
            self._build_dynamics_diagram(entity)
        ]
        return self.DOUBLE_NEWLINE.join(filter(None, sections))

    def _format_section(self, title: str, content: str) -> str:
        """Formatte une section avec titre et contenu"""
        return f"## {title}{self.DOUBLE_NEWLINE}{content.strip()}"

    def _format_entity_header(self, entity: Dict) -> str:
        """Formatte l'en-tête d'entité avec gestion des espaces"""
        return f"### Entité : `{entity['name']}`"

    def _build_entity_description(self, entity: Dict) -> Optional[str]:
        """Construit la description avec gestion des espaces"""
        description = entity.get('description', '').strip()
        examples = entity.get('examples', [])
          
        content = ["#### Description"]
        if description:
            content.append(textwrap.dedent(description))
        else:
            content.append("*Description à compléter*")
            
        if examples:
            content.append(self.NEWLINE + "**Exemples** :")
            content.extend(f"- {ex}" for ex in examples)
            
        return self.NEWLINE.join(content)

    def _build_attributes_section(self, entity: Dict) -> Optional[str]:
        """Génère la section attributs avec formatage contrôlé"""
        attributes = entity.get('attributes', [])
        if not attributes:
            return None
        
        attribute_groups = self._group_attributes(attributes)
        content = ["#### Attributs"]
        
        for attr_type, attrs in attribute_groups.items():
            if attrs:
                content.append(f"**{attr_type.label}** :")
                content.extend(self._format_attribute(attr) for attr in attrs)
        
        return self.NEWLINE.join(content)

    def _group_attributes(self, attributes: List[Dict]) -> Dict[AttributeType, List[Dict]]:
        """Classe les attributs par type"""
        groups = {t: [] for t in AttributeType}
        
        for attr in attributes:
            try:
                if attr.get('is_derived'):
                    groups[AttributeType.DERIVED].append(attr)
                elif attr.get('is_shared'):
                    groups[AttributeType.SHARED].append(attr)
                else:
                    groups[AttributeType.INDIVIDUAL].append(attr)
            except Exception as e:
                logger.warning(f"Erreur classification attribut: {str(e)}")
                groups[AttributeType.INDIVIDUAL].append(attr)
                
        return groups

    def _format_attribute(self, attribute: Dict) -> str:
        """Formate un attribut avec gestion des espaces internes"""
        parts = [f"- `{attribute['name']}`"]
        
        if attribute.get('type'):
            parts.append(f" (*{attribute['type']}*)")
            
        if attribute.get('default_value') is not None:
            parts.append(f" [défaut: {attribute['default_value']}]")
            
        if attribute.get('description'):
            parts.append(f" - {textwrap.shorten(attribute['description'], width=100)}")
            
        return ''.join(parts)

    def _build_processes_section(self, entity: Dict) -> Optional[str]:
        """Construit la section processus avec gestion précise des sauts de ligne"""
        processes = entity.get('processes', [])
        if not processes:
            return None
            
        content = ["#### Processus"]
        for process in processes:
            process_content = [
                f"##### {process['name']}",
                f"**Description** : {process.get('description', '*À compléter*')}",
                self._build_behavior_subsection(process),
                self._build_parameters_subsection(process),
                self._build_attributes_usage(process)
            ]
            content.append(self.NEWLINE.join(filter(None, process_content)))
            
        return (self.DOUBLE_NEWLINE * self.SECTION_PADDING).join(content)

    def _build_behavior_subsection(self, process: Dict) -> str:
        """Formatte le comportement avec gestion des blocs de code"""
        content = ["**Comportement** :"]
        
        if process.get('governing_equation'):
            content.append(f"{self.NEWLINE}- Équation : `{process['governing_equation']}`")
            
        if process.get('code_snippet'):
            code = textwrap.dedent(process['code_snippet']).strip()
            content.append(f"{self.NEWLINE}```python\n{code}\n```")
        else:
            content.append(f"{self.NEWLINE}*Implémentation à spécifier*")
            
        return ''.join(content)

    def _build_parameters_subsection(self, process: Dict) -> str:
        """Formatte les paramètres avec alignement"""
        params = process.get('parameters', [])
        param_list = '\n'.join(f"  - {p}" for p in params) if params else '*Aucun*'
        return f"**Paramètres** :\n{param_list}"

    def _build_attributes_usage(self, process: Dict) -> str:
        """Formatte l'usage des attributs avec alignement"""
        inputs = process.get('input_attrs', [])
        outputs = process.get('output_attrs', [])
        
        if not inputs and not outputs:
            return "*Non spécifié*"
            
        content = ["**Attributs Utilisés** :"]
        if inputs:
            content.append(f"{self.NEWLINE}- Entrée : {', '.join(inputs)}")
        if outputs:
            content.append(f"{self.NEWLINE}- Sortie : {', '.join(outputs)}")
            
        return ''.join(content)

    def _build_dynamics_diagram(self, entity: Dict) -> Optional[str]:
        """Génère un diagramme Mermaid avec gestion des espaces"""
        diagram = entity.get('dynamics_diagram')
        if not diagram:
            return None
            
        clean_diagram = textwrap.dedent(diagram).strip()
        return f"""#### Dynamiques
```mermaid
{clean_diagram}
```"""