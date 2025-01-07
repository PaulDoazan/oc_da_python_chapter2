from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from typing import List, Optional


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
                cleaned_href = link["href"].replace("../", "")
                absolute_url = urljoin(self.base_url, f"catalogue/{cleaned_href}")
                self.books_urls.append(absolute_url)

        return self.books_urls
