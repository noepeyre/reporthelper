# Guide d'installation

Ce guide explique comment installer et lancer Report Helper sur Windows avec PowerShell.

## 1. Installer Python et pip

1. Ouvrez cette page dans votre navigateur : <https://www.python.org/downloads/windows/>
2. Telechargez la derniere version stable de Python 3 pour Windows.
3. Lancez l'installateur.
4. Sur le premier ecran de l'installateur, activez **Add python.exe to PATH**.
5. Cliquez sur **Install Now**.

Les installateurs recents de Python incluent `pip`. Apres l'installation, ouvrez une nouvelle fenetre PowerShell et verifiez les deux commandes :

```powershell
python --version
python -m pip --version
```

Si `pip` est manquant, lancez :

```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

## 2. Telecharger le projet

Telechargez le projet depuis GitHub, puis extrayez-le si vous avez telecharge un fichier ZIP.

Si vous utilisez Git, lancez :

```powershell
git clone https://github.com/YOUR-USERNAME/reporthelper.git
cd reporthelper
```

Si vous avez telecharge un fichier ZIP, ouvrez PowerShell dans le dossier extrait du projet.

## 3. Creer un environnement virtuel

Depuis le dossier du projet, lancez :

```powershell
python -m venv .venv
```

Cela cree un environnement Python local dans le dossier `.venv`.

## 4. Activer l'environnement virtuel

PowerShell peut bloquer l'activation des scripts par defaut. Pour autoriser l'activation uniquement dans la fenetre PowerShell actuelle, lancez :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Puis activez l'environnement :

```powershell
.\.venv\Scripts\Activate.ps1
```

Quand l'activation fonctionne, votre invite de commande commence generalement par `(.venv)`.

## 5. Installer les dependances

Avec l'environnement virtuel actif, installez les paquets requis :

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 6. Lancer Report Helper

Demarrez l'application :

```powershell
python main.py
```

La console doit indiquer que Report Helper est pret.

## 7. Utiliser les raccourcis

- Appuyez sur `F8` pour ouvrir la fenetre de configuration.
- Choisissez le slot cible, le nombre d'options du menu, l'option a selectionner, le nombre de boucles, la vitesse, l'offset aleatoire et le fichier de layout.
- Cliquez sur **Save**.
- Appuyez sur `F10` pour demarrer l'automatisation.
- Appuyez encore sur `F10` pour arreter l'automatisation.
- Appuyez sur `F9` pour quitter le programme.

L'application reste inactive tant que vous n'avez pas ouvert et enregistre la configuration au moins une fois avec `F8`.

## 8. Depannage

Si `python` n'est pas reconnu, fermez PowerShell, ouvrez une nouvelle fenetre PowerShell et reessayez. Si cela echoue encore, reinstallez Python et verifiez que **Add python.exe to PATH** est active.

Si l'activation est bloquee, lancez cette commande dans la meme fenetre PowerShell avant l'activation :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Si les dependances ne s'installent pas, mettez `pip` a jour et reessayez :

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si les raccourcis ne fonctionnent pas, verifiez que la fenetre PowerShell qui execute `python main.py` est toujours ouverte. Certains systemes peuvent necessiter de lancer PowerShell normalement depuis la session de bureau plutot que depuis un terminal restreint.

## 9. Mettre a jour plus tard

Si vous avez installe avec Git, mettez le projet a jour avec :

```powershell
git pull
```

Puis reactivez l'environnement virtuel et reinstallez les dependances si necessaire :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
