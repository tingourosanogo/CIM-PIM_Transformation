import yaml
import json


"""
Install yaml (if not already installed).
  pip install PyYAML
or
  pip install ruamel.yaml
"""


def yaml_to_json(yaml_file_path: str, json_file_path: str):
    # Read Yaml data 
    with open(yaml_file_path, mode='r', encoding='utf-8') as yaml_file:
        yaml_object = yaml.safe_load(yaml_file)
        # yaml_object = yaml.load(yaml_file)  # directly load without safe when we use ruamel.yaml


    # Write the data to a JSON file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(yaml_object, json_file, indent=4, ensure_ascii=False)



### Example of use
# yaml_to_json()