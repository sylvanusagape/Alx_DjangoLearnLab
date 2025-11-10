from relationship_app.models import Author, Book, Library, Librarian


# Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian


# Example usage for Django shell testing
if __name__ == "__main__":
    print("Books by Author:", books_by_author("J.K. Rowling"))
    print("Books in Library:", books_in_library("Central Library"))
    print("Librarian for Library:", librarian_for_library("Central Library"))
