from src.collections import BookCollection
from src.library import Library
from src.models import Book
from src.simulation import run_simulation


def test_book_collection_behaves_like_list():
    books = [
        Book("Учебник питона", "Студент", 2024, "учеба", "ISBN-1"),
        Book("Конспекты", "Студент", 2024, "учеба", "ISBN-2"),
    ]
    collection = BookCollection(books)

    assert len(collection) == 2
    assert [book.isbn for book in collection] == ["ISBN-1", "ISBN-2"]
    assert collection[0].title == "Учебник питона"

    sliced = collection[:1]
    assert isinstance(sliced, BookCollection)
    assert len(sliced) == 1
    assert sliced[0].isbn == "ISBN-1"
    assert "ISBN-2" in collection


def test_indexes_follow_changes():
    lib = Library()
    first = Book("Сборник", "Автор", 2020, "сборник", "ISBN-10")
    lib.add_book(first)

    assert lib.get_by_isbn(first.isbn) is first
    by_author = lib.search_by_author("Автор")
    assert isinstance(by_author, BookCollection)
    assert len(by_author) == 1

    lib.remove_book(first.isbn)
    assert lib.get_by_isbn(first.isbn) is None
    assert len(lib.search_by_author("Автор")) == 0


def test_search_by_genre_uses_collection():
    lib = Library(
        [
            Book("Рассказ", "Писатель", 1999, "рассказ", "ISBN-20"),
            Book("Роман", "Писатель", 2001, "роман", "ISBN-21"),
        ]
    )

    found = lib.search_by_genre("роман")
    assert isinstance(found, BookCollection)
    assert len(found) == 1
    assert found[0].isbn == "ISBN-21"


def test_simulation_reproducible(capsys):
    run_simulation(steps=5, seed=7)
    first = capsys.readouterr().out

    run_simulation(steps=5, seed=7)
    second = capsys.readouterr().out

    assert first == second
    assert "[01]" in first
