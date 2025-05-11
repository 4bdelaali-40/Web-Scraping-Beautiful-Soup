import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
import os

class WebScraper:
    def __init__(self, url, headers=None):
        """
        Initialise le web scraper avec l'URL cible et les en-têtes optionnels
        
        Args:
            url (str): L'URL à scraper
            headers (dict, optional): En-têtes HTTP à utiliser pour les requêtes
        """
        self.url = url
        self.headers = headers if headers else {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def fetch_page(self):
        """
        Récupère le contenu HTML de la page
        
        Returns:
            str: Le contenu HTML de la page
        """
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()  # Vérifie si la requête a réussi
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération de la page: {e}")
            return None
    
    def parse_html(self, html):
        """
        Parse le HTML avec Beautiful Soup
        
        Args:
            html (str): Le contenu HTML à parser
        
        Returns:
            BeautifulSoup: Un objet BeautifulSoup parsé
        """
        if html:
            return BeautifulSoup(html, 'html.parser')
        return None
    
    def extract_data(self, soup, selector, attribute=None):
        """
        Extrait des données en utilisant un sélecteur CSS
        
        Args:
            soup (BeautifulSoup): L'objet BeautifulSoup parsé
            selector (str): Le sélecteur CSS pour trouver les éléments
            attribute (str, optional): L'attribut à extraire (si None, récupère le texte)
        
        Returns:
            list: Liste des données extraites
        """
        elements = soup.select(selector)
        
        if attribute:
            return [element.get(attribute) for element in elements if element.get(attribute)]
        else:
            return [element.get_text(strip=True) for element in elements]
    
    def save_to_csv(self, data, filename):
        """
        Sauvegarde les données dans un fichier CSV
        
        Args:
            data (list): Liste de dictionnaires contenant les données
            filename (str): Nom du fichier CSV
        """
        if not data:
            print("Aucune donnée à sauvegarder")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Données sauvegardées dans {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")
    
    def save_to_excel(self, data, filename):
        """
        Sauvegarde les données dans un fichier Excel
        
        Args:
            data (list): Liste de dictionnaires contenant les données
            filename (str): Nom du fichier Excel
        """
        if not data:
            print("Aucune donnée à sauvegarder")
            return
        
        try:
            df = pd.DataFrame(data)
            df.to_excel(filename, index=False)
            print(f"Données sauvegardées dans {filename}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des données: {e}")


# Exemple d'utilisation - Scraping d'un site d'actualités
def scrape_news_example():
    """
    Exemple de scraping d'actualités
    """
    url = "https://news.ycombinator.com/"  # Hacker News comme exemple
    scraper = WebScraper(url)
    
    # Récupération et parsing de la page
    html = scraper.fetch_page()
    soup = scraper.parse_html(html)
    
    if not soup:
        print("Impossible de parser la page")
        return
    
    # Extraction des titres et des liens
    titles = scraper.extract_data(soup, ".titleline > a")
    links = scraper.extract_data(soup, ".titleline > a", "href")
    scores = scraper.extract_data(soup, ".score")
    
    # Création d'une liste de dictionnaires
    news_data = []
    for i in range(min(len(titles), len(links))):
        score = scores[i] if i < len(scores) else "Inconnu"
        news_data.append({
            "titre": titles[i],
            "lien": links[i],
            "score": score
        })
    
    # Sauvegarde des données
    scraper.save_to_csv(news_data, "actualites.csv")
    
    # Affichage des résultats
    print(f"\nRésultats ({len(news_data)} actualités récupérées):")
    for i, news in enumerate(news_data[:5], 1):  # Affiche les 5 premiers résultats
        print(f"{i}. {news['titre']} - {news['score']}")


# Exemple d'utilisation - Scraping d'un site e-commerce
def scrape_ecommerce_example():
    """
    Exemple de scraping d'un site e-commerce
    """
    url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    scraper = WebScraper(url)
    
    html = scraper.fetch_page()
    soup = scraper.parse_html(html)
    
    if not soup:
        print("Impossible de parser la page")
        return
    
    # Extraction des données des livres
    titles = scraper.extract_data(soup, ".product_pod h3 a", "title")
    prices = scraper.extract_data(soup, ".product_pod .price_color")
    ratings = scraper.extract_data(soup, ".product_pod .star-rating", "class")
    
    # Traitement des données des ratings (convertir "star-rating Three" en "3")
    processed_ratings = []
    for rating_class in ratings:
        if isinstance(rating_class, list):
            rating_class = rating_class[1]  # Prendre le deuxième élément de la liste
        rating_value = rating_class.split()[-1] if rating_class else "Inconnu"
        processed_ratings.append(rating_value)
    
    # Création d'une liste de dictionnaires
    books_data = []
    for i in range(min(len(titles), len(prices), len(processed_ratings))):
        books_data.append({
            "titre": titles[i],
            "prix": prices[i],
            "évaluation": processed_ratings[i]
        })
    
    # Sauvegarde des données
    scraper.save_to_excel(books_data, "livres.xlsx")
    
    # Affichage des résultats
    print(f"\nRésultats ({len(books_data)} livres récupérés):")
    for i, book in enumerate(books_data[:5], 1):  # Affiche les 5 premiers résultats
        print(f"{i}. {book['titre']} - {book['prix']} - {book['évaluation']}")


# Point d'entrée principal
if __name__ == "__main__":
    print("=== Démonstration de Web Scraping avec Beautiful Soup ===\n")
    
    while True:
        print("\nChoisissez un exemple à exécuter:")
        print("1. Scraping d'un site d'actualités (Hacker News)")
        print("2. Scraping d'un site e-commerce (Books to Scrape)")
        print("3. Quitter")
        
        choice = input("\nVotre choix (1-3): ")
        
        if choice == "1":
            scrape_news_example()
        elif choice == "2":
            scrape_ecommerce_example()
        elif choice == "3":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")