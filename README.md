# LeanBridge

**LeanBridge** est une bibliothèque Python conçue pour servir de "Middleware Sémantique" entre des intentions mathématiques (souvent exprimées mentalement ou en LaTeX) et le langage formel [Lean 4](https://leanprover.github.io/).

Son objectif est de permettre des définitions mathématiques qui sont **"Moldable"** (modifiables comme des objets Python), **Tolérantes** (inférence de type agressive) et **Agnostiques** (indépendantes de la syntaxe Lean exacte).

## Installation

```bash
pip install leanbridge
```
ou pour le développement (depuis la source) :
```bash
git clone https://github.com/example/leanbridge
cd leanbridge
pip install -e .
```

## Quick Start
Générer un lemme mathématique valide en quelques lignes.

```python
from leanbridge import LeanBridgeInterpreter

# 1. Initialiser
bridge = LeanBridgeInterpreter()

# 2. Définir un espace de travail (Namespace)
with bridge.Namespace("Tutoriel"):
    
    # 3. Définir une structure
    bridge.define_structure("Vecteur2D", {"x": "Int", "y": "Int"})
    
    # 4. Compiler
    print(bridge.process())
```

**Sortie Lean générée :**
```lean
import Mathlib

namespace Tutoriel
structure Vecteur2D where
  x : Int
  y : Int
end Tutoriel
```

## Philosophie
LeanBridge ne cherche pas à remplacer Lean, mais à **réduire la friction** d'entrée. 
- **Indépendance :** Le package ne dépend d'aucune autre logique métier (pas de LeanGraph ici).
- **Extensibilité :** Tout est configuralbe via le `Registry`.

Voir [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) pour les détails techniques.
