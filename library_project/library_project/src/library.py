from exceptions import BookNotAvailableError

class Library:
    def __init__(self):
        self.books = []  # store all books 

    def add_book(self, book):
        self.books.append(book)  # add new book 

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]  
        # Remove the book from the list whose ISBN matches the given ISBN.

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if not book.available:
                    raise BookNotAvailableError("Book already lent!")
                book.available = False
                return book
        raise BookNotAvailableError("Book not found!")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.available = True

    def __iter__(self):
        # The iterator will return only the available books
        for b in self.books:
            if b.available:
                yield b

    def books_by_author(self, author_name):
        # The generator will yield books of a specific author.
        for b in self.books:
            if b.author == author_name:
                yield b
