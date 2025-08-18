# Converting CSV to JSON in Python can be achieved using either the built-in json and csv modules or the pandas library.
import csv
import json

def parse_nested(text: str) -> list:
    """Parse les champs imbriqués style 'name:unit' ou 'name:value:unit'"""
    return [item.split(':') for item in text.split('|')] if text else []

"""
Using csv and json modules (Standard Approach):
Import necessary modules.
    import csv
    import json
"""

def csv_to_json(csv_file_path: str, json_file_path: str):
    # Read CSV data and convert to a list of dictionaries
    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        csv_reader = list(csv.DictReader(csvfile))
        for row in csv_reader:
            row['variables'] = [{'name':v[0], 'entity':v[1], 'definition':v[2], 'unit':v[3]} for v in parse_nested(row['variables'])]
            row['parameters'] = [{'name':p[0], 'entity':p[1], 'definition':p[2], 'unit':p[3]} for p in parse_nested(row['parameters'])]


    # Write the data to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump({'indicators': csv_reader}, jsonfile, indent=2, ensure_ascii=False)



#### Example usage ####
# csv_to_json()
