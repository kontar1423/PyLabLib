from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    year: int
    genre: str
    isbn: str

    def __repr__(self) -> str:
        return f"{self.title} ({self.year}) / {self.author} / {self.isbn}"
