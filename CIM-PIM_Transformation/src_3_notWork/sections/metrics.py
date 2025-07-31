from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from .base import BaseSection, SectionData
from enum import Enum

class MetricType(Enum):
    KPI = "Indicateur Clé de Performance"
    PROCESS = "Indicateur de Processus"
    QUALITY = "Indicateur de Qualité"

@dataclass
class Metric:
    name: str
    metric_type: MetricType
    formula: str
    description: str
    related_attributes: List[str]
    calculation_frequency: Optional[str] = None
    target_value: Optional[Union[float, str]] = None
    threshold: Optional[float] = None

class MetricsSection(BaseSection):
    @property
    def metadata(self) -> SectionData:
        return SectionData(
            title="Indicateurs et Métriques",
            required_fields=['metrics']
        )

    def build_content(self) -> str:
        if not self.data['metrics']:
            return "*Aucun indicateur défini dans le modèle*"
            
        return "\n\n".join([
            self._build_metrics_summary(),
            self._build_metrics_table(),
            self._build_detailed_metrics()
        ])

    def _build_metrics_summary(self) -> str:
        """Génère un résumé statistique des indicateurs"""
        kpi_count = sum(1 for m in self.data['metrics'] if m['type'] == MetricType.KPI.name)
        return f"""
### Aperçu des Indicateurs

- **Total d'indicateurs** : {len(self.data['metrics'])}
- **KPI** : {kpi_count}
- **Indicateurs de Processus** : {len(self.data['metrics']) - kpi_count}
"""

    def _build_metrics_table(self) -> str:
        """Génère un tableau synthétique des indicateurs"""
        if not self.data['metrics']:
            return ""
    
        # Générer les lignes du tableau d'abord
        table_rows = []
        for m in self.data['metrics']:
            row = f"| {m['name']} | {MetricType[m['type']].value} | `{m['formula']}` | {m.get('frequency', 'N/A')} |"
            table_rows.append(row)
    
        # Assembler le tableau
        all_table = '\n'.join(table_rows)
        return f"""
### Tableau Synoptique

| Nom | Type | Formule | Fréquence |
|-----|------|---------|-----------|
{all_table}
"""

    def _build_detailed_metrics(self) -> str:
        """Génère la documentation détaillée pour chaque indicateur"""
        content = ["### Détails par Indicateur"]
        
        for metric in self.data['metrics']:
            content.extend([
                f"#### {metric['name']}",
                f"**Type** : {MetricType[metric['type']].value}",
                f"**Description** : {metric.get('description', '*Description manquante*')}",
                f"**Formule** : `{metric['formula']}`",
                self._build_attributes_subsection(metric),
                self._build_targets_subsection(metric),
                self._build_calculation_example(metric)
            ])
        
        return "\n\n".join(content)

    def _build_attributes_subsection(self, metric: Dict) -> str:
        attrs = metric.get('related_attributes', [])
        if not attrs:
            return "*Aucun attribut associé*"
            
        return "**Attributs Associés** :\n" + "\n".join(
            f"- `{attr}`" for attr in attrs
        )

    def _build_targets_subsection(self, metric: Dict) -> str:
        target = metric.get('target_value')
        threshold = metric.get('threshold')
        
        if not target and not threshold:
            return "*Cibles non spécifiées*"
            
        content = ["**Valeurs Cibles** :"]
        if target:
            content.append(f"- Valeur attendue : {target}")
        if threshold:
            content.append(f"- Seuil critique : {threshold}")
            
        return "\n".join(content)

    def _build_calculation_example(self, metric: Dict) -> str:
        example = metric.get('calculation_example')
        if not example:
            return "*Exemple de calcul : À fournir*"
            
        return f"""**Exemple** :
```python
{example}
```"""