from typing import Optional
from bs4 import BeautifulSoup

from utils.fetch_utils import fetch_page


class CategoryUrlScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.soup: Optional[BeautifulSoup] = None

    def scrape_urls(self):
        self.soup = BeautifulSoup(fetch_page(self.base_url), "html.parser")
