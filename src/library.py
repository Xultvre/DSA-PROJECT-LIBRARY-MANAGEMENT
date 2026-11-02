import json
import os
from src.skip_list import create_skip_list, insert, search, display as skip_display
from src.indexing import create_index, add_to_index, search_index

# File paths
BOOKS_FILE = "data/books.json"
BORROWED_FILE = "data/borrowed.json"

# JSON File Handlers
def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_books(books):
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)

def load_borrowed():
    if os.path.exists(BORROWED_FILE):
        with open(BORROWED_FILE, "r") as f:
            return json.load(f)
    return {}

def save_borrowed(borrowed):
    with open(BORROWED_FILE, "w") as f:
        json.dump(borrowed, f, indent=4)

# Initialize data structures
books = load_books()
skip_list = create_skip_list()
index = create_index()

for book_id_str, details in books.items():
    book_id = int(book_id_str)
    insert(skip_list, book_id, details)
    add_to_index(index, details["title"], book_id)
    add_to_index(index, details["author"], book_id)
    add_to_index(index, details["genre"], book_id)


# Admin: Add Book
def add_book():
    book_id = int(input("\nEnter Book ID: "))

    if str(book_id) in books:
        print("A book with this ID already exists!")
        existing = books[str(book_id)]
        print(f"{existing['title']} by {existing['author']} ({existing['genre']})")
        return

    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    genre = input("Enter Genre: ")

    books[str(book_id)] = {
        "title": title,
        "author": author,
        "genre": genre,
        "available": True
    }

    insert(skip_list, book_id, books[str(book_id)])
    add_to_index(index, title, book_id)
    add_to_index(index, author, book_id)
    add_to_index(index, genre, book_id)

    save_books(books)
    print("Book added successfully!")


# Admin: Remove Book
def remove_book():
    book_id = int(input("\nEnter Book ID to remove: "))
    if str(book_id) in books:
        del books[str(book_id)]
        save_books(books)
        print("Book removed successfully!")
    else:
        print("Book ID not found.")

def search_books(query):
    query = query.strip()
    book_ids = search_index(index, query)

    if book_ids:
        print("\n Books Found:")
        for book_id in book_ids:
            book = books.get(str(book_id))
            if book:
                status = "[Available]" if book["available"] else "[Borrowed]"
                print(f" {book_id} - {book['title']} by {book['author']} ({book['genre']}) {status}")
    else:
        print(" No books found.")

def list_all_books():
    books = load_books()

    if not books:
        print(" The library is currently empty.")
        return

    print("\n All Books in the Library:")
    for book_id, book in books.items():
        status = "[Available]" if book["available"] else "[Borrowed]"
        print(f" {book_id} - {book['title']} by {book['author']} ({book['genre']}) {status}")

def display_books_skip_order():
    print("\n Skip List Book Order (Level 0):")

    # Start at level 0
    node = skip_list["head"]["forward"][0]
    if not node:
        print(" No books in the skip list.")
        return

    while node:
        book_id = node["key"]
        book = books.get(str(book_id))
        if book:
            status = "[Available]" if book["available"] else "[Borrowed]"
            print(f"🔹 {book_id} - {book['title']} by {book['author']} ({book['genre']}) {status}")
        node = node["forward"][0]
    print("\n Debug - Skip List Structure:")
    skip_display(skip_list)

# User: Borrow Book
def borrow_book(username):
    book_id = int(input("\nEnter Book ID to borrow: "))
    book_key = str(book_id)

    borrowed = load_borrowed()
    book = books.get(book_key)

    if book and book["available"]:
        # Book is available
        books[book_key]["available"] = False
        borrowed[book_key] = username
        save_books(books)
        save_borrowed(borrowed)
        print(f"You {username} have borrowed {book['title']}")
    elif book and not book["available"]:
        borrower = borrowed.get(book_key, "someone else")
        print(f"Sorry, '{book['title']}' is already borrowed by {borrower}.")
    else:
        print("Book not found.")

# User: Return Book
def return_book(username):
    book_id = int(input("\nEnter Book ID to return: "))
    book_key = str(book_id)

    borrowed = load_borrowed()
    book = books.get(book_key)

    if book_key not in borrowed:
        print("This book wasn't borrowed.")
        return

    if borrowed[book_key] != username:
        print(f"You have not borrowed this book")
        return

    # Allow return
    books[book_key]["available"] = True
    del borrowed[book_key]
    save_books(books)
    save_borrowed(borrowed)
    print(f"Thank you, {username}, for returning '{book['title']}'")