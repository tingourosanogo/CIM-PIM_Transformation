from typing import Dict, List, Type
from sections.base import BaseSection
#from sections.constants import DEFAULT_CONFIG, DEFAULT_MODEL_NAME
from sections.introduction import IntroductionSection
from sections.structure import StructureSection
from sections.metrics import MetricsSection
from sections.initialization import InitializationSection
from sections.user_manual import UserManualSection
from dataclasses import dataclass
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    import warnings
    warnings.warn("Le module PyYAML n'est pas installé. La lecture des fichiers YAML sera désactivée.")


@dataclass
class DocConfig:
    title: str = "Documentation du Modèle"
    authors: List[Dict] = None
    version: str = "1.0.0"
    custom_css: str = None

"""
class DocConfig:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', DEFAULT_CONFIG['title'])
        self.version = kwargs.get('version', DEFAULT_CONFIG['version'])
        self.authors = kwargs.get('authors', DEFAULT_CONFIG['authors'])
"""


class DocumentationBuilder:
    def __init__(self, config: DocConfig = None):
        self.config = config if config else DocConfig()
        self.sections_order = [
            IntroductionSection,
            StructureSection,
            MetricsSection,
            InitializationSection,
            UserManualSection
        ]
        self._validate_config()

    def _validate_config(self):
        if not self.config.authors:
            self.config.authors = [{"name": "À compléter", "affiliation": ""}]

    def build_document(self, data: Dict, output_format: str = "markdown") -> str:
        """Assemble toutes les sections dans le format demandé"""
        sections_content = self._build_all_sections(data)
        
        if output_format == "markdown":
            return self._build_markdown(sections_content)
        elif output_format == "html":
            return self._build_html(sections_content)
        else:
            raise ValueError(f"Format non supporté: {output_format}")

    def _build_all_sections(self, data: Dict) -> Dict[Type[BaseSection], str]:
        """Construit chaque section séparément"""
        return {
            section_class: section_class(data).build()
            for section_class in self.sections_order
        }

    def _build_markdown(self, sections: Dict) -> str:
        """Assemble le document Markdown final"""
        content = [
            f"# {self.config.title}",
            self._build_metadata_block(),
            *[sections[section] for section in self.sections_order]
        ]
        return "\n\n".join(content)

    def _build_html(self, sections: Dict) -> str:
        """Génère un document HTML (version basique)"""
        css = f"<style>{self.config.custom_css}</style>" if self.config.custom_css else ""
        sections_html = "\n".join(
            f"<section class='{section.__name__.lower()}'>\n{content}\n</section>"
            for section, content in sections.items()
        )
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.config.title}</title>
    {css}
</head>
<body>
{sections_html}
</body>
</html>"""

    def _build_metadata_block(self) -> str:
        """Génère le bloc d'en-tête avec métadonnées"""
        authors = "\n".join(
            f"- {a['name']} ({a['affiliation']})" if a['affiliation'] else f"- {a['name']}"
            for a in self.config.authors
        )
        
        return f"""
**Version**: {self.config.version}  
**Auteurs**:  
{authors}

---
"""

    @classmethod
    def from_yaml(cls, config_path: str):
        """Méthode alternative de construction à partir d'un YAML"""
        with open(config_path) as f:
            config_data = yaml.safe_load(f)
        return cls(DocConfig(**config_data))