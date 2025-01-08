import requests


def fetch_page(url: str):
    """Fetch the page content and create BeautifulSoup object"""
    response = requests.get(url)
    return response.content
