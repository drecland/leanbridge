from .commands import Action
from ..inference.context import ContextManager
from ..inference.mapper import LibraryMapper

class ActionStartScope(Action):
    """
    Début d'un scope (namespace ou section).
    """
    def __init__(self, kind: str, name: str = ""):
        self.kind = kind # "namespace" ou "section"
        self.name = name

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        # On pourrait ici modifier le contexte pour préfixer les futurs noms
        if self.name:
            return f"{self.kind} {self.name}"
        return f"{self.kind}"

class ActionEndScope(Action):
    """
    Fin d'un scope.
    """
    def __init__(self, kind: str, name: str = ""):
        self.kind = kind
        self.name = name

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        if self.name:
            return f"end {self.name}"
        return f"end"
