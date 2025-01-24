from book_scraper import BookScraper
from book_url_scraper import BookUrlScraper
from image_handler import ImageHandler
import csv
import os
from category_url_scraper import CategoryUrlScraper
import time


def delete_results_directories(result_dir: str = 'result') -> None:
    """Delete all files and subdirectories in result directory one by one"""
    if os.path.exists(result_dir):
        for root, dirs, files in os.walk(result_dir, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {str(e)}")
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    print(f"Error deleting directory {dir_path}: {str(e)}")
        try:
            os.rmdir(result_dir)
        except Exception as e:
            print(f"Error deleting root directory: {str(e)}")

    os.makedirs(result_dir, exist_ok=True)
    print(f"Created empty results directory: {result_dir}")


def save_to_csv(book_data: dict, category: str, result_dir: str = 'result') -> None:
    """Save the scraped book data to a category-specific CSV file"""
    category_dir = os.path.join(result_dir, category.lower().replace(' ', '_'))
    os.makedirs(category_dir, exist_ok=True)

    filename = "books.csv"
    filepath = os.path.join(category_dir, filename)

    # Check if file exists to determine if we need to write headers
    file_exists = os.path.exists(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=book_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(book_data)
    print(f"Data has been appended to {filepath}")


def main():
    # It will be used to calculate time needed for all requests
    start_time = time.time()

    base_url = "http://books.toscrape.com/"

    # Initialize image loader
    image_loader = ImageHandler(base_url)

    # Delete existing results directory
    delete_results_directories()

    category_url_scraper = CategoryUrlScraper(base_url)
    category_urls = category_url_scraper.scrape_urls()

    for category_url in category_urls:
        category_name = category_url.split('/')[-2].split('_')[0]
        book_url_scraper = BookUrlScraper(base_url)
        book_urls = book_url_scraper.scrape_urls(category_url)

        for url in book_urls:
            scraper = BookScraper(base_url)
            book_data = scraper.scrape_book(url)

            # Process and download the book image
            book_data = image_loader.process_book_image(book_data, category_name)

            # Save book data to CSV
            save_to_csv(book_data, category_name)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
