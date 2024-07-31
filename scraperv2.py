import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://books.toscrape.com/catalogue/do-androids-dream-of-electric-sheep-blade-runner-1_149/index.html"
page = requests.get(url)
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
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    review_rating = soup.find('p', {'class': 'star-rating'})['class'][1]
    if review_rating in star_number:
        review_rating = star_number[review_rating]
    else:
        review_rating = 0
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


#Extraction de tout les livres d'une catégorie
base_url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
page = requests.get(base_url)
soup = BeautifulSoup(page.text, "html.parser")

#Extraire les URL de chaque livre d'une categorie
def extract_book_url(soup, base_url):
    book_elements = soup.find("ol", class_="row").find_all("h3")
    book_url = []
    for book_element in book_elements:
        complement_url = book_element.find("a")["href"]
        #ajout du début de l'URL pour avoir l'URL du livre
        full_url = "https://books.toscrape.com/catalogue/" + complement_url.replace("../", "")
        book_url.append(full_url)
    return book_url











