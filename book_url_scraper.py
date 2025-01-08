from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

from utils.fetch_utils import fetch_page
from utils.url_utils import create_absolute_url


class BookUrlScraper:
    def __init__(self, base_url: str):
        self.books_urls: List = []
        self.soup: Optional[BeautifulSoup] = None
        self.base_url: str = base_url

    def fetch_page(self, url: str) -> None:
        """Fetch the page content and create BeautifulSoup object"""
        response = requests.get(url)
        page = response.content
        self.soup = BeautifulSoup(page, "html.parser")

    def get_next_page_url(self, current_url: str) -> Optional[str]:
        """Get the URL of the next page if it exists"""
        next_button = self.soup.find("li", class_="next")
        if next_button and next_button.find("a"):
            next_url = next_button.find("a")["href"]
            return urljoin(current_url, next_url)
        return None

    def scrape_urls(self, url: str) -> List:
        current_url = url

        while current_url:
            self.soup = BeautifulSoup(fetch_page(current_url), "html.parser")

            product_pods = self.soup.find_all("article", class_="product_pod")

            for product in product_pods:
                link = product.find("a")
                if link and link.get("href"):
                    self.books_urls.append(create_absolute_url(self.base_url, link["href"], "catalogue/"))

            current_url = self.get_next_page_url(current_url)

        return self.books_urls
