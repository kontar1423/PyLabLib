from __future__ import annotations

import random
from typing import Iterable, Iterator

from src.models import Book


class BookCollection:
    def __init__(self, books: Iterable[Book] | None = None) -> None:
        self._books: list[Book] = list(books) if books else []

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)

    def __len__(self) -> int:
        return len(self._books)

    def __getitem__(self, index: int | slice) -> Book | "BookCollection":
        if isinstance(index, slice):
            return BookCollection(self._books[index])
        return self._books[index]

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Book):
            return any(book.isbn == item.isbn for book in self._books)
        if isinstance(item, str):
            return any(book.isbn == item for book in self._books)
        return False

    def add(self, book: Book) -> bool:
        if book in self or book.isbn in self:
            return False
        self._books.append(book)
        return True

    def remove_by_isbn(self, isbn: str) -> Book | None:
        for index, book in enumerate(self._books):
            if book.isbn == isbn:
                return self._books.pop(index)
        return None

    def pop_random(self, rng: random.Random) -> Book | None:
        if not self._books:
            return None
        index = rng.randrange(len(self._books))
        return self._books.pop(index)


class IndexDict:
    def __init__(self) -> None:
        self._by_isbn: dict[str, Book] = {}
        self._by_author: dict[str, list[Book]] = {}
        self._by_year: dict[int, list[Book]] = {}

    def __iter__(self) -> Iterator[str]:
        return iter(self._by_isbn)

    def __len__(self) -> int:
        return len(self._by_isbn)

    def __getitem__(self, key: str | tuple[str, str | int]) -> Book | list[Book] | None:
        if isinstance(key, tuple) and len(key) == 2:
            field, value = key
            if field == "author":
                return list(self._by_author.get(str(value), []))
            if field == "year":
                try:
                    year_value = int(value)
                except (TypeError, ValueError):
                    return []
            return list(self._by_year.get(year_value, []))
        return self._by_isbn.get(str(key))

    def add(self, book: Book) -> None:
        self._by_isbn[book.isbn] = book
        self._by_author.setdefault(book.author, []).append(book)
        self._by_year.setdefault(book.year, []).append(book)

    def remove(self, book: Book) -> None:
        self._by_isbn.pop(book.isbn, None)
        if book.author in self._by_author:
            self._by_author[book.author] = [
                stored for stored in self._by_author[book.author] if stored.isbn != book.isbn
            ]
            if not self._by_author[book.author]:
                self._by_author.pop(book.author, None)
        if book.year in self._by_year:
            self._by_year[book.year] = [
                stored for stored in self._by_year[book.year] if stored.isbn != book.isbn
            ]
            if not self._by_year[book.year]:
                self._by_year.pop(book.year, None)

    def rebuild(self, books: Iterable[Book]) -> None:
        self._by_isbn.clear()
        self._by_author.clear()
        self._by_year.clear()
        for book in books:
            self.add(book)
