from book_scraper import BookScraper
from book_url_scraper import BookUrlScraper
import csv
import os

from category_url_scraper import CategoryUrlScraper


def delete_csv_files(result_dir: str = 'result') -> None:
    """Delete all CSV files in the result directory"""
    if os.path.exists(result_dir):
        for filename in os.listdir(result_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(result_dir, filename)
                os.remove(filepath)
                print(f"CSV file has been deleted: {filepath}")


def save_to_csv(book_data, category: str, result_dir: str = 'result') -> None:
    """Save the scraped book data to a category-specific CSV file"""
    os.makedirs(result_dir, exist_ok=True)

    # Create a valid filename from the category name
    filename = f"{category.lower().replace(' ', '_')}_books.csv"
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
    # Delete existing CSV files
    delete_csv_files()

    category_url_scraper = CategoryUrlScraper("http://books.toscrape.com/")
    category_urls = category_url_scraper.scrape_urls()

    for category_url in category_urls:
        category_name = category_url.split('/')[-2].split('_')[0]
        book_url_scraper = BookUrlScraper("http://books.toscrape.com/")
        book_urls = book_url_scraper.scrape_urls(category_url)

        for url in book_urls:
            scraper = BookScraper("http://books.toscrape.com/")
            book_data = scraper.scrape_book(url)
            save_to_csv(book_data, category_name)


main()
