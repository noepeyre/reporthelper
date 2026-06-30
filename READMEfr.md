# Report Helper

Report Helper est un petit outil Python pour Windows controle avec des raccourcis clavier globaux. Il automatise une sequence repetee de trois clics dans une application graphique en utilisant des fichiers de reference de layout.

## Demarrage Rapide

Pour un guide d'installation complet, consultez [INSTALLfr.md](INSTALLfr.md).

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Raccourcis

- `F8` ouvre la fenetre de configuration, uniquement quand l'automatisation est arretee.
- `F10` demarre ou arrete immediatement l'automatisation.
- `F9` quitte proprement le programme.

Au lancement, l'application ne fait rien tant que la configuration n'a pas ete ouverte et enregistree au moins une fois avec `F8`.

## Configuration

Dans la fenetre `F8`, choisissez :

- le slot cible;
- le nombre d'options du menu;
- l'option a selectionner;
- le nombre de boucles;
- la vitesse en millisecondes;
- l'offset aleatoire en pixels;
- le layout a utiliser.

Le layout est charge depuis un fichier de reference fourni avec le projet, par exemple `layout_reference.json` ou `layout_reference_v2.json`.
