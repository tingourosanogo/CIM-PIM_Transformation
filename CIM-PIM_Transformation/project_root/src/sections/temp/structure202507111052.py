from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum, auto
from .base import BaseSection
import logging
import textwrap

logger = logging.getLogger(__name__)

class StructureSection(BaseSection):
    """Génère la documentation structurelle à partir du modèle XMI"""
    
    # Constantes pour les messages
    DEFAULT_DESC = "*Description à compléter*"
    MISSING_DATA = "..."
    EMPTY_SECTION = "*Section vide : à compléter manuellement*"
    GUIDE_ROW = "| ... | ... | ... |"
    MISSING_DATA_MESSAGE = "*A compléter*"
    
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

    def _has_valid_data(self) -> bool:
        """Valide la présence des données minimales"""
        return isinstance(self.data.get('entities'), list) and len(self.data['entities']) > 0

    def _format_main_section(self, title: str, content: str) -> str:
        """Formatte une section principale avec titre"""
        return f"# {title}\n\n{content.strip()}"

    def _build_entity(self, entity: Dict) -> str:
        """Construit la documentation pour une classe UML"""
        sections = [
            f"## Entité : {entity.get('name', 'Sans nom')}",
            self._build_description(entity),
            self._build_attributes_section(entity),
            self._build_operations_section(entity),
        ] #self._build_dynamics(entity)
        return "\n\n".join(filter(None, sections))

    ####_________Fonction pour la description de l'entité_________####
    def _build_description(self, entity: Dict) -> str:
        """Section description avec image optionnelle"""
        
        try:
            description = entity.get('documentation', '').strip()
            """
            if not description:
                return None
            """
            content = ["### Documentation"]
            content.append(description if description else self.DEFAULT_DESC)

            return "\n".join(content) if len(content) > 1 else None
        except Exception as e:
            logger.warning(f"Erreur description entité: {str(e)}")
            return "### Documentation\n" + self.EMPTY_SECTION
    
    ####_________Fonction pour les attributs de l'entité_________####
    def _build_attributes_section(self, entity: Dict) -> str:
        """Section attributs avec tableaux guides systématiques"""
        """Génère la section des attributs d'une entité"""
        attrs = entity.get('attributes', [])
            
        
        # Catégorisation des attributs
        shared_fixed = []
        shared_var = []
        individual_fixed = []
        individual_var = []
        for attr in attrs:
            if attr.get('stereotype') == 'shared_fixed':  
                shared_fixed.append(attr)
            elif attr.get('stereotype') == 'shared_variable':  
                shared_var.append(attr)
            elif attr.get('stereotype') == 'individual_variable':  # Par défaut considérés comme individuels fixes
                individual_var.append(attr)
            else:
                individual_fixed.append(attr)

        content = ["### Attributs"]
        
        # Tableau guide systématique pour chaque catégorie
        content.append("\n**Attributs partagés (fixes)** \n\n Les attributs dont la valeur est la même pour toutes les instances et fixe dans la simulation :")
        content.append(self._build_attributes_table(shared_fixed))
        
        content.append("\n**Variables partagées** \n\n Les variables dont la valeur est la même pour toutes les instances et évolue au cours de la simulation :")
        content.append(self._build_attributes_table(shared_var))
        
        content.append("\n**Attributs individuels** \n\n Les attributs dont la valeur est différente pour chaque instance et évolue au cours de la simulation :")
        content.append(self._build_attributes_table(individual_var))
        
        content.append("\n**Variables individuelles (fixes)**\n\n Les attributs dont la valeur est différente pour chaque instance et fixe dans la simulation :")
        content.append(self._build_attributes_table(individual_fixed))

        return "\n".join(content)

    ####_________Fonction qui contruit les tableaux_________####
    def _build_attributes_table(self, attributes: List[Dict]) -> str:
        """Génère une table Markdown avec ligne guide si vide"""
        headers = "| **Paramètre** | **Commentaire** | **Unité** |\n|---------------|-----------------|-----------|"
        
        if not attributes:
            return f"{headers}\n{self.GUIDE_ROW}"
        
        rows = []
        for attr in attributes:
            rows.append(
                f"| `{attr.get('name', '?')}` | "
                f"{attr.get('description', self.MISSING_DATA)} | "
                f"{attr.get('type', self.MISSING_DATA)} |"
            )
        
        return f"{headers}\n" + "\n".join(rows)


    def _build_operations_section(self, entity: Dict) -> Optional[str]:
        """Section pour les opérations/méthodes (transformées en Processus)"""

        try:
            processes = entity.get('processes', [])
            """
            if not processes:
                return None

            if not isinstance(processes, list):
                raise ValueError("Les processus doivent être une liste")
            """

            content = ["### Dynamiques"]
            if processes:
                for process in processes:
                    process_content = self._build_single_process(process)
                    if process_content:
                        content.append(process_content)
            else:
                content.append(self.EMPTY_SECTION)

            return "\n\n".join(content) if len(content) > 1 else None
        except Exception as e:
            logger.warning(f"Erreur section Dynamiques: {str(e)}")
            return "### Dynamiques\n" + self.EMPTY_SECTION

    def _build_single_process(self, process: Dict) -> Optional[str]:
        """Construit un processus individuel avec checks"""
        try:
            if not isinstance(process, dict) or not process.get('name'):
                return None

            sections = [
                f"#### Processus: {process['name']}",
                f"**Description** :\n {process.get('description', self.DEFAULT_DESC)}",
                self._build_parameters_subsection(process),
                self._build_attributes_usage(process),
                self._build_behavior_subsection(process),
                self._build_code_snippet(process)
            ]
            return "\n".join(filter(None, sections))
        except Exception as e:
            logger.warning(f"Erreur processus {process.get('name')}: {str(e)}")
            return None

    #####______________Le comportement__________________#####
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
                content.append(f"\n{self.MISSING_DATA_MESSAGE}")
                
            return ''.join(content)
        except Exception:
            return "**Comportement** :\n" + self.MISSING_DATA_MESSAGE

    #####______________Les parametres utilsés__________________#####        
    def _build_parameters_subsection(self, operation: Dict) -> str:
        """Table des paramètres pour une opération"""
        try:
            params = operation.get('parameters', [])
            if not params:
                return f"**Paramètres** : {self.MISSING_DATA_MESSAGE}"

            headers = "| **Variables** | **Entité** | **Définition** | **Unité** |\n|----------------|------------|-----------------|-----------|"
            rows = []
        
            for param in params:
                rows.append(
                    f"| {param.get('name', '?')} | "
                    f"{param.get('type', self.MISSING_DATA_MESSAGE)} | "
                    f"{param.get('direction', self.MISSING_DATA_MESSAGE)} | "
                    f"{self.MISSING_DATA_MESSAGE} |"
                )
        
            return "**Paramètres** :\n" + headers + "\n" + "\n".join(rows)
        except Exception:
            return f"**Paramètres** :\n{self.MISSING_DATA_MESSAGE}"

    def _build_operation_behavior(self, operation: Dict) -> Optional[str]:
        """Section comportement avec équation et code"""
        behavior = operation.get('body', '')
        if not behavior.strip():
            return None

        content = ["**Comportement** :"]
        
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


    def _build_code_snippet(self, process: Dict):
        return None

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

