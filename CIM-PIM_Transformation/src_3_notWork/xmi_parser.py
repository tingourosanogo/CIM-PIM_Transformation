from lxml import etree
#from typing import List, Dict, Any  
from typing import Any, Dict, List, Optional

# Définition des constantes par défaut
# Constantes par défaut
DEFAULT_VALUES = {
    'model_name': 'Modèle Sans Nom',
    'attribute_type': 'Non typé',
    'operation_params': [],
    'metric_formula': 'Non spécifiée'
}
"""
DEFAULT_MODEL_NAME = "Modèle Sans Nom"
DEFAULT_METRICS = [
    {
        "name": "Exemple_Métrique",
        "type": "KPI",
        "formula": "À définir",
        "related_attributes": []
    }
]
"""


class XMIParser:
    def __init__(self, xmi_path: str):
        try:
            self.tree = etree.parse(xmi_path)
            self.ns = {
                'xmi': 'http://schema.omg.org/spec/XMI/2.1',
                'uml': 'http://www.eclipse.org/uml2/3.0.0/UML'
            }
        except Exception as e:
            raise ValueError(f"Erreur de lecture du fichier XMI: {str(e)}")

    def safe_xpath(self, path: str, default=None):
        # Méthode sécurisée pour les requêtes XPath
        elements = self.tree.xpath(path, namespaces=self.ns)
        return elements if elements else default

    def get_model_name(self) -> str:
        """Version robuste avec valeur par défaut"""
        try:
            model = self.tree.xpath("//uml:Model", namespaces=self.ns)
            return model[0].get("name", DEFAULT_VALUES['model_name']) if model else DEFAULT_VALUES['model_name']
        except Exception:
            return DEFAULT_VALUES['model_name']


    def get_classes(self) -> List[Dict]:
        """Version sécurisée"""
        try:
            return [
                {
                    "name": cls.get("name", "Classe Sans Nom"),
                    "attributes": self._extract_attributes(cls),
                    "operations": self._extract_operations(cls)
                }
                for cls in self.tree.xpath("//packagedElement[@xmi:type='uml:Class']", namespaces=self.ns)
            ] or []  # Retourne une liste vide si aucune classe
        except Exception as e:
            print(f"Erreur extraction classes: {str(e)}", file=sys.stderr)
            return []


    def _extract_attributes(self, cls) -> list[dict]:
        """Version sécurisée"""
        try:
            return [{
                "name": attr.get("name", "attr_sans_nom"),
                "type": attr.get("type", DEFAULT_VALUES['attribute_type']),
                "description": attr.get("documentation", "")
            } for attr in cls.xpath(".//ownedAttribute", namespaces=self.ns)
            ] or []  # Retourne une liste vide si aucun attribut
        except :
            print(f"Erreur extraction attributs")
            return []

    def _extract_operations(self, cls) -> list[dict]:
        operations = []
 
        try:
            operation_elements = cls.xpath(".//ownedOperation", namespaces=self.ns)
            if not operation_elements:
                return []
        
            for op in operation_elements:
                try:
                    operation = {
                        "name": op.get("name", "Unnamed_Operation"),
                        "parameters": self._safe_extract_parameters(op),
                        "description": self._safe_extract_documentation(op),
                        "behavior": self._safe_extract_behavior(op),
                        "used_attributes": self._safe_extract_used_attributes(op),
                        "return_type": op.get("type", DEFAULT_VALUES['attribute_type']),
                        "xmi_id": op.get("{" + self.ns['xmi'] + "}id", "")
                    }
                    operations.append(operation)
                except :
                    print(f"[WARNING] Erreur lors de l'extraction d'une opération")
                    continue
                
        except :
            print(f"[ERROR] Erreur majeure dans _extract_operations ")
            return []  # Retourne une liste vide plutôt que de faire échouer le processus
    
        return operations


    def _safe_extract_parameters(self, operation_element) -> list[str]:
        """Version sécurisée de l'extraction des paramètres"""
        try:
            return self._extract_parameters(operation_element)
        except :
            print(f"[WARNING] Erreur d'extraction des paramètres ")
            return ["?"]  # Valeur par défaut identifiable

    def _safe_extract_documentation(self, element) -> str:
        """Version sécurisée de l'extraction de documentation"""
        try:
            doc = self._extract_documentation(element)
            return doc if doc else "Aucune description disponible"
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction de documentation : {e}")
            return "Description non lisible"
        
    def _safe_extract_behavior(self, operation_element) -> str:
        """Version sécurisée de l'extraction du comportement"""
        try:
            behavior = self._extract_behavior(operation_element)
            return behavior if behavior else "Comportement non spécifié"
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction du comportement : {e}")
            return "Erreur de lecture du comportement"

    def _safe_extract_used_attributes(self, operation_element) -> dict:
        """Version sécurisée de l'extraction des attributs utilisés"""
        default = {"input": ["?"], "output": ["?"]}
        try:
            attrs = self._extract_used_attributes(operation_element)
            return attrs if attrs else default
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction des attributs utilisés : {e}")
            return default
        
    def _extract_documentation(self, element) -> str:
        """Extrait la documentation UML (commentaires)"""
        try:
            doc = element.xpath(".//ownedComment/@body", namespaces=self.ns)
            return doc[0] if doc else ""
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction de la documentation : {e}")
            return "Erreur d'extraction de la documentation"
        

    def _extract_behavior(self, operation) -> str:
        """Extrait le code de comportement depuis les tags UML"""
        # Implémentation dépendante de votre outil UML
        try:
            tags = operation.xpath(".//taggedValue[@tag='behavior']/@value", namespaces=self.ns)
            return tags[0] if tags else ""
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction du comportement : {e}")
            return "Erreur d'extraction du comportement"


        

    def _extract_used_attributes(self, operation) -> dict:
        """Extrait les attributs utilisés"""
        # À adapter selon votre modélisation
        try:
            return {
                "input": [],  # Liste des attributs d'entrée
                "output": []  # Liste des attributs impactés
            }
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction input et ouput : {e}")
            return "Erreur d'extraction input et ouput"

    def _extract_parameters(self, operation) -> list[str]:
        try:
            return [
                param.get("name")
                for param in operation.xpath(".//ownedParameter", namespaces=self.ns)
            ]
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction des parametres : {e}")
            return "Erreur d'extraction des parametres"

    def _find_documentation(self, element) -> str:
        """À compléter pour extraire la documentation UML"""
        try:
            return ""
        except Exception as e:
            print(f"[WARNING] Erreur d'extraction de la documentation : {e}")
            return "Erreur d'extraction de la documentation"
    

    def get_metrics(self) -> List[Dict]:
        """
        Extrait les indicateurs/métriques depuis le modèle XMI avec gestion sécurisée des erreurs.
        Retourne toujours une liste (potentiellement vide) de dictionnaires normalisés.
        """
        metrics = []
    
        try:
            # 1. Métriques basées sur les attributs dérivés
            derived_properties = self.tree.xpath("//uml:Property[@isDerived='true']", namespaces=self.ns) or []
        
            for attr in derived_properties:
                try:
                    metric_data = {
                        "name": attr.get("name", "Unnamed_Metric"),
                        "type": "DERIVED",
                        "formula": self._safe_extract_formula(attr),
                        "related_attributes": self._safe_get_related_attributes(attr),
                        "source": "derived_property"
                    }
                    metrics.append(metric_data)
                except :
                    print(f"[Warning] Erreur traitement attribut dérivé")
                    continue

            # 2. Métriques taggées explicitement
            comments = self.tree.xpath("//uml:Comment", namespaces=self.ns) or []
        
            for comment in comments:
                try:
                    body = comment.get("body", "")
                    if "<<metric>>" in body:
                        metric_data = {
                            "name": comment.get("name", f"Metric_{len(metrics) + 1}"),
                            "type": "TAGGED",
                            "formula": "À spécifier",
                            "description": body.replace("<<metric>>", "").strip(),
                            "source": "tagged_comment"
                        }
                        metrics.append(metric_data)
                except Exception as comment_err:
                    print(f"[Warning] Erreur traitement commentaire: {comment_err}", file=sys.stderr)
                    continue

        except Exception as global_err:
            print(f"[Error] Erreur majeure dans get_metrics(): {global_err}", file=sys.stderr)
            # Retourne les métriques déjà collectées malgré l'erreur

        return metrics or [self._get_default_metric()]  # Jamais vide


    def _safe_extract_formula(self, element) -> str:
        """Version sécurisée de l'extraction de formule"""
        """Extrait la formule depuis les contraintes OCL"""
        try:
            constraint = element.xpath(".//uml:Constraint", namespaces=self.ns)
            if constraint:
                return constraint[0].get("specification", "Formule non spécifiée")
            return "Formule non spécifiée"
        except:
            return "[Erreur extraction formule]"


    def _safe_get_related_attributes(self, element) -> List[str]:
        """Version sécurisée de l'extraction des attributs liés"""
        """Trouve les attributs utilisés dans le calcul"""
        try:
            return [
                elem.get("name", f"attr_{idx}") 
                for idx, elem in enumerate(element.xpath("../ownedAttribute", namespaces=self.ns) or [])
                if elem.get("name")
            ][:5]  # Limite à 5 attributs pour éviter les boucles infinies
        except:
            return ["Attributs non extraits"]

    def _parse_metric_comment(self, comment) -> Dict:
        """Parse les commentaires taggés comme métriques"""
        try:
            return {
                "name": f"Metric_{comment.get('name', '')}",
                "type": "TAGGED",
                "formula": "À spécifier",
                "description": comment.get("body", "").replace("<<metric>>", "").strip()
            }
        except:
            return ["Metric comment non extrait"]


    def get_parameters(self) -> List[Dict[str, Any]]:
        """Extrait les paramètres globaux du modèle XMI"""
        parameters = []
        try:
            # 1. Paramètres dans les Classes avec stéréotype <<parameter>>
            for param_class in self.tree.xpath("//uml:Class[@stereotype='parameter']", namespaces=self.ns):
                for attr in param_class.xpath(".//ownedAttribute", namespaces=self.ns):
                    parameters.append(self._build_parameter(attr, param_class.get("name")))
    
            # 2. Propriétés dans le Package racine
            root_package = self.tree.xpath("//uml:Package", namespaces=self.ns)[0]
            for prop in root_package.xpath(".//ownedAttribute", namespaces=self.ns):
                parameters.append(self._build_parameter(prop, "Global"))
    
            return parameters
        except:
            return ["Paramètres globaux non extrait"]


    def _build_parameter(self, attribute, source: str) -> Dict[str, Any]:
        """Construit un dictionnaire de paramètre standardisé"""
        try:
            return {
                "name": attribute.get("name"),
                "type": attribute.get("type", "string"),
                "default_value": self._get_default_value(attribute),
                "source": source,
                "description": self._get_documentation(attribute),
                "constraints": self._get_constraints(attribute)
            }
        except:
            return ["Dictionnaire de paramètre non construit"]

    def _get_default_metric(self) -> Dict:
        """Fournit une métrique par défaut en cas d'échec complet"""
        try:
            return {
                "name": "Default_Metric",
                "type": "DEFAULT",
                "formula": "1",
                "description": "Métrique générée automatiquement",
                "related_attributes": ["default_attr"],
                "source": "system_default"
            }
        except:
            return ["Métrique par défaut non défini"]

    def _get_default_value(self, element) -> str:
        """Extrait la valeur par défaut depuis les tags ou les valeurs initiales"""
        try:
            default = element.xpath(".//defaultValue/@value", namespaces=self.ns)
            if default:
                return default[0]
            return "Non spécifié"
        except:
            return ["Valeur par défaut non défini"]

    def _get_documentation(self, element) -> str:
        """Extrait la documentation associée"""
        try:
            doc = element.xpath(".//ownedComment/@body", namespaces=self.ns)
            return doc[0] if doc else "Aucune description"
        except:
            return ["Documentation associée non trouvée"]

    def _get_constraints(self, element) -> str:
        """Extrait les contraintes OCL"""
        try:
            constraints = element.xpath(".//constraint/specification/@value", namespaces=self.ns)
            return " | ".join(constraints) if constraints else "Aucune"
        except:
            return ["Contrainte non trouvée"]



    def get_scenarios(self) -> List[Dict]:
        """Extrait les scénarios de simulation depuis le XMI"""
        scenarios = []
    
        # 1. Scénarios définis comme des Classes stéréotypées
        for scenario in self.tree.xpath("//uml:Class[contains(@name, 'Scenario_')]", namespaces=self.ns):
            scenarios.append({
                "name": scenario.get("name"),
                "parameters": self._extract_scenario_parameters(scenario)
            })
    
        # 2. Scénarios définis dans les commentaires
        for comment in self.tree.xpath("//uml:Comment[contains(@body, '<<scenario>>')]", namespaces=self.ns):
            scenarios.append(self._parse_scenario_comment(comment))
    
        return scenarios if scenarios else [
            {
                "name": "Default_Scenario",
                "description": "Scénario par défaut",
                "parameters": {}
            }
        ]

    def _extract_scenario_parameters(self, scenario) -> Dict[str, Any]:
        """Extrait les paramètres d'un scénario"""
        return {
            param.get("name"): param.get("defaultValue", "N/A")
            for param in scenario.xpath(".//ownedAttribute", namespaces=self.ns)
        }

    def _parse_scenario_comment(self, comment) -> Dict[str, Any]:
        """Parse les scénarios définis dans les commentaires"""
        return {
            "name": comment.get("name", "Unnamed_Scenario"),
            "description": comment.get("body", "").replace("<<scenario>>", "").strip(),
            "parameters": {}
        }