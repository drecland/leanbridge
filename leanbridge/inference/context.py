from typing import Dict, List, Optional
from ..core.objects import MathObject

class Environment:
    """
    Stocke l'état courant des variables et hypothèses.
    """
    def __init__(self):
        self.variables: Dict[str, MathObject] = {}
        self.hypotheses: Dict[str, str] = {} # nom -> énoncé (str pour l'instant)

    def add_variable(self, name: str, obj: MathObject):
        self.variables[name] = obj

    def get_variable(self, name: str) -> Optional[MathObject]:
        return self.variables.get(name)

class ContextManager:
    """
    Gère une pile d'environnements (scopes) pour l'inférence.
    """
    def __init__(self):
        self.scopes: List[Environment] = [Environment()] # Scope global par défaut

    @property
    def current_scope(self) -> Environment:
        return self.scopes[-1]

    def push_scope(self):
        """Entre dans un nouveau bloc (ex: corps d'une fonction, preuve)."""
        # Pour faire simple, on pourrait copier le scope précédent, 
        # mais ici on va juste faire une pile et chercher récursivement.
        # Pour l'instant, simplifions : chaque scope est indépendant mais a accès aux parents ?
        # Dans un premier temps, une liste simple. La recherche se fera du dernier au premier.
        self.scopes.append(Environment())

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def declare(self, name: str, obj: MathObject):
        self.current_scope.add_variable(name, obj)

    def resolve(self, name: str) -> Optional[MathObject]:
        """Cherche une variable dans la pile de scopes, du plus récent au plus ancien."""
        for scope in reversed(self.scopes):
            res = scope.get_variable(name)
            if res:
                return res
        return None
