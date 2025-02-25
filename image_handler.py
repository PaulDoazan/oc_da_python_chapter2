import os
import requests
from urllib.parse import urljoin
import re


class ImageHandler:
    def __init__(self, base_url: str, result_dir: str = 'result'):
        self.base_url = base_url
        self.result_dir = result_dir

    def create_category_directories(self, category: str) -> tuple[str, str]:
        """
        Create category and images directories if they don't exist
        Returns tuple of (category_dir_path, images_dir_path)
        """
        category_dir = os.path.join(self.result_dir, category.lower().replace(' ', '_'))
        images_dir = os.path.join(category_dir, 'images')

        print(f"Creating directories: {category_dir} and {images_dir}")
        os.makedirs(category_dir, exist_ok=True)
        os.makedirs(images_dir, exist_ok=True)

        return category_dir, images_dir

    def download_image(self, image_url: str, save_path: str) -> None:
        """Download an image from the given URL and save it to the specified path"""
        try:
            print(f"Attempting to download image from: {image_url}")
            response = requests.get(image_url)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {save_path}")
        except Exception as e:
            print(f"Error downloading image from {image_url}: {str(e)}")

    def sanitize_filename(self, filename: str) -> str:
        # Split into name and extension
        name, ext = os.path.splitext(filename)
        # Remove all punctuation and special characters from name
        clean_name = re.sub(r'[^\w\s-]', '', name)
        # Replace multiple spaces/hyphens with single ones
        clean_name = re.sub(r'[-\s]+', '_', clean_name)
        # If name ends with hyphen or underscore, append 'x'
        if clean_name[-1] in '-_':
            clean_name += 'x'
        return clean_name + ext

    def process_book_image(self, book_data: dict, category: str) -> dict:
        """
        Process and download the book image, update book_data with local image path
        Returns updated book_data dictionary
        """
        if 'Image URL' not in book_data:
            print(f"No image URL found in book data for {book_data.get('title', 'unknown')}")
            return book_data

        # Create directories if they don't exist
        category_dir, images_dir = self.create_category_directories(category)

        # Ensure the image URL is absolute
        image_url = urljoin(self.base_url, book_data['Image URL'])
        print(f"Processing image URL: {image_url}")

        # Create a valid filename for the image
        title = book_data.get('Title', 'unknown')
        image_filename = f"{title.lower().replace(' ', '_')[:50]}.jpg"
        image_filename = self.sanitize_filename(image_filename)
        image_path = os.path.join(images_dir, image_filename)

        print(f"Saving image to: {image_path}")

        # Download the image
        self.download_image(image_url, image_path)

        # Add the local image path to the book data
        book_data['local_image_path'] = os.path.join('images', image_filename)

        return book_data
