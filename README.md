# Library Author Search

Small library helper that loads `books.txt`, sorts books by author with an iterative merge sort, and lets you list or search authors via Gradio.

## Files
- `app.py`: Core logic for loading books, merge-sorting by author, and binary search lookup.
- `Gradio.py`: UI wrapper that loads data once, builds a de-duplicated author list, and wires the search UI.
- `books.txt`: Comma-separated book data per line (`title,author`).

## Decomposition
- Parse file lines into `Book` objects (`title: str`, `author: str`).
- Iterative merge sort on the book list, comparing `author.lower()`.
- Build a de-duplicated author list in first-seen order.
- Binary search (lower/upper bounds) on sorted books to locate an author slice.
- Present results via CLI or Gradio UI.

## Pattern Recognition
- Merge sort repeatedly pairs adjacent runs of width `w`, compares leading authors, and appends the smaller until one side is exhausted.
- Binary search adjusts `low/high` by comparing the target author to the midpoint author, shrinking the search space logarithmically.

## Abstraction
- Shown: distinct author list, count of matches, formatted book strings (`"Title by Author"`).
- Hidden: file parsing internals, iterative merging steps, and bound calculations during binary search.

## Algorithm Design (Input → Processing → Output)
- Input types: `books.txt` lines as `str`, parsed into list[`Book`]; user-selected/entered author `str` (dropdown or CLI input).
- Processing: parse → iterative merge sort by `author.lower()` → build distinct author list → binary search range for chosen author.
- Output: count header plus matched books as strings (CLI print or Gradio text/markdown). GUI displays authors in a text area and dropdown; Search button triggers the lookup.

## Running
- CLI: `python app.py` → prints authors, prompts for an author, then prints matches.
- Gradio: `python Gradio.py` → opens the web UI (launch URL printed in console).

## Data Format
- Each line: `Title,Author`
- Example:
  ```
  The Great Gatsby,F. Scott Fitzgerald
  Hamlet,William Shakespeare
  ```