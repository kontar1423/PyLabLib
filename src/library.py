import random
from typing import Iterable

from src.collections import BookCollection, IndexDict
from src.models import Book


class Library:
    def __init__(self, books: Iterable[Book] | None = None) -> None:
        self.books = BookCollection()
        self.indexes = IndexDict()
        if books:
            for book in books:
                self.add_book(book)

    def add_book(self, book: Book) -> bool:
        added = self.books.add(book)
        if added:
            self.indexes.add(book)
        return added

    def remove_book(self, isbn: str) -> Book | None:
        removed = self.books.remove_by_isbn(isbn)
        if removed:
            self.indexes.remove(removed)
        return removed

    def refresh_indexes(self) -> None:
        self.indexes.rebuild(self.books)

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.indexes[isbn]

    def search_by_author(self, author: str) -> BookCollection:
        return BookCollection(self.indexes[("author", author)])

    def search_by_year(self, year: int) -> BookCollection:
        return BookCollection(self.indexes[("year", year)])

    def search_by_genre(self, genre: str) -> BookCollection:
        return BookCollection(book for book in self.books if book.genre == genre)

    def random_book(self, rng: random.Random) -> Book | None:
        if len(self.books) == 0:
            return None
        index = rng.randrange(len(self.books))
        return self.books[index]
