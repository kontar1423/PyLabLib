# Лабораторная работа №4 — «Библиотека»

Вариант 1 «Библиотека». Свои коллекции, индексы, библиотека и случайные события.

## Что есть
- `src/models.py` — книга `Book` с нормальным `__repr__`.
- `src/collections.py` — `BookCollection` (список со срезами и `in`) и `IndexDict` (индекс по ISBN/автору/году).
- `src/library.py` — `Library` с добавлением/удалением и поиском по автору, году, жанру.
- `src/simulation.py` — набор событий и `run_simulation(steps, seed)` для лога в консоль.
- `src/constants.py` — стартовые книги и дефолты.
- `src/main.py` — спрашивает шаги и seed, запускает симуляцию.
- `tests/test_library.py` — простые проверки коллекций, индексов и повторяемости.

## Как запустить
```bash
python3 -m src.main
```
Можно просто жать Enter, чтобы взять значения по умолчанию.

## Как проверить тесты
```bash
python3 -m pytest
```

## Структура
```
.
├── src/        # исходники
├── tests/      # pytest-тесты
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```
