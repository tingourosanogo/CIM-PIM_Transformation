# src/xmi_parser.py
from lxml import etree

class XMIParser:
    def __init__(self, xmi_path: str):
        self.tree = etree.parse(xmi_path)
    
    def get_classes(self) -> list:
        """Extrait les classes UML avec leurs attributs/méthodes."""
        classes = []
        for cls in self.tree.xpath("//uml:Class", namespaces={"uml": "http://www.omg.org/spec/UML/20131001"}):
            classes.append({
                "name": cls.get("name"),
                "attributes": self._get_attributes(cls),
                "methods": self._get_methods(cls)
            })
        return classes
    
    def _get_attributes(self, cls) -> list:
        return [{
            "name": attr.get("name"),
            "type": attr.get("type")
        } for attr in cls.xpath(".//ownedAttribute")]

    def _get_methods(self, cls) -> list:
        return [{
            "name": meth.get("name"),
            "parameters": self._get_parameters(meth)
        } for meth in cls.xpath(".//ownedOperation")]