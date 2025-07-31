#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from typing import Dict, Any

from xmi_parser import XMIParser
from doc_builder import DocumentationBuilder, DocConfig

def parse_arguments():
    """Configure et parse les arguments CLI"""
    parser = argparse.ArgumentParser(
        description="Générateur de Documentation Technique à partir de modèles XMI"
    )
    parser.add_argument(
        "input_xmi",
        type=str,
        help="Chemin vers le fichier XMI d'entrée"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="documentation.md",
        help="Fichier de sortie (default: documentation.md)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "html"],
        default="markdown",
        help="Format de sortie"
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Fichier YAML de configuration optionnel"
    )
    return parser.parse_args()

def load_config(config_path: str = None) -> DocConfig:
    """Charge la configuration depuis un fichier YAML ou utilise les valeurs par défaut"""
    if config_path:
        try:
            return DocumentationBuilder.from_yaml(config_path).config
        except Exception as e:
            print(f"Erreur de chargement de la config: {e}", file=sys.stderr)
            print("Utilisation des valeurs par défaut", file=sys.stderr)
    
    # Valeurs par défaut
    return DocConfig(
        title="Documentation Générée Automatiquement",
        authors=[{"name": "Équipe de Modélisation", "affiliation": ""}],
        version="1.0.0"
    )

def extract_model_data(xmi_path: str) -> Dict[str, Any]:
    """Version ultra-robuste"""
    try:
        parser = XMIParser(xmi_path)
        return {
            'model_name': parser.get_model_name(),
            'entities': parser.get_classes(),
            'metrics': parser.get_metrics(),
            'parameters': parser.get_parameters(),
            'scenarios': parser.get_scenarios(),
            'installation': {
                'prerequisites': 'Python 3.8+',
                'pip_command': 'pip install mon-package'
            },
            "basic_usage": {
                "steps": [
                    {
                        "command": "python -m monmodele --config config.yaml",
                        "explanation": "Lancer la simulation avec configuration",
                        "expected_output": "Simulation démarrée...\nDurée: 00:00:05\nRésultats sauvegardés"
                    }
                ]
            },
            "troubleshooting": [
                {
                    "error": "ModuleNotFoundError",
                    "solution": "Vérifiez l'installation avec 'pip show monmodele'"
                }
            ]
        }

    except Exception as e:
        print(f"Erreur critique lors de l'extraction: {str(e)}")
        return {
            'model_name': 'Modèle Inconnu',
            'entities': [],
            'metrics': [],
            'parameters': [],
            'scenarios': [],
            'installation': {
                'prerequisites': 'Python 3.8+',
                'pip_command': 'pip install mon-package'
            }
        }

def generate_documentation():
    """Point d'entrée principal"""
    args = parse_arguments()
    
    # Validation du fichier d'entrée
    if not Path(args.input_xmi).exists():
        print(f"Fichier introuvable: {args.input_xmi}", file=sys.stderr)
        sys.exit(1)
    
    # Configuration
    config = load_config(args.config)
    
    try:
        # Extraction des données
        print("Extraction des données depuis le XMI...")
        model_data = extract_model_data(args.input_xmi)
        
        # Construction du document
        print("Génération de la documentation...")
        builder = DocumentationBuilder(config)
        output_content = builder.build_document(
            data=model_data,
            output_format=args.format
        )
        
        # Sauvegarde
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"Documentation générée avec succès: {args.output}")
    
    except Exception as e:
        print(f"Erreur critique: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_documentation()