from book_scraper import BookScraper


def main():
    # Example usage
    book_url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    scraper = BookScraper()
    scraper.scrape_book(book_url)
    scraper.save_to_csv()


main()
