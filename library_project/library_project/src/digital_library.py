from library import Library
from book import Book

class DigitalBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size  # filesize is in MB

class DigitalLibrary(Library):
    def add_ebook(self, title, author, isbn, download_size):
        ebook = DigitalBook(title, author, isbn, download_size)
        self.books.append(ebook)
