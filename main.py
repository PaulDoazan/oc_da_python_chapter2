from book_scraper import BookScraper
from book_url_scraper import BookUrlScraper
import csv
import os

from category_url_scraper import CategoryUrlScraper


def delete_csv(result_dir: str = 'result', filename: str = 'book_data.csv') -> None:
    """Delete the CSV file if it exists"""
    filepath = os.path.join(result_dir, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"CSV file has been deleted: {filepath}")


def save_to_csv(book_data, result_dir: str = 'result', filename: str = 'book_data.csv') -> None:
    """Save the scraped book data to a CSV file"""
    os.makedirs(result_dir, exist_ok=True)
    filepath = os.path.join(result_dir, filename)

    # Check if file exists to determine if we need to write headers
    file_exists = os.path.exists(filepath)

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=book_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(book_data)

    print(f"Data has been appended to {filepath}")


def main():
    delete_csv()

    category_url_scraper = CategoryUrlScraper("http://books.toscrape.com/")
    category_urls = category_url_scraper.scrape_urls()
    book_url_scraper = BookUrlScraper("http://books.toscrape.com/")
    book_urls = book_url_scraper.scrape_urls(
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

    for url in book_urls:
        scraper = BookScraper("http://books.toscrape.com/")
        book_data = scraper.scrape_book(url)
        save_to_csv(book_data)


main()
