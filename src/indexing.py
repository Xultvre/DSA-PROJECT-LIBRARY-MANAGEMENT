from collections import defaultdict

# Initialize Index
def create_index():
    return defaultdict(list)

# Add a book to the index
def add_to_index(index, key, book_id):
    index[key].append(book_id)

# Search books by attribute (title, author, genre)
def search_index(index, key):
    return index.get(key, [])
