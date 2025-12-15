from abc import ABC, abstractmethod
from typing import Optional, List, Any, Union, Dict

class MathObject(ABC):
    """
    Classe de base abstraite représentant un objet mathématique.
    
    Attributes:
        latex_symbol (str): Représentation LaTeX (ex: "f", "\\alpha").
        lean_type_hint (Optional[str]): Type Lean explicite ou inféré (ex: "Real", "group G").
        is_computable (bool): Si l'objet est calculable (implique `def` vs `noncomputable def`).
    """
    def __init__(self, latex_symbol: str = "", lean_type_hint: Optional[str] = None, is_computable: bool = True):
        self.latex_symbol = latex_symbol
        self.lean_type_hint = lean_type_hint
        self.is_computable = is_computable

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.latex_symbol or 'anon'} : {self.lean_type_hint}>"

class MScalar(MathObject):
    """
    Représente un scalaire (Entier, Réel, Complexe).
    Gère la hiérarchie numérique.
    """
    TYPE_NAT = "Nat"
    TYPE_INT = "Int"
    TYPE_REAL = "Real"
    TYPE_COMPLEX = "Complex"

    def __init__(self, scalar_type: str = "Real", value: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.scalar_type = scalar_type
        self.value = value
        if not self.lean_type_hint:
            self.lean_type_hint = scalar_type

class MSet(MathObject):
    """
    Abstraction unifiant les Ensembles (Set) et les Types (Type) de Lean.
    """
    def __init__(self, element_type: Optional[str] = None, is_type_universe: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.element_type = element_type
        self.is_type_universe = is_type_universe # True si c'est un Type (ex: Real), False si c'est un Set (ex: intervalle)
        
        if not self.lean_type_hint:
            if self.is_type_universe:
                self.lean_type_hint = "Type*"
            else:
                self.lean_type_hint = f"Set {element_type}" if element_type else "Set ?"

class MFunc(MathObject):
    """
    Représente une fonction mathématique.
    """
    def __init__(self, domain: MathObject, codomain: MathObject, body: Any = None, **kwargs):
        super().__init__(**kwargs)
        self.domain = domain
        self.codomain = codomain
        self.body = body
        
        if not self.lean_type_hint:
            # Construction basique du type de flèche
            dom_str = domain.lean_type_hint if domain.lean_type_hint else "?"
            cod_str = codomain.lean_type_hint if codomain.lean_type_hint else "?"
            self.lean_type_hint = f"{dom_str} -> {cod_str}"

class MStruct(MathObject):
    """
    Représente une structure algébrique complexe (Groupe, Espace Vectoriel).
    """
    def __init__(self, struct_name: str, carrier: Optional[MathObject] = None, **kwargs):
        super().__init__(**kwargs)
        self.struct_name = struct_name # ex: "Group", "Module"
        self.carrier = carrier # L'ensemble sous-jacent
        
        if not self.lean_type_hint:
            if carrier and carrier.latex_symbol:
               self.lean_type_hint = f"{struct_name} {carrier.latex_symbol}"
            else:
               self.lean_type_hint = struct_name

class MInductive(MathObject):
    """
    Représente un Type Inductif.
    Ex: inductive Day | monday | tuesday ...
    """
    def __init__(self, name: str, constructors: List[str], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.constructors = constructors # Liste de "constructor_name : type" ou juste noms
        self.lean_type_hint = f"Type {name}" # Meta-description

class MStructure(MathObject):
    """
    Représente la définition d'une Structure.
    Ex: structure Point where x : Int ...
    """
    def __init__(self, name: str, fields: Dict[str, str], extends: List[str] = [], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.fields = fields # nom -> type
        self.extends = extends # structures parentes

class MClass(MathObject):
    """
    Représente une Type Class.
    Ex: class Group (G : Type) ...
    """
    def __init__(self, name: str, args: List[str], fields: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.args = args
        self.fields = fields

class MInstance(MathObject):
    """
    Représente une Instance d'une classe.
    Ex: instance : Group Int where ...
    """
    def __init__(self, class_name: str, for_type: str, implementation: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.class_name = class_name
        self.for_type = for_type
        self.implementation = implementation

class MAttribute(MathObject):
    """
    Décorateur/Attribut Lean.
    Ex: @[simp]
    """
    def __init__(self, name: str, content: str = "", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.content = content

    def __str__(self):
        if self.content:
            return f"@[{self.name} {self.content}]"
        return f"@[{self.name}]"
