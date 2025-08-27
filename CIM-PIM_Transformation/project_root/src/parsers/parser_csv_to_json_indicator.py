# Converting CSV to JSON in Python can be achieved using either the built-in json and csv modules or the pandas library.
import csv
import json
from pathlib import Path
from typing import Dict, List

def parse_nested(text: str, expected_parts: int) -> list:
    """Parse les champs imbriqués style 'name:unit' ou 'name:value:unit' avec gestion d'erreurs"""
    if not text or not text.strip():
        return []
    
    result = []
    items = text.split('|')
    
    for item in items:
        if not item.strip():
            continue
            
        parts = item.split(':')
        
        # Ajouter des valeurs par défaut pour les parties manquantes
        while len(parts) < expected_parts:
            parts.append('')  # Valeur vide pour les champs manquants
        
        # Prendre seulement le nombre de parties attendu
        result.append(parts[:expected_parts])
    
    return result


"""
Using csv and json modules (Standard Approach):
Import necessary modules.
    import csv
    import json
"""

def load_indicator_csv(csv_file_path: str, delimitor: str):
    # Read CSV data and convert to a list of dictionaries
    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = list(csv.DictReader(csvfile, delimiter=delimitor))
        for row in csv_reader:
                # Parser les variables (4 parties attendues: name, entity, definition, unit)
                if 'variables' in row:
                    parsed_vars = parse_nested(row['variables'], 4)
                    row['variables'] = [{
                        'name': v[0] if len(v) > 0 else '',
                        'entity': v[1] if len(v) > 1 else '',
                        'definition': v[2] if len(v) > 2 else '',
                        'unit': v[3] if len(v) > 3 else ''
                    } for v in parsed_vars]
                else:
                    row['variables'] = []
                
                # Parser les paramètres (5 parties attendues: name, entity, definition, unit, value)
                if 'parameters' in row:
                    parsed_params = parse_nested(row['parameters'], 5)
                    row['parameters'] = [{
                        'name': p[0] if len(p) > 0 else '',
                        'entity': p[1] if len(p) > 1 else '',
                        'definition': p[2] if len(p) > 2 else '',
                        'unit': p[3] if len(p) > 3 else '',
                        'value': p[4] if len(p) > 4 else ''
                    } for p in parsed_params]
                else:
                    row['parameters'] = []
    return csv_reader


def csv_to_json(csv_file_path: str, json_file_path: str, delimitor: str):
    _csv_reader = load_indicator_csv(csv_file_path, delimitor)



    # Write the data to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump({'indicators': _csv_reader}, jsonfile, indent=4, ensure_ascii=False)



#### Example usage ####
# csv_to_json()
