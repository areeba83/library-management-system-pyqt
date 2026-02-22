# This Book class book store basic info of book

class Book:
    def __init__(self, title, author, isbn):
        self.title = title      # book title
        self.author = author    # book author
        self.isbn = isbn        # ISBN for identification
        self.available = True   # check book available or not

    def __str__(self):
        return f"{self.title} by {self.author}"
