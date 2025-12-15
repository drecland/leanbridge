from typing import List
from .core.objects import MathObject, MScalar, MStructure, MInductive
from .inference.context import ContextManager
from .inference.mapper import LibraryMapper
from .actions.commands import Action, ActionDefine  # Import ActionDefine
from .actions.definitions_extended import ActionDefineStructure, ActionDefineInductive
from .config.registry import Registry, TranslationTarget
from .core.scopes import ScopeManager

class LeanBridgeInterpreter:
    """
    Orchestre la traduction des actions utilisateur en code Lean.
    Version v0.2 : Supporte l'API impérative, les Scopes et le Registre.
    """
    def __init__(self, config_path: str = "leanbridge/config.yaml"):
        self.context = ContextManager()
        self.header_imports = ["import Mathlib"]
        
        # v0.2 Components
        self.config = Registry() # Registre de configuration
        self.mapper = LibraryMapper(config_path) # Pourrait utiliser le registre aussi
        self._action_buffer: List[Action] = [] # Buffer interne pour l'API impérative
        
        # Scope Factories
        self._scope_manager = ScopeManager(self)

    def Namespace(self, name: str):
        return self._scope_manager.Namespace(name)

    def Section(self, name: str = ""):
        return self._scope_manager.Section(name)

    def add_action(self, action: Action):
        """Ajoute une action au buffer courant."""
        self._action_buffer.append(action)

    def define_structure(self, name: str, fields: dict):
        """Helper pour définir une structure rapidement."""
        struct = MStructure(name, fields)
        self.add_action(ActionDefineStructure(struct))

    def define_inductive(self, name: str, constructors: list):
        """Helper pour définir un type inductif."""
        ind = MInductive(name, constructors)
        self.add_action(ActionDefineInductive(ind))
    
    # Pour compatibilité v0.1 ou usage hybride, on garde process si on lui passe une liste
    def process(self, actions: List[Action] = None) -> str:
        """
        Traite une séquence d'actions et retourne le code Lean complet.
        Si 'actions' est None, utilise le buffer interne accumulé.
        """
        target_actions = actions if actions is not None else self._action_buffer
        
        lines = []
        
        # 1. Imports
        lines.extend(self.header_imports)
        lines.append("") 
        
        # 2. Traitement des actions
        for action in target_actions:
            lean_code = action.to_lean(self.context, self.mapper)
            lines.append(lean_code)
            
        return "\n".join(lines)

