from abc import ABC, abstractmethod
from typing import Optional, Any
from ..core.objects import MathObject
from ..inference.context import ContextManager
from ..inference.mapper import LibraryMapper

class Action(ABC):
    """
    Représente une intention atomique de l'utilisateur.
    """
    @abstractmethod
    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        """Traduit l'action en code Lean."""
        pass

class ActionDeclare(Action):
    """
    Déclare une variable ou une hypothèse dans le contexte courant.
    Ex: 'Soit x un Réel' -> variable (x : Real)
    """
    def __init__(self, name: str, obj_type: MathObject, is_hypothesis: bool = False):
        self.name = name
        self.obj_type = obj_type
        self.is_hypothesis = is_hypothesis

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        # Enregistrer dans le contexte
        context.declare(self.name, self.obj_type)
        
        type_str = self.obj_type.lean_type_hint
        # Mapper les noms de types si nécessaire (ex: "Real" -> "Real")
        type_str = mapper.get_lean_name(type_str)
        
        if self.is_hypothesis:
             # Hypothèse nommée ? Pour l'instant on garde simple : variable
             return f"variable ({self.name} : {type_str})"
        else:
             return f"variable ({self.name} : {type_str})"

class ActionRaw(Action):
    """
    Injecte du code Lean brut. Utile pour les imports, sections, ou fonctionnalités non encore supportées.
    """
    def __init__(self, content: str):
        self.content = content

    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        return self.content

class ActionDefine(Action):
    """
    Définit une nouvelle entité (fonction ou valeur).
    Ex: f(n) := n * n
    """
    def __init__(self, name: str, value_expr: Any, args: list = [], type_hint: str = None, is_computable: bool = True):
        self.name = name
        self.value_expr = value_expr 
        self.args = args # Liste de chaînes ex: ["(n : Nat)"]
        self.type_hint = type_hint # Ex: "Nat"
        self.is_computable = is_computable
        
    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        kw = "def" if self.is_computable else "noncomputable def"
        args_str = " ".join(self.args)
        if args_str:
            args_str = " " + args_str
            
        type_str = ""
        if self.type_hint:
             clean_type = mapper.get_lean_name(self.type_hint)
             type_str = f" : {clean_type}"
             
        return f"{kw} {self.name}{args_str}{type_str} := {self.value_expr}"

class ActionClaim(Action):
    """
    Affirme un lemme ou théorème.
    Ex: "x^2 >= 0"
    """
    def __init__(self, name: str, statement: str):
        self.name = name
        self.statement = statement # String formatée (ex: "x^2 >= 0")
        
    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        # Ici on entrerait typiquement dans un nouveau scope de preuve
        # context.push_scope() # géré par l'interpréteur ou ici ? 
        # Pour une action atomique, on génère juste l'en-tête.
        return f"lemma {self.name} : {self.statement}"

class ActionSolve(Action):
    """
    Termine la preuve courante.
    """
    def __init__(self, method: str = "sorry"):
        self.method = method # "sorry", "simp", "aesop"
        
    def to_lean(self, context: ContextManager, mapper: LibraryMapper) -> str:
        return f"  := by {self.method}"
