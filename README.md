# Library Author Search

A library database that loads `requirements.txt`, sorts books by author with a merge sort, and lets you search authors using Gradio.

## Files
- `app.py`: Core logic for loading books, merge sorting by author, and binary search.
- `Gradio.py`: GUI file that loads data once, builds a duplicated author list, and creates the search UI.
- `requirements.txt`: Comma separated book data per line (`title,author`).

## Decomposition
- Parse file lines into `Book` objects (`title: str`, `author: str`).
- Merge sort on the book list, comparing `author.lower()`.
- Build a author list
- Binary search (lower/upper bounds) on sorted books to locate an author.
- Present results in the Gradio GUI.

## Pattern Recognition
- Merge sort repeatedly pairs adjacent runs of width `w`, compares leading authors, and appends the smaller until one side is finished.
- Binary search adjusts `low/high` by comparing the target author to the midpoint author.

## Abstraction
- Shown: distinct author list, count of matches, formatted book strings (`"Title by Author"`).
- Hidden: file parsing internals, iterative merging steps, and bound calculations during binary search.

## Algorithm Design (Input → Processing → Output)
- Input types: `requirements.txt` lines as `str`, parsed into list[`Book`]; user selected author `str`.
- Processing: parse → iterative merge sort by `author.lower()` → build distinct author list → binary search range for chosen author.
- Output: count header and matched books as strings. GUI displays authors in a text area and dropdown. Search button triggers the lookup.

## Running
- Program: `python app.py` → prints authors, prompts for an author, then prints matches.
- Gradio: `python Gradio.py` → opens the GUI.

## Flowchart
![Library App Flowchart](flowchart.png)

## Data Format
- Each line: `Title,Author`
- Example:
  ```
  The Great Gatsby,F. Scott Fitzgerald
  Hamlet,William Shakespeare
  ```