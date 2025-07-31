from dataclasses import dataclass
from typing import Dict, List, Optional
from .base import BaseSection, SectionData
from enum import Enum

class UserLevel(Enum):
    BEGINNER = "Débutant"
    INTERMEDIATE = "Intermédiaire"
    ADVANCED = "Avancé"

@dataclass
class TutorialStep:
    command: str
    explanation: str
    expected_output: Optional[str] = None

class UserManualSection(BaseSection):
    @property
    def metadata(self) -> SectionData:
        return SectionData(
            title="Manuel Utilisateur",
            required_fields=['installation', 'basic_usage']
        )

    def build_content(self) -> str:
        return "\n\n".join([
            self._build_installation_section(),
            self._build_quickstart_guide(),
            self._build_usage_examples(),
            self._build_troubleshooting(),
            self._build_faq_section()
        ])

    def _build_installation_section(self) -> str:
        """Guide d'installation détaillé"""
        install = self.data['installation']
        return f"""
## 5.1 Installation

### Prérequis
- {install.get('prerequisites', '*À spécifier*')}

### Procédure
```bash
# Installation via pip
{install['pip_command']}

# Vérification
{install.get('verify_command', 'python -c "import package_name; print(package_name.__version__)"')}
```"""

    def _build_quickstart_guide(self) -> str:
        """Version corrigée sans problèmes de backslash"""
        steps = self.data['basic_usage']['steps']
        if not steps:
            return ""
    
        guide_lines = []
        for i, step in enumerate(steps, 1):
            step_content = [
                f"**Étape {i}** : {step['explanation']}",
                f"```bash\n{step['command']}\n```"
            ]
        
            if output := self._add_expected_output(step):
                step_content.append(output)
        
        guide_lines.append("\n".join(step_content))
        return "## 5.2 Démarrage Rapide\n\n" + "\n\n".join(guide_lines)

def _add_expected_output(self, step: Dict) -> str:
    """Version simplifiée"""
    if 'expected_output' not in step:
        return ""
    return f"**Résultat attendu** :\n```\n{step['expected_output']}\n```"
    
    def _add_expected_output(self, step: Dict) -> str:
        if 'expected_output' not in step:
            return ""
        return f"**Résultat attendu** :\n'''\n{step['expected_output']}\n'''"

def _build_usage_examples(self) -> str:
    """Exemples avancés par niveau"""
    examples = self.data.get('advanced_examples', {})
    content = ["## 5.3 Exemples d'Utilisation"]
    
    for level in UserLevel:
        if level.name.lower() in examples:
            content.append(f"""
            Niveau {level.value}
            {examples[level.name.lower()]}
            """)
        return "\n".join(content)

def _build_troubleshooting(self) -> str:
    """Guide de dépannage"""
    issues = self.data.get('troubleshooting', [])
    if not issues:
        return ""
    
    prob_solution = "\n".join(
                f"""
                Problème : {issue['error']}
                Solution : {issue['solution']}
                """
                for issue in issues
            )
    return f"""
            {prob_solution}"""

def _build_faq_section(self) -> str:
    """Questions fréquentes"""
    faqs = self.data.get('faq', [])
    if not faqs:
        return ""
    
    faq_list = "\n".join(
            f"""
            Q : {faq['question']}
            R : {faq['answer']}
            """
            for faq in faqs
            )
    return f"""
            {faq_list}"""

def _validate_data(self, data: Dict):
    required = ['installation', 'basic_usage']
    missing = [field for field in required if field not in data]
    
    if missing:
        # Fournit des valeurs par défaut au lieu de lever une exception
        if 'basic_usage' not in data:
            data['basic_usage'] = {
                'steps': [{
                    'command': 'python -m monmodele',
                    'explanation': 'Commande de base pour démarrer',
                    'expected_output': 'Modèle initialisé'
                }]
            }