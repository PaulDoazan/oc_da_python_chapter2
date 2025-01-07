from book_scraper import BookScraper
from url_scraper import UrlScraper


def main():
    url_scraper = UrlScraper("http://books.toscrape.com/catalogue")
    book_urls = url_scraper.scrape_urls(
        "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html")

    # book_url = "http://books.toscrape.com/catalogue/sharp-objects_997/index.html"

    for url in book_urls:
        scraper = BookScraper()
        scraper.scrape_book(url)
        scraper.save_to_csv()


main()
