from leanbridge import LeanBridgeInterpreter, MScalar
from leanbridge.actions.commands import ActionDeclare, ActionDefine, ActionClaim, ActionSolve, ActionRaw

def run_complex_translation():
    print("--- Traduction du snippet Lean complexe (Sous-semble) ---\n")
    
    bridge = LeanBridgeInterpreter()
    
    actions = []

    # 1. Imports (Via ActionRaw car c'est spécifique au fichier)
    # Note: L'interpréteur ajoute déjà 'import Mathlib' par défaut, 
    # mais pour correspondre au snippet utilisateur qui en a plein :
    actions.append(ActionRaw("-- Imports spécifiques"))
    actions.append(ActionRaw("import Mathlib.Data.Set.Basic"))
    actions.append(ActionRaw("import Mathlib.Data.Nat.Basic"))
    actions.append(ActionRaw("")) # Ligne vide

    # 2. DEFINITIONS SIMPLES
    # def carre (n : ℕ) : ℕ := n * n
    # En Python, on définirait une ActionDefine avec arguments
    actions.append(ActionDefine(
        name="carre",
        args=["(n : ℕ)"],
        type_hint="ℕ",
        value_expr="n * n"
    ))

    # def est_nul (n : ℕ) : Prop := (n = 0)
    actions.append(ActionDefine(
        name="est_nul",
        args=["(n : ℕ)"],
        type_hint="Prop",
        value_expr="(n = 0)"
    ))
    
    # def plus_un (n : ℕ) : ℕ := n + 1
    actions.append(ActionDefine(
        name="plus_un",
        args=["(n : ℕ)"],
        type_hint="ℕ",
        value_expr="n + 1"
    ))

    actions.append(ActionRaw(""))

    # 3. EXEMPLES / PREUVES
    # example : est_cinq (plus_un 4) := by rfl
    # Nous pourrions ajouter une méthode 'ActionExample', mais ActionClaim fonctionne si on omet le nom
    # Ou on utilise ActionRaw pour 'example' qui est un mot clé spécial
    actions.append(ActionRaw("example : plus_un 4 = 5 :="))
    actions.append(ActionSolve("rfl"))

    actions.append(ActionRaw(""))
    
    # example : ¬ (est_nul (plus_un 0)) := by simp [est_nul, plus_un]
    actions.append(ActionRaw("example : ¬ (est_nul (plus_un 0)) :="))
    # Ici on utilise ActionSolve avec une tactique complexe
    actions.append(ActionSolve("simp [est_nul, plus_un]"))

    actions.append(ActionRaw(""))

    # 4. STRUCTURES & NAMESPACES (Avancé)
    # LeanBridge v0.1 n'a pas d'objets 'MNamespace' ou 'MStructure' dédiés, donc on utilise Raw
    # C'est la philosophie "Middleware" : ce qu'on ne comprend pas, on le laisse passer.
    
    actions.append(ActionRaw("namespace DefParadigma"))
    actions.append(ActionRaw(""))
    
    # structure ParadigmInterne (E F I : Type*) where ...
    # On peut imaginer construire cette string en Python si on avait les données
    struct_def = """structure ParadigmInterne (E F I : Type*) where
  sigma : E → I
  f     : I → (E → F)"""
    actions.append(ActionRaw(struct_def))
    
    actions.append(ActionRaw("end DefParadigma"))

    # 5. GÉNÉRATION
    lean_code = bridge.process(actions)
    
    print("### Code Lean Généré par LeanBridge : ###")
    print(lean_code)
    print("\n------------------------------")
    print("Note : LeanBridge combine des abstractions Pythoniques (ActionDefine) pour la logique métier")
    print("et des passes-plats (ActionRaw) pour la syntaxe Lean spécifique non encore modélisée.")

if __name__ == "__main__":
    run_complex_translation()
