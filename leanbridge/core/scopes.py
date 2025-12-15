from typing import List
from ..actions.commands import Action
from ..actions.scopes import ActionStartScope, ActionEndScope

class ScopeContext:
    """
    Context manager générique pour Namespace et Section.
    """
    def __init__(self, interpreter, kind: str, name: str):
        self.interpreter = interpreter
        self.kind = kind
        self.name = name

    def __enter__(self):
        # Ajouter l'action d'ouverture à l'interpréteur
        action = ActionStartScope(self.kind, self.name)
        self.interpreter.add_action(action)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ajouter l'action de fermeture
        action = ActionEndScope(self.kind, self.name)
        self.interpreter.add_action(action)

class ScopeManager:
    """
    Mixin ou Helper pour l'interpréteur pour créer des scopes.
    """
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def Namespace(self, name: str) -> ScopeContext:
        return ScopeContext(self.interpreter, "namespace", name)

    def Section(self, name: str = "") -> ScopeContext:
        return ScopeContext(self.interpreter, "section", name)
