from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SectionData:
    """Conteneur typé pour les données de section"""
    title: str
    required_fields: List[str]

class BaseSection(ABC):
    def __init__(self, data: Dict):
        self._validate_data(data)
        self.data = data
    
    def _validate_data(self, data: Dict):
        missing = [f for f in self.metadata.required_fields if f not in data]
        if missing:
            raise ValueError(f"Champs manquants pour {self.metadata.title}: {missing}")

    @property
    @abstractmethod
    def metadata(self) -> SectionData:
        pass

    @abstractmethod
    def build_content(self) -> str:
        pass

    def build(self) -> str:
        return f"## {self.metadata.title}\n\n{self.build_content()}"