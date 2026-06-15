import json
import os
from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    available: bool

def save_books(books):
    with open("books.json", "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in books], f, ensure_ascii=False, indent=2)
def load_books():
    if os.path.exists("books.json"):
        with open("books.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Book(**item) for item in data]
    return []
def add_book(books):
    title = input("Enter book name: ")
    author = input("Enter author name: ")
    year = int(input("Entr year: "))

    new_id = max((b.id for b in books), default=0) + 1
    book = Book(new_id, title, author, year, True)
    books.append(book)

    print("Book added")
def show_books(books):
    if not books:
        print("Library is empty")
        return
    for book in books:
        status = "Available" if book.available else "Borrowed"
        print(
            f"ID: {book.id} | "
            f"{book.title} | "
            f"{book.author} | "
            f"{book.year} | "
            f"{status}"
        )
def search_book(books):
    search = input("Enter title to search: ")
    found = False
    for book in books:
        if search.lower() in book.title.lower():
            status = "Available" if book.available else "Borrowed"
            print(
                f"ID: {book.id} | "
                f"{book.title} | "
                f"{book.author} | "
                f"{book.year} | "
                f"{status}"
            )
            found = True
    if not found:
        print("No books found")
def borrow_book(books):
    book_id = int(input("Enter book ID: "))
    for book in books:
        if book.id == book_id:
            if book.available:
                book.available = False
                print("Book borrowed successfully")
            else:
                print("This book is already borrowed")
            return
    print("Book not found.")
def return_book(books):
    book_id = int(input("Enter book ID: "))
    for book in books:
        if book.id == book_id:
            book.available = True
            print("Book returned successfully")
            return
    print("Book not found")
def statistics(books):
    total = len(books)
    available = sum(1 for b in books if b.available)
    borrowed = total - available

    print(f"Total books: {total}")
    print(f"Available books: {available}")
    print(f"Borrowed books: {borrowed}")

books = load_books()
while True:
    print("\nLibrary Management System ")
    print("1. Add book")
    print("2. View all books")
    print("3. Search book by title")
    print("4. Borrow book")
    print("5. Return book")
    print("6. Statistics")
    print("7. Save data")
    print("8. Exit")

    choice = input("Choose an option: ")
    if choice == "1":
        add_book(books)
    elif choice == "2":
        show_books(books)
    elif choice == "3":
        search_book(books)
    elif choice == "4":
        borrow_book(books)
    elif choice == "5":
        return_book(books)
    elif choice == "6":
        statistics(books)
    elif choice == "7":
        save_books(books)
        print("Data saved successfully.")
    elif choice == "8":
        save_books(books)
        print("Program terminated.")
        break
    else:
        print("Invalid choice.")
