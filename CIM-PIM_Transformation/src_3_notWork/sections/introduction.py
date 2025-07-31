from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from .base import BaseSection, SectionData

@dataclass
class Author:
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None

class IntroductionSection(BaseSection):
    @property
    def metadata(self) -> SectionData:
        return SectionData(
            title="Introduction",
            required_fields=['model_name']
        )

    def build_content(self) -> str:
        return "\n".join([
            self._build_header(),
            self._build_objectives(),
            self._build_scope(),
            self._build_diagram(),
            self._build_version_info()
        ])

    def _build_header(self) -> str:
        authors = self.data.get('authors', [])
        return f"""### Modèle : {self.data['model_name']}

**Auteurs** :
{self._format_authors(authors)}"""

    def _build_version_info(self) -> str:
        version = self.data.get('version', datetime.now().strftime("%Y-%m-%d"))
        return f"""
**Version** : {version}  
**Dernière mise à jour** : {datetime.now().strftime("%d/%m/%Y")}"""

    def _format_authors(self, authors: List[Author]) -> str:
        if not authors:
            return "- *À compléter*"
        
        formatted = []
        for author in authors:
            parts = [f"- {author.name}"]
            if author.affiliation:
                parts.append(f"({author.affiliation})")
            if author.email:
                parts.append(f"<{author.email}>")
            formatted.append(" ".join(parts))
        return "\n".join(formatted)

    def _build_objectives(self) -> str:
        objectives = self.data.get('objectives')
        if not objectives:
            objectives = [
                "Décrire le comportement du système",
                "Spécifier les règles métier"
            ]
        objectives_list = "\n".join(f"- {obj}" for obj in objectives)
        return f"""
### Objectifs
{objectives_list}"""

    def _build_scope(self) -> str:
        scope = self.data.get('scope')
        if not scope:
            scope = "*À compléter : périmètre couvert et limites du modèle*"
        return f"""
### Portée
{scope}"""

    def _build_diagram(self) -> str:
        diagram = self.data.get('overview_diagram')
        if diagram:
            return f"""
### Vue d'Ensemble
```mermaid
{diagram}
```"""
        return """
### Vue d'Ensemble
*À compléter : diagramme des composants principaux*"""

