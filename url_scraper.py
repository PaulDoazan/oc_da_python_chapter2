from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from typing import List, Optional

from utils.url_utils import create_absolute_url


class UrlScraper:
    def __init__(self, books_url: str):
        self.books_urls: List = []
        self.soup: Optional[BeautifulSoup] = None
        self.base_url = books_url

    def fetch_page(self, url: str) -> None:
        """Fetch the page content and create BeautifulSoup object"""
        response = requests.get(url)
        page = response.content
        self.soup = BeautifulSoup(page, "html.parser")

    def scrape_urls(self, url: str) -> List:
        self.fetch_page(url)
        product_pods = self.soup.find_all("article", class_="product_pod")

        for product in product_pods:
            link = product.find("a")
            if link and link.get("href"):
                self.books_urls.append(create_absolute_url(self.base_url, link["href"], "catalogue/"))

        return self.books_urls
