from __future__ import annotations

import random

from src.constants import DEFAULT_BOOK_DATA, DEFAULT_SEED, DEFAULT_STEPS
from src.library import Library
from src.models import Book


class LibraryAction:
    name: str = "action"

    def run(self, library: Library, rng: random.Random) -> str:
        raise NotImplementedError


class AddBookAction(LibraryAction):
    name = "add_book"

    def __init__(self, candidates: list[Book]) -> None:
        self._candidates = candidates

    def run(self, library: Library, rng: random.Random) -> str:
        sample = rng.choice(self._candidates)
        isbn = generate_isbn(library, rng)
        book = Book(
            title=sample.title,
            author=sample.author,
            year=sample.year,
            genre=sample.genre,
            isbn=isbn,
        )
        added = library.add_book(book)
        if added:
            return f"Добавили книгу {book}"
            return f"Не получилось добавить {book.isbn}"


class RemoveBookAction(LibraryAction):
    name = "remove_book"

    def run(self, library: Library, rng: random.Random) -> str:
        removed = library.books.pop_random(rng)
        if not removed:
            return "Удалять нечего"
        library.indexes.remove(removed)
        return f"Удалили книгу {removed.isbn}"


class SearchByAuthorAction(LibraryAction):
    name = "search_author"

    def __init__(self, authors: list[str]) -> None:
        self._authors = authors

    def run(self, library: Library, rng: random.Random) -> str:
        author = rng.choice(self._authors)
        found = library.search_by_author(author)
        return f"Ищем по автору {author}: {len(found)} шт."


class SearchByGenreAction(LibraryAction):
    name = "search_genre"

    def __init__(self, genres: list[str]) -> None:
        self._genres = genres

    def run(self, library: Library, rng: random.Random) -> str:
        genre = rng.choice(self._genres)
        found = library.search_by_genre(genre)
        return f"Ищем по жанру {genre}: {len(found)} шт."


class SearchByYearAction(LibraryAction):
    name = "search_year"

    def __init__(self, years: list[int]) -> None:
        self._years = years

    def run(self, library: Library, rng: random.Random) -> str:
        year = int(rng.choice(self._years))
        found = library.search_by_year(year)
        return f"Ищем по году {year}: {len(found)} шт."


class RefreshIndexesAction(LibraryAction):
    name = "refresh_indexes"

    def run(self, library: Library, rng: random.Random) -> str:
        library.refresh_indexes()
        return "Пересчитали индексы"


class MissingBookAction(LibraryAction):
    name = "missing_book"

    def run(self, library: Library, rng: random.Random) -> str:
        isbn = f"ISBN-{rng.randint(90000, 99999)}"
        book = library.get_by_isbn(isbn)
        if book:
            return f"Случайно нашли книгу {book}"
        return f"Пробуем найти {isbn}: такой книги нет"


def make_base_books() -> list[Book]:
    books: list[Book] = []
    for raw_book in DEFAULT_BOOK_DATA:
        books.append(
            Book(
                title=str(raw_book["title"]),
                author=str(raw_book["author"]),
                year=int(raw_book["year"]),
                genre=str(raw_book["genre"]),
                isbn=str(raw_book["isbn"]),
            )
        )
    return books


def generate_isbn(library: Library, rng: random.Random) -> str:
    while True:
        candidate = f"ISBN-{rng.randint(10000, 99999)}"
        if library.get_by_isbn(candidate) is None:
            return candidate


def run_simulation(steps: int = DEFAULT_STEPS, seed: int | None = DEFAULT_SEED) -> None:
    rng = random.Random(seed)
    library = Library(make_base_books())
    actions: list[LibraryAction] = [
        AddBookAction(make_base_books()),
        RemoveBookAction(),
        SearchByAuthorAction([book.author for book in library.books]),
        SearchByGenreAction([book.genre for book in library.books]),
        SearchByYearAction([book.year for book in library.books]),
        RefreshIndexesAction(),
        MissingBookAction(),
    ]

    for step in range(1, steps + 1):
        action = rng.choice(actions)
        message = action.run(library, rng)
        print(f"[{step:02d}] {message}")
