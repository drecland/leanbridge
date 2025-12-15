from leanbridge import LeanBridgeInterpreter
from leanbridge.config import TranslationTarget
from leanbridge.actions.commands import ActionRaw, ActionDefine

def run_alpha_demo():
    print("--- LeanBridge Alpha v0.2 Demo ---\n")
    
    # 1. Instanciation
    interpreter = LeanBridgeInterpreter()
    
    # 2. Configuration (Maniabilité)
    # On enregistre un token personnalisé (juste pour montrer l'API)
    interpreter.config.register_token("mon_symbole", TranslationTarget.LEAN, "MySpecialOp")
    
    # 3. Usage Impératif avec Scopes
    
    # On peut ajouter des actions directement
    interpreter.add_action(ActionRaw("-- Début de la géométrie générée automatiquement"))

    with interpreter.Namespace("Geometrie"):
        
        # Définition d'une structure
        # structure Point where x : Int ...
        interpreter.define_structure("Point", fields={"x": "Int", "y": "Int"})
        
        # Définition d'un type inductif (Formes simples)
        interpreter.define_inductive("Shape", [
            "circle (center : Point) (radius : Nat)",
            "rectangle (p1 : Point) (p2 : Point)"
        ])
        
        with interpreter.Section("Operations"):
            # Une définition simple
            # def origine := Point.mk 0 0
            # Note: On utilise ici directement ActionDefine classique 
            # (on pourrait faire un helper define() aussi)
            interpreter.add_action(ActionDefine(
                name="origine", 
                value_expr="{ x := 0, y := 0 }", 
                type_hint="Point"
            ))
            
    # Fin automatique des scopes via le context manager
    
    # 4. Compilation
    print("### Résultat Lean 4 : ###")
    print(interpreter.process()) # Utilise le buffer interne
    print("\n-------------------------")

if __name__ == "__main__":
    run_alpha_demo()
