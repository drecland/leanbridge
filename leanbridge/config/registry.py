from typing import Dict, Any, Optional, Callable, Type

class TranslationTarget:
    LEAN = "lean"
    LATEX = "latex"

class Registry:
    """
    Registre central pour la configuration dynamique de LeanBridge.
    Permet d'enregistrer des mappings symboliques et des handlers de commandes.
    """
    def __init__(self):
        # Mappings simples : token -> traduction
        self.rewrites: Dict[str, Dict[str, str]] = {
            TranslationTarget.LEAN: {},
            TranslationTarget.LATEX: {}
        }
        # Handlers avancés pour des comportements spécifiques
        self.handlers: Dict[str, Callable] = {}

    def register_token(self, token: str, target: str, value: str):
        """
        Enregistre une traduction simple.
        Ex: register_token("mon_symbole", Target.LEAN, "MySpecialOp")
        """
        if target not in self.rewrites:
            self.rewrites[target] = {}
        self.rewrites[target][token] = value
    
    def get_token(self, token: str, target: str) -> Optional[str]:
        return self.rewrites.get(target, {}).get(token)

    def register_handler(self, command_name: str, handler: Callable):
        self.handlers[command_name] = handler
