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
import time


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
    os.makedirs(result_dir, exist_ok=True)
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
    start_time = time.time()
    base_url = "http://books.toscrape.com/"
    max_workers = 20

    image_loader = ImageHandler(base_url)
    csv_writer = ThreadSafeWriter()
    delete_results_directories()

    category_url_scraper = CategoryUrlScraper(base_url)
    category_urls = category_url_scraper.scrape_urls()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        category_args = []
        for url in category_urls:
            category_args.append((url, base_url))

        # Runs process_category() on each tuple in parallel, returns list of results: [books_from_url1, books_from_url2]
        category_results = list(executor.map(process_category, category_args))

        book_tasks = []
        for i in range(len(category_urls)):
            category_url = category_urls[i]
            book_urls = category_results[i]
            category_name = category_url.split('/')[-2].split('_')[0]

            for url in book_urls:
                book_tasks.append((url, base_url, category_name, image_loader))

        # executor.map() starts parallel processing tasks:
        # - Takes each item from book_tasks list (containing tuples of URL, base_url, category, image_loader)
        # - Passes each tuple to process_book() function
        # - Thread pool executes these operations concurrently (multiple books processed simultaneously)
        # - Returns iterator of results that yields each book's data as processing completes
        # - Results maintain same order as input book_tasks list
        results = executor.map(process_book, book_tasks)
        for book_data in results:
            if book_data:
                category_name = book_data.get('category', 'unknown')
                csv_writer.save_to_csv(book_data, category_name)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
