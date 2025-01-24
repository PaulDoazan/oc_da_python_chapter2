import requests


def fetch_page(url: str):
    """Fetch the page content to create afterward BeautifulSoup object"""
    response = requests.get(url)
    return response.content
