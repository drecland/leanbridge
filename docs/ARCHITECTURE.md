# Architecture Technique de LeanBridge

Ce document décrit l'organisation interne du package `leanbridge`.

## Structure des Dossiers

```text
leanbridge/
├── __init__.py          # Point d'entrée, expose l'Interpréteur principal
├── interpreter.py       # Orchestrateur (LeanBridgeInterpreter)
├── config/
│   ├── registry.py      # Singleton de configuration (Registry) - Extensibilité
│   └── ...
├── core/
│   ├── objects.py       # Hiérarchie MathObject (Scalar, Structure, Inductive...)
│   ├── scopes.py        # Gestionnaires de contexte (Namespace, Section)
│   └── ...
├── actions/
│   ├── commands.py      # Actions atomiques (Declare, Define, Claim)
│   ├── scopes.py        # Actions de début/fin de bloc
│   └── definitions_extended.py # Actions complexes (Structure, Inductive)
└── inference/
    ├── context.py       # Suivi des variables (ContextManager)
    └── mapper.py        # Traduction des symboles (LibraryMapper)
```

## Flux de Données

1.  **API Utilisateur** : L'utilisateur instancie `LeanBridgeInterpreter`.
2.  **Enregistrement** : Les appels (ex: `define_structure`) créent des objets `MathObject` (dans `core/`) et les enveloppent dans des `Action` (dans `actions/`).
3.  **Accumulation** : Ces actions sont stockées dans le buffer interne de l'interpréteur.
4.  **Traitement (`process()`)** :
    *   Le `ContextManager` (dans `inference/`) suit les variables déclarées.
    *   Chaque `Action` génère sa chaîne Lean via sa méthode `.to_lean()`.
    *   Le `LibraryMapper` (dans `inference/`) traduit les types "flous" (ex: "Entier") en types Lean concrets (ex: "Int").

## Guide d'Extensibilité (Extensibility Guide)

LeanBridge est conçu pour être étendu sans modifier le code source du noyau.

### Cas 1 : Ajouter un nouveau symbole mathématique
Utilisez le registre pour mapper un token LaTeX/Utilisateur vers une fonction Lean.

```python
interpreter.config.register_token("mon_token", target="lean", value="MaLib.MaFonction")
```

### Cas 2 : Ajouter une nouvelle commande complète
Si vous voulez gérer un concept non supporté (ex: une commande `DefineCoinductive`), vous pouvez :
1.  Créer une sous-classe de `Action`.
2.  L'ajouter manuellement via `interpreter.add_action()`.

(Une API `register_handler` est prévue pour automatiser cela dans le futur).

## Indépendance
Ce package est autonome.
*   **Zéro dépendance circulaire** : `core` ne dépend pas de `interpreter`.
*   **Zéro dépendance métier** : Aucune référence à `LeanGraph` ou à une interface graphique.
*   **Pure Python** : Dépendances minimales (`pyyaml` optionnel pour la config).
