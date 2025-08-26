# user_manual_loader.py
import json
from pathlib import Path
from typing import Dict, Any
from src.parsers.yaml_to_json import yaml_to_json

class UserManual_Loader:
    def __init__(self):
        self.supported_formats = ['yaml']
    
    def load_userManual_data(self, input_path: str, output_path: str, input_format: str = None):
        """Charge les données de Mode d'utilisateur"""
        path = Path(input_path)
   
         # Chargement depuis YAML
        if input_format == 'yaml' or input_format == 'yml':
            yaml_to_json(input_path, output_path)
        
        else:
            raise ValueError(f"Unsupported format: {input_format}")
    
