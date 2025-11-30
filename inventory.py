import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(filename="library.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


class LibraryInventory:
    def __init__(self, file_path="books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_data()

    # ---------------- FILE PERSISTENCE ---------------- #

    def load_data(self):
        try:
            if not self.file_path.exists():
                logging.info("JSON file not found. Creating a new empty catalog.")
                self.save_data()
                return

            with open(self.file_path, "r") as f:
                data = json.load(f)

            self.books = [Book(**item) for item in data]

        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading file: {e}")
            self.books = []
            self.save_data()

    def save_data(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except IOError as e:
            logging.error(f"Error saving file: {e}")

    # ---------------- BOOK OPERATIONS ---------------- #

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")
        self.save_data()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books
🖥️ Task 4 — CLI Application (main.p