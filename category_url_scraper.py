from typing import Optional, List
from bs4 import BeautifulSoup

from utils.fetch_utils import fetch_page
from utils.url_utils import create_absolute_url


class CategoryUrlScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.soup: Optional[BeautifulSoup] = None

    def scrape_urls(self):
        self.soup = BeautifulSoup(fetch_page(self.base_url), "html.parser")
        a_tags = self.soup.select('ul.nav-list > li > ul > li > a[href]')

        urls: List = []

        for a_tag in a_tags:
            href = create_absolute_url(self.base_url, a_tag.get('href'))
            urls.append(href)
            
        return urls
