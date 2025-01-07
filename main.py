import requests
from bs4 import BeautifulSoup
import csv
import os


def getContentNextToTableHead(thParameter):
    try:
        name_header = soup.find('th', string=thParameter)
        return name_header.find_next_sibling('td').text if name_header else ''
    except AttributeError:
        return ''


def getReviewRating(soup):
    try:
        star_div = soup.find('div', class_='star-rating')
        if star_div and star_div.get('class'):
            return star_div.get('class')[1]
        return ''
    except (AttributeError, IndexError):
        return ''


url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
response = requests.get(url)
page = response.content
soup = BeautifulSoup(page, "html.parser")

book_data = {
    'Title': soup.find("h1").text,
    'Product Page URL': url,
    'Universal Product Code': getContentNextToTableHead('UPC'),
    'Price Including Tax': getContentNextToTableHead('Price (incl. tax)'),
    'Price Excluding Tax': getContentNextToTableHead('Price (excl. tax)'),
    'Number Available': getContentNextToTableHead('Availability'),
    'Product Description': soup.find('div', id='product_description').find_next('p').text,
    'Category': getContentNextToTableHead('Product Type'),
    'Review Rating': getReviewRating(soup),
    'Image URL': soup.find('div', class_='item active').find('img')['src']
}

# Write to CSV
# Create result directory if it doesn't exist
result_dir = 'result'
os.makedirs(result_dir, exist_ok=True)

filename = os.path.join(result_dir, 'book_data.csv')

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=book_data.keys())
    writer.writeheader()  # Write the headers
    writer.writerow(book_data)  # Write the data

print(f"Data has been written to {filename}")
