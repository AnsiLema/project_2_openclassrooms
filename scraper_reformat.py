import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin

# URL de base du site
base_url = "https://books.toscrape.com/"


# Fonction pour obtenir le contenu HTML d'une page
def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


# Fonction pour extraire les URLs des catégories
def extract_category_urls(soup):
    category_urls = []
    category_section = soup.find("ul", class_="nav-list").find("ul")
    category_links = category_section.find_all("a")

    for link in category_links:
        category_url = urljoin(base_url, link['href'])
        category_urls.append(category_url)

    return category_urls


# Fonction pour extraire les URLs des livres d'une page de catégorie
def extract_book_urls(soup):
    book_elements = soup.find("ol", class_="row").find_all("h3")
    book_urls = []
    for book_element in book_elements:
        relative_url = book_element.find("a")["href"]
        full_url = urljoin("https://books.toscrape.com/catalogue/", relative_url.replace("../", ""))
        book_urls.append(full_url)
    return book_urls


# Fonction pour gérer la pagination et extraire les URLs de tous les livres d'une catégorie
def extract_all_books_in_category(category_url):
    all_book_urls = []
    next_page = category_url

    while next_page:
        soup = get_soup(next_page)
        all_book_urls.extend(extract_book_urls(soup))

        # Trouver le lien vers la page suivante
        next_button = soup.find("li", class_="next")
        if next_button:
            next_page = urljoin(category_url, next_button.find("a")["href"])
        else:
            next_page = None

    return all_book_urls


# Fonction pour télécharger les images des livres


# Fonction pour extraire les informations d'un livre
def extract_book_info(soup, url):
    upc = soup.find("th", string="UPC").find_next_sibling("td").string
    title = soup.find("h1").string
    price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string
    price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string
    number_available = soup.find("th", string="Availability").find_next_sibling("td").string
    unit_available = int(re.search(r"\d+", number_available).group())
    product_description = soup.find("meta", {"name": "description"})["content"].strip()
    category = soup.find("ul", {"class": "breadcrumb"}).find_all("li")[2].text.strip()
    star_number = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    review_rating = soup.find("p", {"class": "star-rating"})["class"][1]
    if review_rating in star_number:
        review_rating = star_number[review_rating]
    else:
        review_rating = 0
    image_url = soup.find("img")["src"]
    image_url = "http://books.toscrape.com" + image_url.replace("../..", "")

    return {
        "product_page_url": url,
        "universal_product_code (upc)": upc,
        "title": title,
        "price_including_tax": price_including_tax[1:],
        "price_excluding_tax": price_excluding_tax[1:],
        "number_available": unit_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url
    }


# Fonction pour extraire toutes les données d'une catégorie et les enregistrer dans un fichier CSV
def extract_category_in_csv(category_url, csv_filename):
    book_urls = extract_all_books_in_category(category_url)

    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "product_page_url",
            "universal_product_code (upc)",
            "title",
            "price_including_tax",
            "price_excluding_tax",
            "number_available",
            "product_description",
            "category",
            "review_rating",
            "image_url"
        ])
        writer.writeheader()
        for book_url in book_urls:
            soup = get_soup(book_url)
            book_info = extract_book_info(soup, book_url)
            writer.writerow(book_info)

    print(f"Les infos des livres de la catégorie ont été écrites dans le fichier {csv_filename}.")


# Extraire les URLs de toutes les catégories
soup = get_soup(base_url)
category_urls = extract_category_urls(soup)

# Scraper les données de chaque catégorie
for category_url in category_urls:
    category_name = category_url.split("/")[-2]
    csv_filename = f"{category_name}.csv"
    extract_category_in_csv(category_url, csv_filename)

print("Scraping terminé ! Les fichiers CSV ont été créés pour chaque catégorie.")






