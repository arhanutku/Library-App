import os
import sys
import gradio as gr

# Online Library Application
# File: app.py
# Purpose: Library database that loads books, lists authors, and uses binary search to find books by author.
# Date: 2025-12-03
# Creator: Arhan B. Utku

BOOKS_FILE = "books.csv"
DEFAULT_PORT = int(os.environ.get("PORT", 7860))

"""
The Book class contains a books title and its author
"""
class Book:
    
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"{self.title} by {self.author}"

"""
This function reads the books file line-by-line and returns Book objects
@param filePath Path to the books data file.
@return list of Book objects loaded.
"""
def loadBooks(filePath):
    books = []
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            for rawLine in file:
                line = rawLine.strip()
                if not line:
                    continue  # skip empty rows
                row = [dataField.strip() for dataField in line.split(",") if dataField.strip() != "" or dataField == ""]
                if len(row) != 2:
                    print(f"Skipping malformed row: {rawLine!r}")
                    continue
                title, author = row
                books.append(Book(title, author))
    except FileNotFoundError:
        print(f"Error: File '{filePath}' not found.")
    return books

"""
This helper performs a lower-bound binary search for the first book whose
author is greater than or equal to the target.
@param books Sorted list of Book objects.
@param targetAuthor author string to search for.
@return index of the first matching position.
"""
def lowerBound(books, targetAuthor):
    low, high = 0, len(books)
    while low < high:
        mid = (low + high) // 2
        if books[mid].author.lower() < targetAuthor:
            low = mid + 1
        else:
            high = mid
    return low

"""
This helper performs an upper-bound binary search for the first book whose
author is strictly greater than the target.
@param books Sorted list of Book objects.
@param targetAuthor author string to search for.
@return index just past the last matching position.
"""
def upperBound(books, targetAuthor):
    low, high = 0, len(books)
    while low < high:
        mid = (low + high) // 2
        if books[mid].author.lower() <= targetAuthor:
            low = mid + 1
        else:
            high = mid
    return low

"""
This function finds all books with a given author using binary search
over a sorted list.
@param sortedBooks List of Book objects sorted by author.
@param authorName Author string as stored in the list.
@return list slice of matching Book objects.
"""
def searchBooksByAuthor(sortedBooks, authorName):
    target = authorName.lower()
    start = lowerBound(sortedBooks, target)
    end = upperBound(sortedBooks, target)
    return sortedBooks[start:end]

"""
This function sorts the provided books by author using merge sort.
@param books List of Book objects to be sorted.
@return new list of Book objects sorted by author.
"""
def mergeSortBooksByAuthor(books):
    if len(books) <= 1:
        return books.copy()

    sortedBooks = books.copy()
    mergeWidth = 1
    while mergeWidth < len(sortedBooks):
        mergedLevel = []
        for index in range(0, len(sortedBooks), mergeWidth * 2):
            leftHalf = sortedBooks[index:index + mergeWidth]
            rightHalf = sortedBooks[index + mergeWidth:index + (mergeWidth * 2)]
            mergedLevel.extend(merge(leftHalf, rightHalf))
        sortedBooks = mergedLevel
        mergeWidth *= 2
    return sortedBooks

"""
This helper merges two sorted lists of Book objects into a single list
ordered by author.
@param left Sorted list of Book objects.
@param right Sorted list of Book objects.
@return merged, sorted list of Book objects.
"""
def merge(left, right):
    sortedBooks = []
    leftIndex = 0
    rightIndex = 0

    while leftIndex < len(left) and rightIndex < len(right):
        if left[leftIndex].author.lower() <= right[rightIndex].author.lower():
            sortedBooks.append(left[leftIndex])
            leftIndex += 1
        else:
            sortedBooks.append(right[rightIndex])
            rightIndex += 1

    sortedBooks.extend(left[leftIndex:])
    sortedBooks.extend(right[rightIndex:])
    return sortedBooks

# Build a author list while preserving the first seen casing/order
def buildSortedAuthors(sortedBooks):
    authors = []
    seen = set()
    for book in sortedBooks:
        normalizedAuthor = book.author.lower()
        if normalizedAuthor not in seen:
            authors.append(book.author)
            seen.add(normalizedAuthor)
    return authors

# This helper loads the books file, sorts by author, and creates the author list.
def initLibrary(filePath=BOOKS_FILE):
    books = loadBooks(filePath)
    sortedBooks = mergeSortBooksByAuthor(books)
    sortedAuthors = buildSortedAuthors(sortedBooks)
    return sortedBooks, sortedAuthors

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

"""
This is the main function that loads the list of books from a text file and sorts them by author.
"""
def main():
    books = loadBooks(BOOKS_FILE)

    if not books:
        return

    sortedBooks = mergeSortBooksByAuthor(books)
    authors = sorted({book.author for book in books}, key=str.lower)
    print("\nAuthors in database:")
    for author in authors:
        print(author)

    authorName = input("\nEnter author name to search: ")
    foundBooks = searchBooksByAuthor(sortedBooks, authorName)
    if foundBooks:
        count = len(foundBooks)
        print(f"\n{count} book{'s' if count != 1 else ''} by author '{authorName}':")
        for book in foundBooks:
            print(book)
    else:
        print("\nNo books found by that author.")

def buildDemo():
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

    return demo

SORTEDBOOKS, SORTEDAUTHORS = initLibrary(BOOKS_FILE)
demo = buildDemo()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        main()
    else:
        demo.launch(
            server_name="0.0.0.0",
            server_port=DEFAULT_PORT,
            show_error=True,
        )