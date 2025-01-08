from book_scraper import BookScraper
from url_scraper import UrlScraper
import csv
import os


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

    url_scraper = UrlScraper("http://books.toscrape.com/")
    book_urls = url_scraper.scrape_urls(
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

    # book_url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"

    for url in book_urls:
        scraper = BookScraper("http://books.toscrape.com/")
        book_data = scraper.scrape_book(url)
        save_to_csv(book_data)


main()
