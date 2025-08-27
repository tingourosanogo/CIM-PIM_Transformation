# intoduction_loader.py
import json
from pathlib import Path
from typing import Dict
from src.parsers.yaml_to_json import yaml_to_json

class IntroductionLoader:
    def __init__(self):
        self.supported_formats = ['csv', 'yaml', 'json']
    
    def load_introduction_data(self, input_path: str, output_path: str, input_format: str = None):
        """Charge les données d'introduction depuis différents formats"""
        path = Path(input_path)
        
        # Détection automatique du format
        if input_format is None:
            if path.suffix in ['.yaml', '.yml']:
                input_format = 'yaml'
            elif path.suffix == '.json':
                input_format = 'json'
        
        
        # Option 1: Chargement depuis YAML
        if input_format == 'yaml':
            yaml_to_json(input_path, output_path)

        # Option 2: Chargement depuis JSON
        elif input_format == 'json':
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        else:
            raise ValueError(f"Unsupported format: {input_format}")
    
  