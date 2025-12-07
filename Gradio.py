# Program Info
# Purpose: Gradio interface for the library database to list authors and search books by author.
# Date: 25-12-03
# Creator: Arhan B. Utku

import gradio as gr

# Import core library logic
from app import (
    loadBooks,
    mergeSortBooksByAuthor,
    searchBooksByAuthor
)

BOOKS_FILE = "requirements.txt"
SORTEDBOOKS = []
SORTEDAUTHORS = []

# This helper loads the books file, sorts by author, and creates the author list.
def initLibrary():
    books = loadBooks(BOOKS_FILE)
    sortedBooks = mergeSortBooksByAuthor(books)
    sortedAuthors = buildSortedAuthors(sortedBooks)
    return sortedBooks, sortedAuthors

# Build a de-duplicated author list while preserving the first-seen casing/order
def buildSortedAuthors(sortedBooks):
    authors = []
    seen = set()
    for book in sortedBooks:
        normalizedAuthor = book.author.lower()
        if normalizedAuthor not in seen:
            authors.append(book.author)
            seen.add(normalizedAuthor)
    return authors

"""
This function returns the authors as a newline-separated string for display.
@return string of authors or a friendly fallback message.
"""
def listAuthors():
    return "\n".join(SORTEDAUTHORS) if SORTEDAUTHORS else "No authors found."

"""
This function searches books by author using binary search on the sorted list.
@param author_name Name selected from the dropdown.
@return tuple of (header text, details text) for the UI.
"""
def search(authorName):
    if not authorName:
        return "No author selected.", ""

    matches = searchBooksByAuthor(SORTEDBOOKS, authorName)
    count = len(matches)
    header = f"{count} book{'s' if count != 1 else ''} by author '{authorName}':"
    details = "\n".join(str(book) for book in matches) if matches else "No books found."
    return header, details

SORTEDBOOKS, SORTEDAUTHORS = initLibrary()

demo = gr.Blocks(title="Library Author Search")

with demo:
    gr.Markdown("## Library Author Search\nList authors and find their books.")

    with gr.Row():
        authorsBox = gr.TextArea(
            label="Authors in database",
            value=listAuthors(),
            interactive=False,
            lines=10,
        )

    with gr.Row():
        authorDropdown = gr.Dropdown(
            choices=SORTEDAUTHORS,
            label="Select an author",
            value=None,
        )

    searchButton = gr.Button("Search")
    headerOut = gr.Markdown(label="Search summary")
    resultsOut = gr.Textbox(label="Books by author", lines=10)

    # Wire interactions
    searchButton.click(search, inputs=authorDropdown, outputs=[headerOut, resultsOut])

if __name__ == "__main__":
    SORTEDBOOKS, SORTEDAUTHORS = initLibrary()
    # Launches the Gradio UI
    demo.launch()