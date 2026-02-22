import sys
import requests

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt5.QtGui import QColor, QBrush

from book import Book
from library import Library


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 1000, 500)

        # Library object
        self.lib = Library()

        # ---------- INPUT FIELDS ----------
        QLabel("Title", self).move(30, 30)
        self.title = QLineEdit(self)
        self.title.setGeometry(30, 50, 250, 30)

        QLabel("Author", self).move(30, 90)
        self.author = QLineEdit(self)
        self.author.setGeometry(30, 110, 250, 30)

        QLabel("ISBN", self).move(30, 150)
        self.isbn = QLineEdit(self)
        self.isbn.setGeometry(30, 170, 250, 30)

        # ---------- SEARCH ----------
        QLabel("Search", self).move(350, 20)
        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(400, 20, 300, 25)
        self.search_input.textChanged.connect(self.search_books)  # Auto-search as typing

        self.clear_searchBtn = QPushButton("Clear", self)
        self.clear_searchBtn.setGeometry(710, 20, 60, 25)
        self.clear_searchBtn.clicked.connect(self.clear_search)

        # ---------- BUTTONS ----------
        self.addBtn = QPushButton("Add Book", self)
        self.addBtn.setGeometry(30, 220, 120, 35)

        self.updateBtn = QPushButton("Update Book", self)
        self.updateBtn.setGeometry(160, 220, 120, 35)

        self.deleteBtn = QPushButton("Delete Book", self)
        self.deleteBtn.setGeometry(30, 270, 250, 35)

        # ---------- QUOTE BUTTON ----------
        self.quoteBtn = QPushButton("Get Quote", self)
        self.quoteBtn.setGeometry(30, 320, 250, 35)  # Button for quotes
        self.quoteBtn.clicked.connect(self.show_quote)

        self.quoteLabel = QLabel("", self)
        self.quoteLabel.setGeometry(30, 360, 300, 100)  # Output area
        self.quoteLabel.setWordWrap(True)  # Multi-line support

        # ---------- BOOK TABLE ----------
        self.bookTable = QTableWidget(self)
        self.bookTable.setGeometry(350, 50, 600, 400)
        self.bookTable.setColumnCount(4)
        self.bookTable.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Availability"])
        self.bookTable.cellClicked.connect(self.load_selected_book)

        # ---------- CONNECTIONS ----------
        self.addBtn.clicked.connect(self.add_book)
        self.updateBtn.clicked.connect(self.update_book)
        self.deleteBtn.clicked.connect(self.delete_book)

    # ---------- FUNCTIONS ----------
    def refresh_list(self, books=None):
        """Refresh the table. If 'books' is provided, show only those books."""
        self.bookTable.setRowCount(0)
        if books is None:
            books = self.lib.books
        for book in books:
            row = self.bookTable.rowCount()
            self.bookTable.insertRow(row)
            self.bookTable.setItem(row, 0, QTableWidgetItem(book.title))
            self.bookTable.setItem(row, 1, QTableWidgetItem(book.author))
            self.bookTable.setItem(row, 2, QTableWidgetItem(book.isbn))
            status_item = QTableWidgetItem("Available" if book.available else "Lent Out")
            # Color availability
            if book.available:
                status_item.setForeground(QBrush(QColor("green")))
            else:
                status_item.setForeground(QBrush(QColor("red")))
            self.bookTable.setItem(row, 3, status_item)

    def add_book(self):
        if not self.title.text() or not self.author.text() or not self.isbn.text():
            QMessageBox.warning(self, "Error", "All fields are required")
            return
        b = Book(self.title.text(), self.author.text(), self.isbn.text())
        self.lib.add_book(b)
        self.refresh_list()
        QMessageBox.information(self, "Success", "Book Added")
        self.clear_inputs()

    def load_selected_book(self, row, column):
        self.title.setText(self.bookTable.item(row, 0).text())
        self.author.setText(self.bookTable.item(row, 1).text())
        self.isbn.setText(self.bookTable.item(row, 2).text())

    def update_book(self):
        isbn = self.isbn.text()
        for book in self.lib.books:
            if book.isbn == isbn:
                book.title = self.title.text()
                book.author = self.author.text()
                QMessageBox.information(self, "Updated", "Book Updated")
                self.refresh_list()
                self.clear_inputs()
                return
        QMessageBox.warning(self, "Error", "Book not found")

    def delete_book(self):
        isbn = self.isbn.text()
        self.lib.remove_book(isbn)
        self.refresh_list()
        QMessageBox.information(self, "Deleted", "Book Deleted")
        self.clear_inputs()

    def search_books(self):
        query = self.search_input.text().lower()
        filtered = [
            book for book in self.lib.books
            if query in book.title.lower() or query in book.author.lower() or query in book.isbn.lower()
        ]
        self.refresh_list(filtered)

    def show_quote(self):
        """Fetch a quote from RapidAPI and display it in the QLabel"""
        try:
            url = "https://quotes-by-api-ninjas.p.rapidapi.com/v1/quotes"
            headers = {
                "X-RapidAPI-Key": "ED06ECB13EMSH2BD06E7B56F4167P1F1B18JSN96879E269843",  # <-- apni key
                "X-RapidAPI-Host": "quotes-by-api-ninjas.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            quote_text = f"{data[0]['quote']}\n\n— {data[0]['author']}"
            self.quoteLabel.setText(quote_text)
        except Exception as e:
            self.quoteLabel.setText("Error fetching quote")
            print(e)

    def clear_search(self):
        self.search_input.clear()
        self.refresh_list()

    def clear_inputs(self):
        self.title.clear()
        self.author.clear()
        self.isbn.clear()


# ---------- RUN APP ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
