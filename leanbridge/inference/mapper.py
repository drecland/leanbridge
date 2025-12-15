import yaml
from typing import Dict, Optional

class LibraryMapper:
    """
    Mappe les concepts 'Pythoniques/LaTeX' vers les noms de fonctions Mathlib.
    Utilise un fichier de configuration ou des défauts.
    """
    def __init__(self, config_path: str = "leanbridge/config.yaml"):
        self.mapping: Dict[str, str] = {}
        self._load_defaults()
        try:
            with open(config_path, 'r') as f:
                custom_config = yaml.safe_load(f)
                if custom_config and 'mapping' in custom_config:
                    self.mapping.update(custom_config['mapping'])
        except FileNotFoundError:
            pass # Utilise juste les défauts

    def _load_defaults(self):
        # Quelques défauts standard pour la démo
        self.mapping = {
            "norm": "NormedSpace.norm",
            "abs": "abs",
            "add": "Add.add",
            "mul": "Mul.mul",
            "pow": "Pow.pow",
            "ge": "ge", # Greater or equal
            "le": "le",
            "eq": "Eq",
            "Real": "Real",
            "Nat": "Nat"
        }

    def get_lean_name(self, abstract_name: str) -> str:
        return self.mapping.get(abstract_name, abstract_name)
