import requests
from bs4 import BeautifulSoup
import csv
import os
from typing import Dict, Optional


class BookScraper:
    def __init__(self, base_url: str = "http://books.toscrape.com"):
        self.base_url = base_url
        self.soup: Optional[BeautifulSoup] = None
        self.book_data: Dict = {}

    def fetch_page(self, url: str) -> None:
        """Fetch the page content and create BeautifulSoup object"""
        response = requests.get(url)
        page = response.content
        self.soup = BeautifulSoup(page, "html.parser")

    def get_content_next_to_table_head(self, th_parameter: str) -> str:
        """Extract content next to a table header"""
        try:
            name_header = self.soup.find('th', string=th_parameter)
            return name_header.find_next_sibling('td').text if name_header else ''
        except AttributeError:
            return ''

    def get_product_description(self, parent_tag_type: str, child_tag_type: str, id_param: str):
        try:
            product_div = self.soup.find(parent_tag_type, id=id_param)
            if product_div:
                return product_div.find_next(child_tag_type)
            else:
                return ''
        except AttributeError:
            return ''

    def get_product_category(self, parent_tag_type: str, child_tag_type: str, class_param: str):
        try:
            category_ul = self.soup.find(parent_tag_type, class_=class_param)
            if category_ul:
                return category_ul.find_all(child_tag_type)[2].text
            else:
                return ''
        except AttributeError:
            return ''

    def get_image_url(self, parent_tag_type: str, child_tag_type: str, class_param: str):
        try:
            image_div = self.soup.find(parent_tag_type, class_=class_param)
            if image_div:
                return image_div.find(child_tag_type)['src']
            else:
                return ''
        except AttributeError:
            return ''

    def get_review_rating(self) -> str:
        """Extract the review rating"""
        try:
            star_div = self.soup.find('div', class_='star-rating')
            if star_div and star_div.get('class'):
                return star_div.get('class')[1]
            return ''
        except (AttributeError, IndexError):
            return ''

    def scrape_book(self, url: str) -> Dict:
        """Scrape all book data from a given URL"""
        self.fetch_page(url)

        self.book_data = {
            'Title': self.soup.find("h1").text,
            'Product Page URL': url,
            'Universal Product Code': self.get_content_next_to_table_head('UPC'),
            'Price Including Tax': self.get_content_next_to_table_head('Price (incl. tax)'),
            'Price Excluding Tax': self.get_content_next_to_table_head('Price (excl. tax)'),
            'Number Available': self.get_content_next_to_table_head('Availability'),
            'Product Description': self.get_product_description('div', 'p', 'product_description'),
            'Category': self.get_product_category('ul', 'li', 'breadcrumb'),
            'Review Rating': self.get_review_rating(),
            'Image URL': self.get_image_url('div', 'img', 'item active')
        }

        return self.book_data

    def save_to_csv(self, result_dir: str = 'result', filename: str = 'book_data.csv') -> None:
        """Save the scraped book data to a CSV file"""
        os.makedirs(result_dir, exist_ok=True)
        filepath = os.path.join(result_dir, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.book_data.keys())
            writer.writeheader()
            writer.writerow(self.book_data)

        print(f"Data has been written to {filepath}")
