import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

# URL de la page produit à scraper
# product_page_url = "https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html"

# Envoyer une requête GET à la page produit
page = requests.get(url)
# response.raise_for_status()

# Analyser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(page.text, "html.parser")

# Extraire les informations demandées
def extract_book_info(soup, url):
    upc = soup.find("th", string='UPC').find_next_sibling("td").string
    title = soup.find("h1").string
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling('td').string
    price_including_tax_wo_symbol = price_including_tax.replace("Â£", "£")
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling('td').string
    price_excluding_tax_wo_symbol = price_excluding_tax.replace("Â£", "£")
    number_available = soup.find('th', string='Availability').find_next_sibling('td').string
    unit_available = int(re.search(r"\d+", number_available).group())
    product_description = soup.find('meta', {'name': 'description'})['content'].strip()
    category = soup.find('ul', {'class': 'breadcrumb'}).find_all('li')[2].text.strip()
    star_number = {
        "One": "1",
        "Two": "2",
        "Three": "3",
        "Four": "4",
        "Five": "5"
    }
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    if review_rating in star_number:
        review_rating = star_number[review_rating]
        print(review_rating)
    image_url = soup.find('img')['src']
    image_url = 'http://books.toscrape.com' + image_url.replace('../..', '')

    return {
        'product_page_url': url,
        'universal_product_code (upc)': upc,
        'title': title,
        'price_including_tax': price_including_tax_wo_symbol,
        'price_excluding_tax': price_excluding_tax_wo_symbol,
        'number_available': unit_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
        'image_url': image_url
    }

# Extraire les informations du livre
book_info = extract_book_info(soup, url)
print(book_info)

# # Écrire les informations dans un fichier CSV
csv_file = 'book_info.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=book_info.keys())
    writer.writeheader()
    writer.writerow(book_info)

print(f"Les informations du livre ont été écrites dans le fichier {csv_file}.")

# Extraction des données de toute une catégorie de livre

