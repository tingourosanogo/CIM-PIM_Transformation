# Structure et dynamique

## Entité : Espace

### Documentation

*Description de l’entité:*

![](media/193811768d4a531b054ee3741d6599fc.png)

L’espace est la zone géographique du territoire. Elle comprend les occupations des sols (espace-cultivé, eau-de-surface, habitat, végétation-naturelle, zone-rocheuse), les types de sol (sablonneux, gravillonnaire,etc..).

### Attributs partagés

Les attributs dont la valeur est la même pour toutes les instances et fixe dans la simulation :

| **Paramètre** | **Commentaire**                                 | **Unité** |
|---------------|-------------------------------------------------|-----------|
| *xxx*         | *explication*                                   | *unit*    |
| …             | …                                               | …         |
| territoire    | Espace géographique définissant la zone d’étude | polygone  |

Les variables dont la valeur est la même pour toutes les instances et évolue au cours de la simulation :

| **Variable d’état** | **Commentaire**           | **Unité** |
|---------------------|---------------------------|-----------|
| *yyy_s*             | *explication*             | *type*    |
| …                   | …                         | …         |
| land-cover          | unité d’occupation du sol | ha        |

### Attributs individuels

Les attributs dont la valeur est différente pour chaque instance et fixe dans la simulation :

| **Paramètre** | **Commentaire**                    | **Unité**                   |
|---------------|------------------------------------|-----------------------------|
|               |                                    |                             |
| type-de-sol   | le type du sol (pour la fertilité) | {sableux,gravillonaire,...} |

Les attributs dont la valeur est différente pour chaque instance et évolue au cours de la simulation :

| **Variable d’état**     | **Commentaire**                                                | **Unité**                                                 |
|-------------------------|----------------------------------------------------------------|-----------------------------------------------------------|
| fertilité               | fertilité du sol                                               | kgN                                                       |
| feces                   | les fèces déposé sur le sol pendant un an                      | kgMS                                                      |
| engrais-organique       | quantité d’engrais organique déposé dans l’espace chaque année | kgMS                                                      |
| résidus-de-culture      | ce qui reste de biomasse après récolte                         | kgMS                                                      |
| biomasse-broutable      | la biomasse consommable par les troupeaux                      | kgMS                                                      |
| porteurs-de-ressource   | ensemble des porteurs de ressource sur l’espace                | ensemble de porteurs de ressource = 2porteur-de-ressource |
| surface                 | la surface de l’exploitation                                   | ha                                                        |
| surface-1               | la surface de l’exploitation l’année précédente                | ha                                                        |
| lc-eau-de-surface       | surface de l’espace en eau de surface                          | ha                                                        |
| lc-espace-cultivé       | surface de l’espace en espace cultivé                          | ha                                                        |
| lc-habitat              | surface de l’espace en habitat                                 | ha                                                        |
| lc-végétation-naturelle | surface de l’espace en végétation naturelle                    | ha                                                        |
| lc-zone-rocheuse        | surface de l’espace en zone rocheuse                           | ha                                                        |
| lu-corridor             | surface prise par les corridors de passage des troupeaux       | ha                                                        |
| ...                     |                                                                |                                                           |

### Questions ouvertes

*Liste des points à discuter.*

### Dynamiques

*Description de la dynamique globale de l’entité EEE. Suis la définition de chaque dynamique particulière.*

L’espace n’est soumis qu’au processus de minéralisation dans le sol.

#### Processus : minéralisation

##### Documentation

Documentation du processus PPP avec justifications et références éventuelles.

##### Attributs

Le processus dépend des variables suivantes :

| **Variables d’état** | **Entité** | **Définition**                            | **Unité** |
|----------------------|------------|-------------------------------------------|-----------|
| feces                | Espace     | les fèces déposé sur le sol pendant un an | kgMS      |
| résidus-de-culture   | Plante     | ce qui reste de biomasse après récolte    | kgMS      |

Le processus agit sur les variables suivantes :

| **Variables d’état** | **Entité** | **Définition**      | **Unité** |
|----------------------|------------|---------------------|-----------|
| fertilité            | Espace     | la fertilité du sol | kgN       |
| …                    |            | …                   | …         |

