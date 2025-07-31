# src/xmi_parser.py
from lxml import etree

class XMIParser:
    def __init__(self, xmi_path: str):
        self.tree = etree.parse(xmi_path)
        # Namespaces simplifiés pour correspondre à votre fichier
        self.ns = {
            'xmi': 'http://schema.omg.org/spec/XMI/2.1',
            'uml': 'http://www.eclipse.org/uml2/3.0.0/UML'
        }
    
    def get_classes(self) -> list:
        """Extrait les classes UML avec leurs attributs/méthodes."""
        classes = []
        # XPath modifié pour ignorer les namespaces problématiques
        for cls in self.tree.xpath("//packagedElement[@xmi:type='uml:Class']", namespaces=self.ns):
            classes.append({
                "id": cls.get("{" + self.ns['xmi'] + "}id"),
                "name": cls.get("name"),
                "attributes": self._get_attributes(cls),
                "operations": self._get_operations(cls)
            })
        return classes
    
    def _get_attributes(self, cls) -> list:
        return [{
            "id": attr.get("{" + self.ns['xmi'] + "}id"),
            "name": attr.get("name"),
            "type": attr.get("type")
        } for attr in cls.xpath(".//ownedAttribute", namespaces=self.ns)]
    
    def _get_operations(self, cls) -> list:
        return [{
            "id": op.get("{" + self.ns['xmi'] + "}id"),
            "name": op.get("name")
        } for op in cls.xpath(".//ownedOperation", namespaces=self.ns)]

if __name__ == "__main__":
    parser = XMIParser("input/modele_conceptuel.xmi")
    classes = parser.get_classes()
    
    print("=== Classes ===")
    for cls in classes:
        print(f"\nClasse: {cls['name']} (ID: {cls['id']})")
        print("Attributs:")
        for attr in cls['attributes']:
            print(f"  - {attr['name']}: {attr.get('type', 'Non typé')} (ID: {attr['id']})")
        print("Opérations:")
        for op in cls['operations']:
            print(f"  - {op['name']} (ID: {op['id']})")