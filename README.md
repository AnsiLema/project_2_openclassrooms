# Scraper de livres - Books to Scrape

Ce projet est un script Python pour scraper les données du site [Books to Scrape](http://books.toscrape.com/). Il extrait les informations des livres et les enregistre dans des fichiers CSV, tout en téléchargeant les images associées.

## Prérequis

- Python 3.x doit être installé sur votre machine.

## Installation et Utilisation

Les commandes suivantes vont être effectuées depuis votre terminal sous MacOs.

Naviguez dans le repertoire depuis lequel vous voulez executer votre script et sauvegarder vos données, à laide des commandes cd (change directory) et mkdir (make directory)

### 1. Cloner le dépôt

Clonez le dépôt contenant le script :

```
git clone https://github.com/AnsiLema/project_2_openclassrooms.git
```

### 2. Créer et activer un environnement virtuel

Créez un environnement virtuel pour isoler les dépendances du projet

```
 python3 -m venv venv
 ```
puis:

````
source env/bin/activate
````

### 3. Installer les dépendances

````
pip install -r requirements.txt
````

## Utilisation

Une fois les dépendances installées et l'environnement virtuel activé, vous pouvez exécuter le script pour scraper les données :

````
python3 scraper.py
````

Le script va :

- Créer un dossier dossier csv où les fichiers CSV seront stockés.
- Créer un dossier images où les images des livres seront téléchargées et organisées par catégorie.
- Extraire les données de chaque catégorie et les sauvegarder dans les fichiers CSV correspondants.

## Résultat

Après l'exécution du script, vous trouverez :
- Un dossier "dossier csv" contenant les fichiers CSV pour chaque catégorie de livres.
- Un dossier "images" contenant les images des livres organisées par catégorie.

## Remarque

Assurez-vous d'avoir une connexion Internet active pendant l'exécution du script, car il télécharge les données en temps réel à partir du site Books to Scrape.
Sans cela le script ne pourra fonctionner.

# Bon scraping !

A'nsi