from leanbridge import LeanBridgeInterpreter, MScalar
from leanbridge.actions.commands import ActionDeclare, ActionClaim, ActionSolve

def run_demo():
    print("--- Démarrage de LeanBridge Demo ---\n")
    
    # 1. Initialiser l'interpréteur
    bridge = LeanBridgeInterpreter()
    
    # 2. Définir le scénario : "Lemme : pour tout x réel, x^2 >= 0"
    # Scénario abstrait :
    # Declare x: Real
    # Claim: x^2 >= 0
    # Solve: by sorry (default)
    
    real_x = MScalar(scalar_type=MScalar.TYPE_REAL, latex_symbol="x")
    
    actions = [
        ActionDeclare("x", real_x),
        ActionClaim("square_nonneg", "x^2 >= 0"),
        ActionSolve("sorry")
    ]
    
    # 3. Traduire
    lean_code = bridge.process(actions)
    
    # 4. Afficher le résultat
    print("### Code Lean Généré : ###")
    print(lean_code)
    print("\n------------------------------")

if __name__ == "__main__":
    run_demo()
