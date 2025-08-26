# Converting CSV to JSON in Python can be achieved using either the built-in json and csv modules or the pandas library.
import csv
import json
from pathlib import Path
from typing import Dict, List

def parse_nested(text: str, field_type) -> list:
    """Parse les champs imbriqués style 'name:unit' ou 'name:value:unit'"""
    # return [item.split(':') for item in text.split('|')] if text else []
    """Parse les champs complexes pour l'initialisation avec gestion d'erreurs"""
    if not text or text.strip() == '':
        return []
    
    try:
        if field_type == 'key_value':
            # Format: "key1:value1|key2:value2"
            return [item.split(':')
                   for item in text.split('|') if ':' in item]
        
        elif field_type == 'distribution':
            # Format: "mean:10.82|sigma:0.8"
            return {item.split(':')[0]: float(item.split(':')[1]) 
                   for item in text.split('|') if ':' in item}
        
        else:
            # Format par défaut: "val1;val2;val3"
            return [item.strip() for item in text.split(';') if item.strip()]
            
    except Exception as e:
        print(f"Warning: Error parsing '{text}' as {field_type}: {str(e)}")
        return []    


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
            row['variables'] = [{'name':v[0], 'entity':v[1], 'definition':v[2], 'unit':v[3]} for v in parse_nested(row['variables'], 'key_value')]
            row['parameters'] = [{'name':p[0], 'entity':p[1], 'definition':p[2], 'unit':p[3]} for p in parse_nested(row['parameters'], 'key_value')]
    return csv_reader


def csv_to_json(csv_file_path: str, json_file_path: str, delimitor: str):
    _csv_reader = load_indicator_csv(csv_file_path, delimitor)



    # Write the data to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump({'indicators': _csv_reader}, jsonfile, indent=4, ensure_ascii=False)



#### Example usage ####
# csv_to_json()
