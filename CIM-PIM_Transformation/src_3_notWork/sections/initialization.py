from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from .base import BaseSection, SectionData
from enum import Enum

class ParameterType(Enum):
    GLOBAL = "Paramètre Global"
    ENTITY = "Paramètre d'Entité"
    SCENARIO = "Paramètre de Scénario"

@dataclass
class ModelParameter:
    name: str
    param_type: ParameterType
    data_type: str
    default_value: Union[str, float, bool]
    description: str
    constraints: Optional[str] = None

class InitializationSection(BaseSection):
    @property
    def metadata(self) -> SectionData:
        return SectionData(
            title="Initialisation du Modèle",
            required_fields=['parameters', 'scenarios']
        )

    def build_content(self) -> str:
        return "\n\n".join([
            self._build_parameters_section(),
            self._build_scenarios_section(),
            self._build_configuration_guide()
        ])

    def _build_parameters_section(self) -> str:
        """Section détaillée des paramètres"""
        if not self.data['parameters']:
            return "### Paramètres\n*Aucun paramètre défini*"
            
        params = "\n\n".join(
    self._build_parameter_table(param_type)
    for param_type in ParameterType
)
        return f"""
### Paramètres d'Initialisation

{params}
"""

    def _build_parameter_table(self, param_type: ParameterType) -> str:
        """Génère un tableau par type de paramètre"""
        params = [
            p for p in self.data['parameters'] 
            if p['type'] == param_type.name
        ]
        if not params:
            return ""
            
        param_value = "\n".join(
    f"| {p['name']} | `{p['data_type']}` | {p['default_value']} | {p.get('constraints', 'Aucune')} | {p['description']} |"
    for p in params
)
        return f"""
**{param_type.value}** :

| Nom | Type | Valeur par Défaut | Contraintes | Description |
|-----|------|-------------------|-------------|-------------|
{param_value}
"""

    def _build_scenarios_section(self) -> str:
        """Section des scénarios de simulation - Version corrigée"""
        scenarios = self.data['scenarios']
        if not scenarios:
            return "### Scénarios\n*Aucun scénario défini*"
    
        scenario_sections = []
        for scenario in scenarios:
            # Construire chaque partie séparément
            params = [
                f"- `{param}` : {value}" 
                for param, value in scenario.get('parameters', {}).items()
            ]
        
        scenario_content = [
            f"#### {scenario['name']}",
            f"**Description** : {scenario.get('description', 'Non spécifiée')}",
            "**Paramètres Spécifiques** :",
            *params  # Décompression de la liste des paramètres
        ]
        
        scenario_sections.append("\n".join(scenario_content))
    
        return "### Scénarios de Simulation\n\n" + "\n\n".join(scenario_sections)

    def _build_configuration_guide(self) -> str:
        """Guide pratique d'initialisation"""
        return """
### Guide de Configuration

1. **Fichier de Configuration** :
```yaml
# config.yaml
parameters:
  - name: param1
    value: 42
scenario: scenario1"""