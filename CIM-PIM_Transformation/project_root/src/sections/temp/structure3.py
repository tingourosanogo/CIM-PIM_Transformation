from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from .base import BaseSection, SectionData
from enum import Enum, auto

class AttributeType(Enum):
    SHARED = auto()
    INDIVIDUAL = auto()
    DERIVED = auto()  # Pour les indicateurs calculés

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
    @property
    def metadata(self) -> SectionData:
        return SectionData(
            title="Structure Détaillée du Modèle",
            required_fields=['entities']
        )

    def build_content(self) -> str:
        return "\n\n".join([
            self._build_entity(entity) 
            for entity in self.data['entities']
        ])

    def _build_entity(self, entity: Dict) -> str:
        sections = [
            f"### Entité : `{entity['name']}`",
            self._build_entity_description(entity),
            self._build_attributes_section(entity),
            self._build_processes_section(entity),
            self._build_dynamics_diagram(entity)
        ]
        return "\n\n".join(filter(None, sections))

    def _build_entity_description(self, entity: Dict) -> str:
        description = entity.get('description', '').strip()
        examples = entity.get('examples', [])
        
        content = [
            "#### Description",
            description if description else "*Description à compléter*"
        ]
        
        if examples:
            content.append("\n**Exemples** :")
            content.extend(f"- {ex}" for ex in examples)
            
        return "\n".join(content)

    def _build_attributes_section(self, entity: Dict) -> str:
        attributes = entity.get('attributes', [])
        if not attributes:
            return "*Aucun attribut défini*"
        
        attribute_groups = self._group_attributes(attributes)
        
        content = ["#### Attributs"]
        for attr_type, attrs in attribute_groups.items():
            if not attrs:
                continue
                
            content.append(f"**{attr_type.value}** :")
            content.extend(self._format_attribute(attr) for attr in attrs)
        
        return "\n".join(content)

    def _group_attributes(self, attributes: List[Dict]) -> Dict[AttributeType, List[Dict]]:
        groups = {
            AttributeType.SHARED: [],
            AttributeType.INDIVIDUAL: [],
            AttributeType.DERIVED: []
        }
        
        for attr in attributes:
            if attr.get('is_derived'):
                groups[AttributeType.DERIVED].append(attr)
            elif attr.get('is_shared'):
                groups[AttributeType.SHARED].append(attr)
            else:
                groups[AttributeType.INDIVIDUAL].append(attr)
                
        return groups

    def _format_attribute(self, attribute: Dict) -> str:
        parts = [f"- `{attribute['name']}`"]
        
        if attribute.get('type'):
            parts.append(f" (*{attribute['type']}*)")
            
        if attribute.get('default_value'):
            parts.append(f" [défaut: {attribute['default_value']}]")
            
        if attribute.get('description'):
            parts.append(f" - {attribute['description']}")
            
        return "".join(parts)

    def _build_processes_section(self, entity: Dict) -> str:
        processes = entity.get('processes', [])
        if not processes:
            return "*Aucun processus défini*"
        
        content = ["#### Processus"]
        for process in processes:
            content.extend([
                f"##### {process['name']}",
                f"**Description** : {process.get('description', '*À compléter*')}",
                self._build_behavior_subsection(process),
                self._build_parameters_subsection(process),
                self._build_attributes_usage(process)
            ])
            
        return "\n".join(content)

    def _build_behavior_subsection(self, process: Dict) -> str:
        content = ["**Comportement** :"]
        
        if process.get('governing_equation'):
            content.append(f"\n- Équation : `{process['governing_equation']}`")
            
        if process.get('code_snippet'):
            content.append(f"\n```python\n{process['code_snippet']}\n```")
        else:
            content.append("\n*Implémentation à spécifier*")
            
        return "\n".join(content)

    def _build_parameters_subsection(self, process: Dict) -> str:
        params = process.get('parameters', [])
        return f"**Paramètres** : {', '.join(params) if params else '*Aucun*'}"

    def _build_attributes_usage(self, process: Dict) -> str:
        content = ["**Attributs Utilisés** :"]
        
        inputs = process.get('input_attrs', [])
        outputs = process.get('output_attrs', [])
        
        if inputs:
            content.append(f"\n- Entrée : {', '.join(inputs)}")
        if outputs:
            content.append(f"\n- Sortie : {', '.join(outputs)}")
            
        return "\n".join(content) if (inputs or outputs) else "*Non spécifié*"

    def _build_dynamics_diagram(self, entity: Dict) -> str:
        diagram = entity.get('dynamics_diagram')
        if not diagram:
            return ""
            
        return f"""#### Dynamiques
```mermaid
{diagram}
```"""