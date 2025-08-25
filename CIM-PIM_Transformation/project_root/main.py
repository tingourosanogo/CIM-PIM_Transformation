#!/usr/bin/env python3
# main.py
import logging
import json
from pathlib import Path
from src.sections.structure import StructureSection
from src.sections.indicators import IndicatorsSection
from src.sections.initialization import InitializationSection
from src.parsers.yaml_to_json import yaml_to_json
from src.parsers.csv_to_json import csv_to_json
from src.loader.indicator_loader import IndicatorLoader
from src.loader.initialization_loader import InitializationLoader
from src.parsers.uml_parser import UMLParser
from src.doc_builder import DocumentationBuilder
from src.config import DocConfig



# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    """Charge la configuration globale"""
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Erreur chargement config : {str(e)}")
        raise

def generate_documentation(output_path: str, sections) -> None:
    """Génère le document final combiné""" 
    # section for section in sections.values()
    try:
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text("\n\n".join(sections), encoding="utf-8")
        logger.info(f"Documentation générée : {output_path}")
    except Exception as e:
        logger.error(f"Erreur génération docs : {str(e)}")
        raise

def main():
    try:
        # 1. Chargement configuration
        config = load_config("config.json")

        logger.info("Début de la génération...")
        
        # 1. Vérification des fichiers d'entrée
        StructureData_path = Path(config['xmi_path'])
        IndicatorsData_path = Path(config['indicators_path'])
        InitializationData_path = Path(config['initialization_path'])
        
       
        if not StructureData_path.exists():
            raise FileNotFoundError(f"Fichier Structure introuvable: {StructureData_path}")
        logger.info(f"Fichier d'entrée trouvé: {StructureData_path}") # Les messages affichés à virer après le travail 

        if not IndicatorsData_path.exists():
            raise FileNotFoundError(f"Fichier Indicateur introuvable: {IndicatorsData_path}")
        logger.info(f"Fichier d'entrée trouvé: {IndicatorsData_path}") # Les messages affichés à virer après le travail 

        if not InitializationData_path.exists():
            raise FileNotFoundError(f"Fichier Initialisation introuvable: {InitializationData_path}")
        logger.info(f"Fichier d'entrée trouvé: {InitializationData_path}") # Les messages affichés à virer après le travail 


        # 2. Parsing des données
        ## Section Structure (XMI)
        xmi_parser = UMLParser(StructureData_path)
        builder = DocumentationBuilder(config)
        #structure_data = builder.build(xmi_parser)
        

        ## Section Indicateurs (YAML/CSV)
        indicatorsJson_path = Path(config['indicatorsJson_path'])
        indicators_format_delimitor = config['indicators_format']
        indicators_format = indicators_format_delimitor['format']
        delimitor = indicators_format_delimitor['delimitor']
        Indicator_loader = IndicatorLoader()
        indicators_data = Indicator_loader.load_indicator_data(input_path=IndicatorsData_path, output_path=indicatorsJson_path, input_format=indicators_format, delimitor=delimitor)

        with open(indicatorsJson_path, mode='r', encoding='utf-8') as f:
            indicators_data = json.load(f)

        ## Section Indicateurs (YAML/CSV)
        initializationJson_path = Path(config['initializationJson_path'])
        initialization_format_delimitor = config['initialization_format']
        initialization_format = initialization_format_delimitor['format']
        separator = initialization_format_delimitor['delimitor']
        initialization_loader = InitializationLoader()
        initialization_data = initialization_loader.load_initialization_data(input_path=InitializationData_path, output_path=initializationJson_path, input_format=initialization_format, delimitor=separator)
        
        with open(initializationJson_path, mode='r', encoding='utf-8') as f:
            initialization_data = json.load(f)

        '''
        if indicators_format ['format'] == 'yaml':
            yaml_to_json(IndicatorsData_path, indicatorsJson_path)
        elif indicators_format ['format'] == 'csv':
            delimitor = indicators_format.get('delimitor', ';')
            csv_to_json('indicators', IndicatorsData_path, indicatorsJson_path, delimitor)
        else:
            raise ValueError(f"Format d'indicateurs non supporté: {indicators_format['format']}")
        '''
        
            
        logger.debug("Données indicateur parsées: %s", indicators_data) # afficher les données parsées au console
        logger.info("Parsing XMI réussi") # Les messages affichés à virer après le travail 

        # 3. Génération des sections
        structureSect = builder.build(xmi_parser)
        indicatorsSect = IndicatorsSection(indicators_data).generate()
        initializationSect = InitializationSection(initialization_data).generate()
        sections = [
            structureSect,
            indicatorsSect,
            initializationSect
        ]
        logger.info("Génération Markdown terminée") # Les messages affichés à virer après le travail 

        # 4. Production du document final
        output_path = Path(config['output_path'])
        generate_documentation(output_path, sections)
        logger.info(f"Documentation sauvegardée dans: {output_path}") # Les messages affichés à virer après le travail 

    except Exception as e:
        logger.critical(f"Échec du processus : {str(e)}") # Les messages affichés à virer après le travail 
        return 1

    return 0
if __name__ == "__main__":
    exit(main())