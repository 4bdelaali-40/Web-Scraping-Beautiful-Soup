# Projet de Web Scraping avec Beautiful Soup

Un outil Python versatile pour extraire des données de sites web en utilisant Beautiful Soup et Requests.


## Caractéristiques

- Interface simple et intuitive
- Extraction de données avec des sélecteurs CSS
- Export des données au format CSV et Excel
- Gestion des erreurs et des exceptions
- Exemples pratiques inclus
- Structure orientée objet facilement extensible


2. Installez les dépendances requises

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Utilisation

Pour lancer le script principal :

```bash
python web_scraping.py
```

Le programme vous présentera un menu interactif avec les exemples disponibles.

## Exemples inclus

### 1. Scraping d'un site d'actualités (Hacker News)

Extrait les derniers titres, liens et scores des publications de Hacker News.

```python
# Pour utiliser uniquement cette fonctionnalité
from web_scraper import WebScraper, scrape_news_example
scrape_news_example()
```

### 2. Scraping d'un site e-commerce (Books to Scrape)

Extrait les titres, prix et évaluations de livres de la catégorie Science.

```python
# Pour utiliser uniquement cette fonctionnalité
from web_scraper import WebScraper, scrape_ecommerce_example
scrape_ecommerce_example()
```

## Bonnes pratiques

- Respectez les conditions d'utilisation du site cible
- Consultez le fichier `robots.txt` du site
- Ajoutez des délais entre les requêtes (`time.sleep()`)
- Utilisez des en-têtes HTTP appropriés
- Ne surchargez pas les serveurs avec trop de requêtes

## Structure du projet

```
web-scraping-beautiful-soup/
│
├── web_scraping.py         # Script principal avec la classe WebScraper et les exemples
├── README.md              # Ce fichier
├── actualites.csv         # Fichier de sortie de l'exemple d'actualités
└── livres.xlsx            # Fichier de sortie de l'exemple e-commerce
```"# Web-Scraping-Beautiful-Soup" 
