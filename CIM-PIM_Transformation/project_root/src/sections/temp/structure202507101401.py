from dataclasses import dataclass
from typing import Dict, List, Optional
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

class StructureSection(BaseSection):
    """Génère la documentation structurelle avec gestion robuste des données manquantes"""
    
    # Constantes de formatage
    EMPTY_SECTION_MESSAGE = "*Section à compléter*"
    MISSING_DATA_MESSAGE = "*Donnée manquante*"
    DEFAULT_DESCRIPTION = "*Description à ajouter*"

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
                "Structure du Modèle", 
                "\n\n".join(entities_content)
            )
            
        except Exception as e:
            logger.critical(f"Erreur critique: {str(e)}")
            return self._format_main_section("Structure", "Erreur de génération de la section")

    def _has_valid_data(self) -> bool:
        """Valide la présence des données minimales"""
        return isinstance(self.data.get('entities'), list) and len(self.data['entities']) > 0

    def _format_main_section(self, title: str, content: str) -> str:
        """Formatte une section principale avec titre"""
        return f"## {title}\n\n{content.strip()}"

    def _build_entity(self, entity: Dict) -> Optional[str]:
        """Construit le contenu d'une entité avec gestion des données manquantes"""
        try:
            if not isinstance(entity, dict) or not entity.get('name'):
                logger.warning("Entité invalide ignorée")
                return None

            sections = [
                self._build_entity_header(entity),
                self._build_entity_description(entity),
                self._build_attributes_section(entity),
                self._build_processes_section(entity),
                self._build_dynamics_diagram(entity)
            ]
            return "\n\n".join(filter(None, sections))
        except Exception as e:
            logger.error(f"Erreur construction entité {entity.get('name')}: {str(e)}")
            return f"### Entité : `{entity.get('name', 'Inconnue')}`\n\n{self.EMPTY_SECTION_MESSAGE}"

    def _build_entity_header(self, entity: Dict) -> str:
        """En-tête d'entité avec fallback"""
        return f"### Entité : `{entity.get('name', 'Sans nom')}`"

    def _build_entity_description(self, entity: Dict) -> Optional[str]:
        """Description avec gestion des cas manquants"""
        try:
            description = entity.get('description', '').strip()
            examples = entity.get('examples', [])
            """
            if not description and not examples:
                return None
            """
            content = ["#### Description"]
            content.append(description if description else self.DEFAULT_DESCRIPTION)

            if examples:
                if not isinstance(examples, list):
                    raise ValueError("Le champ 'examples' doit être une liste")
                content.append("\n**Exemples** :")
                content.extend(f"- {ex}" for ex in examples if str(ex).strip())

            return "\n".join(content) if len(content) > 1 else None
        except Exception as e:
            logger.warning(f"Erreur description entité: {str(e)}")
            return "#### Description\n" + self.EMPTY_SECTION_MESSAGE

    def _build_attributes_section(self, entity: Dict) -> Optional[str]:
        """Section attributs avec validation complète"""
        try:
            attributes = entity.get('attributes', [])
            if not attributes:
                return None

            if not isinstance(attributes, list):
                raise ValueError("Les attributs doivent être une liste")

            attribute_groups = self._group_attributes(attributes)
            content = ["#### Attributs"]
            
            for attr_type, attrs in attribute_groups.items():
                if attrs:
                    content.append(f"**{attr_type.label}** :")
                    for attr in attrs:
                        attr_content = self._format_attribute(attr)
                        if attr_content:
                            content.append(attr_content)

            return "\n".join(content) if len(content) > 1 else None
        except Exception as e:
            logger.warning(f"Erreur section attributs: {str(e)}")
            return "#### Attributs\n" + self.EMPTY_SECTION_MESSAGE

    def _format_attribute(self, attribute: Dict) -> Optional[str]:
        """Formatage sécurisé d'un attribut"""
        try:
            if not isinstance(attribute, dict) or not attribute.get('name'):
                return None

            parts = [f"- `{attribute['name']}`"]
            
            if attribute.get('type'):
                parts.append(f" (*{attribute['type']}*)")
                
            if attribute.get('default_value') is not None:
                parts.append(f" [défaut: {attribute['default_value']}]")
                
            if attribute.get('description'):
                desc = str(attribute['description']).strip()
                if desc:
                    parts.append(f" - {textwrap.shorten(desc, width=100)}")
                    
            return ''.join(parts) if len(parts) > 1 else None
        except Exception:
            return None

    def _build_processes_section(self, entity: Dict) -> Optional[str]:
        """Section processus avec validation approfondie"""
        try:
            processes = entity.get('processes', [])
            if not processes:
                return None

            if not isinstance(processes, list):
                raise ValueError("Les processus doivent être une liste")

            content = ["#### Processus"]
            for process in processes:
                process_content = self._build_single_process(process)
                if process_content:
                    content.append(process_content)

            return "\n\n".join(content) if len(content) > 1 else None
        except Exception as e:
            logger.warning(f"Erreur section processus: {str(e)}")
            return "#### Processus\n" + self.EMPTY_SECTION_MESSAGE

    def _build_single_process(self, process: Dict) -> Optional[str]:
        """Construit un processus individuel avec checks"""
        try:
            if not isinstance(process, dict) or not process.get('name'):
                return None

            sections = [
                f"##### {process['name']}",
                f"**Description** : {process.get('description', self.DEFAULT_DESCRIPTION)}",
                self._build_behavior_subsection(process),
                self._build_parameters_subsection(process),
                self._build_attributes_usage(process)
            ]
            return "\n".join(filter(None, sections))
        except Exception as e:
            logger.warning(f"Erreur processus {process.get('name')}: {str(e)}")
            return None

    def _build_behavior_subsection(self, process: Dict) -> str:
        """Sous-section comportement avec fallbacks"""
        try:
            content = ["**Comportement** :"]
            
            equation = process.get('governing_equation')
            if equation and str(equation).strip():
                content.append(f"\n- Équation : `{equation}`")
                
            code = process.get('code_snippet')
            if code and str(code).strip():
                content.append(f"\n```python\n{textwrap.dedent(code).strip()}\n```")
            else:
                content.append(f"\n{self.EMPTY_SECTION_MESSAGE}")
                
            return ''.join(content)
        except Exception:
            return "**Comportement** :\n" + self.EMPTY_SECTION_MESSAGE

    def _build_parameters_subsection(self, process: Dict) -> Optional[str]:
        """Formatage des paramètres avec validation"""
        try:
            params = process.get('parameters', [])
            if not params:
                return f"**Paramètres** : {self.MISSING_DATA_MESSAGE}"

            if not isinstance(params, list):
                raise ValueError("Les paramètres doivent être une liste")

            param_list = '\n'.join(f"  - {p}" for p in params if str(p).strip())
            return f"**Paramètres** :\n{param_list if param_list else self.MISSING_DATA_MESSAGE}"
        except Exception:
            return f"**Paramètres** :\n{self.MISSING_DATA_MESSAGE}"

    def _build_attributes_usage(self, process: Dict) -> Optional[str]:
        """Usage des attributs avec checks"""
        try:
            inputs = process.get('input_attrs', [])
            outputs = process.get('output_attrs', [])
            
            if not inputs and not outputs:
                return f"**Attributs Utilisés** :\n{self.MISSING_DATA_MESSAGE}"
                
            content = ["**Attributs Utilisés** :"]
            if inputs:
                if not isinstance(inputs, list):
                    raise ValueError("input_attrs doit être une liste")
                content.append(f"\n- Entrée : {', '.join(filter(None, inputs))}")
            if outputs:
                if not isinstance(outputs, list):
                    raise ValueError("output_attrs doit être une liste")
                content.append(f"\n- Sortie : {', '.join(filter(None, outputs))}")
                
            return ''.join(content)
        except Exception:
            return f"**Attributs Utilisés** :\n{self.MISSING_DATA_MESSAGE}"

    def _build_dynamics_diagram(self, entity: Dict) -> Optional[str]:
        """Diagramme dynamique avec validation"""
        try:
            diagram = entity.get('dynamics_diagram')
            if not diagram or not str(diagram).strip():
                return None

            return f"""#### Dynamiques
```mermaid
{textwrap.dedent(diagram).strip()}
```"""
        except Exception:
            return None