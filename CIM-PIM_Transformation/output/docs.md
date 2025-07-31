## Structure du Modèle

### Entité : `Actor`

#### Attributs
**Individuel** :
- `id` (*string*)
- `type` (*string*)

### Entité : `IndividualActor`

*Aucun attribut défini*

#### Processus
##### manageResource
**Description** : *À compléter*
**Comportement** :

*Implémentation à spécifier*
**Paramètres** : resource: class_Resource
*Non spécifié*

### Entité : `Resource`

#### Attributs
**Individuel** :
- `id` (*string*)
- `quantity` (*float*)

### Entité : `FarmingActivity`

#### Attributs
**Individuel** :
- `startDate` (*date*)
- `endDate` (*date*)

### Entité : `Livestock`

#### Attributs
**Individuel** :
- `herdSize` (*integer*)

#### Processus
##### produceMeat
**Description** : *À compléter*
**Comportement** :

*Implémentation à spécifier*
**Paramètres** : *Aucun*
*Non spécifié*
##### produceMilk
**Description** : *À compléter*
**Comportement** :

*Implémentation à spécifier*
**Paramètres** : *Aucun*
*Non spécifié*

### Entité : `Plant`

#### Attributs
**Individuel** :
- `species` (*string*)
- `biomass` (*float*)

#### Processus
##### absorbNutrients
**Description** : *À compléter*
**Comportement** :

*Implémentation à spécifier*
**Paramètres** : nutrients: class_Nutrient
*Non spécifié*

### Entité : `Product`

#### Attributs
**Individuel** :
- `quality` (*float*)

### Entité : `Meat`

#### Attributs
**Individuel** :
- `cutType` (*string*)

### Entité : `Milk`

#### Attributs
**Individuel** :
- `fatContent` (*float*)

### Entité : `WaterSource`

#### Attributs
**Individuel** :
- `capacity` (*float*)

### Entité : `SurfaceWater`

*Aucun attribut défini*

### Entité : `Soil`

#### Attributs
**Individuel** :
- `fertility` (*float*)
- `compaction` (*float*)

### Entité : `Consumption`

#### Attributs
**Individuel** :
- `date` (*date*)
- `quantity` (*float*)

### Entité : `Growth`

#### Attributs
**Individuel** :
- `rate` (*float*)