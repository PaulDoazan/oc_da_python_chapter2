from urllib.parse import urljoin


def create_absolute_url(base_url: str, relative_url: str) -> str:
    """
    Creates an absolute URL from a base URL and a relative URL.

    Args:
        base_url (str): The base URL of the website
        relative_url (str): The relative URL path

    Returns:
        str: The absolute URL
    """
    cleaned_url = relative_url.replace("../", "")
    return urljoin(base_url, cleaned_url)
