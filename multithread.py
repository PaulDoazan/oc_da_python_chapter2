from book_scraper import BookScraper
from book_url_scraper import BookUrlScraper
from image_handler import ImageHandler
from category_url_scraper import CategoryUrlScraper
import csv
import os
import shutil
import concurrent.futures
from typing import List, Dict
import threading


class ThreadSafeWriter:
    """Thread-safe CSV writer class"""

    def __init__(self):
        self.lock = threading.Lock()

    def save_to_csv(self, book_data: dict, category: str, result_dir: str = 'result') -> None:
        """Thread-safe method to save book data to CSV"""
        with self.lock:
            category_dir = os.path.join(result_dir, category.lower().replace(' ', '_'))
            os.makedirs(category_dir, exist_ok=True)
            filename = "books.csv"
            filepath = os.path.join(category_dir, filename)

            file_exists = os.path.exists(filepath)
            with open(filepath, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=book_data.keys())
                if not file_exists:
                    writer.writeheader()
                writer.writerow(book_data)


def delete_results_directories(result_dir: str = 'result') -> None:
    """Delete the entire result directory and its contents"""
    if os.path.exists(result_dir):
        try:
            shutil.rmtree(result_dir)
            print(f"Results directory has been deleted")
        except Exception as e:
            print(f"Error deleting results directory: {str(e)}")
    os.makedirs(result_dir)
    print(f"Created empty results directory: {result_dir}")


def process_book(args: tuple) -> Dict:
    """Process a single book URL"""
    url, base_url, category_name, image_loader = args
    scraper = BookScraper(base_url)
    try:
        book_data = scraper.scrape_book(url)
        book_data = image_loader.process_book_image(book_data, category_name)
        return book_data
    except Exception as e:
        print(f"Error processing book {url}: {str(e)}")
        return None


def process_category(args: tuple) -> List[str]:
    """Process a single category URL and return all book URLs"""
    category_url, base_url = args
    book_url_scraper = BookUrlScraper(base_url)
    try:
        return book_url_scraper.scrape_urls(category_url)
    except Exception as e:
        print(f"Error processing category {category_url}: {str(e)}")
        return []


def main():
    base_url = "http://books.toscrape.com/"
    max_workers = 20  # Adjust this based on your system capabilities and website limitations

    # Initialize shared resources
    image_loader = ImageHandler(base_url)
    csv_writer = ThreadSafeWriter()

    # Delete existing results directory
    delete_results_directories()

    # Get category URLs
    category_url_scraper = CategoryUrlScraper(base_url)
    category_urls = category_url_scraper.scrape_urls()

    # Process categories in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create arguments for each category
        category_args = [(url, base_url) for url in category_urls]

        # Process categories and collect all book URLs
        category_results = list(executor.map(process_category, category_args))

        # Flatten the list of book URLs and pair with their categories
        book_tasks = []
        for category_url, book_urls in zip(category_urls, category_results):
            category_name = category_url.split('/')[-2].split('_')[0]
            book_tasks.extend([(url, base_url, category_name, image_loader) for url in book_urls])

        # Process books in parallel
        for book_data in executor.map(process_book, book_tasks):
            if book_data:
                category_name = book_data.get('category', 'unknown')
                csv_writer.save_to_csv(book_data, category_name)


if __name__ == "__main__":
    main()