et dépend des paramètres suivants :

| **Paramètres**             | **Entité** | **Définition**                                              | **Unité**                |
|----------------------------|------------|-------------------------------------------------------------|--------------------------|
| taux-contribution-feces    | Espace     | contribution des fèces à la teneur du sol en N              | type-de-sol -\> kgN/kgMS |
| taux-contribution-résidus  | Espace     | contribution des résidus de culture à la teneur du sol en N | type-de-sol -\> kgN/kgMS |
| taux-contribution-engrais  | Espace     | contribution des engrais à la teneur du sol en N            | type-de-sol -\> kgN/kgMS |
| contribution-atmospherique |            | apport de l’azote atmosphérique                             | kgN/ha                   |

##### Comportement

*Description détaillée du processus avec, éventuellement des sous-processus, des équations, des diagrammes d’état ou d’activité (UML), etc.*

La fertilité dépend de l’utilisation par les porteurs de ressources de l’espace et de l’apport, dépendant du type de sol, de fèces par les troupeaux:

fertilite = fertilite

\+ *(apports d’azote)*

taux-contribution-résidus \* résidus-de-culture +

taux-contribution-feces\* feces +

taux-contribution-engrais \* engrais-organique +

taux-contribution-engrais-chimique\*engrais-chimique +

contribution-atmospherique \* surface-legumineuse

\- *(retraits d’azote)*

SUM_porteurs-de-ressouces(consommation-fertilité de chaque porteur-de-ressource)

La contribution atmosphérique dépend du type du sol et de la présence des légumineuses.

##### Code

Le code ou pseudo-code s’il existe pour ceux qui peuvent le comprendre.

## Entité : Plante

### Documentation

Description à ajouter

### Attributs partagés

Les attributs dont la valeur est la même pour toutes les instances et fixe dans la simulation :

| **Paramètre** | **Commentaire** | **Unité** |
|---------------|-----------------|-----------|
| *xxx*         | *explication*   | *unit*    |
| …             | …               | …         |

Les variables dont la valeur est la même pour toutes les instances et évolue au cours de la simulation :

| **Variable d’état** | **Commentaire** | **Unité** |
|---------------------|-----------------|-----------|
| *yyy_s*             | *explication*   | *type*    |
| …                   | …               | …         |

### Attributs individuels

Les attributs dont la valeur est différente pour chaque instance et fixe dans la simulation :

| **Paramètre** | **Commentaire** | **Unité** |
|---------------|-----------------|-----------|
|               |                 |           |

Les attributs dont la valeur est différente pour chaque instance et évolue au cours de la simulation :

| **Variable d’état** | **Commentaire** | **Unité** |
|---------------------|-----------------|-----------|
| ...                 |                 |           |

### Questions ouvertes

*Liste des points à discuter.*

### Dynamiques

*Description de la dynamique globale de l’entité EEE. Suis la définition de chaque dynamique particulière.*

L’espace n’est soumis qu’au processus de minéralisation dans le sol.

#### Processus : minéralisation

##### Documentation

Documentation du processus PPP avec justifications et références éventuelles.

##### Attributs

Le processus dépend des variables suivantes :

| **Variables d’état** | **Entité** | **Définition** | **Unité** |
|----------------------|------------|----------------|-----------|
| **…**                |            |                |           |

Le processus agit sur les variables suivantes :

| **Variables d’état** | **Entité** | **Définition** | **Unité** |
|----------------------|------------|----------------|-----------|
| **…**                |            |                |           |

et dépend des paramètres suivants :

| **Paramètres** | **Entité** | **Définition** | **Unité** |
|----------------|------------|----------------|-----------|
| **…**          |            |                |           |

##### Comportement

A compléter

##### 

##### Code

Le code ou pseudo-code s’il existe pour ceux qui peuvent le comprendre.

A compléter




def _build_operations_section(self, entity: Dict) -> Optional[str]:
    """Section pour les opérations/méthodes (transformées en Processus)"""
    operations = entity.get('processes', [])
    """ 
    if not operations:
        return None
    """

    content = ["### Dynamiques"]
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
