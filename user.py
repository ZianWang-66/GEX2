## This module contains the user interface for the library system. 
# It allows users to search for books, borrow books, and return books.

## Import the necessary functions from the admin module. 
# Replace "function_name1" with the actual function names you want to import.



from admin import (
    find_book,
    load_library,
    save_library,
)



## Search books by category.
## This function should return book IDs that match the given category.
def books_in_category(
    books,
    category
):

    target_category = category.strip().lower()
    matching_books = []

    for book_id, book_info in books.items():
        if book_info['category'].lower() == target_category:
            matching_books.append(book_id)
    return matching_books

    


## Search books by full or partial title.
## This function should return book IDs that match the given title or part of the title.
def search_by_title(
    books,
    search_text
):
    search = search_text.strip().lower()
    matching_books = []
    for book_id, book_info in books.items():
        if search in book_info['title'].lower():
            matching_books.append(book_id)
    return matching_books
    


## Create logic to let users borrow books.
## The function should check if the book is available or on loan, or if the borrower name is provided.
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not available, then return "NOT_AVAILABLE"
## If the book is successfully borrowed, then return "OK"
def borrow_book(
    books,
    loans,
    search_text,
    borrower
):
    if not borrower.strip():
        return 'EMPTY_NAME'

    book_id = find_book(books, search_text)
    if book_id is None:
        return 'BOOK_NOT_FOUND'

    if not books[book_id]['available']:
        return 'NOT_AVAILABLE'

    books[book_id]['available'] = False
    loans.append({"book_id" : book_id, "borrower" : borrower})
    return "OK"

    


## Create logic to let users return books.
## The function should check if the book is on loan, or if the borrower name is provided
## If the book is not found, then return "BOOK_NOT_FOUND"
## If the borrower name is empty, then return "EMPTY_NAME"
## If the book is not on loan, then return "NOT_ON_LOAN"
## If the book is successfully returned, then return "OK"

def return_book(
    books,
    loans,
    book_title,
    borrower
):
    if not borrower.strip():
        return 'EMPTY_NAME'

    book_id = find_book(books, book_title)
    if book_id is None:
        return 'BOOK_NOT_FOUND'

    loan_found = None
    for loan in loans:
        if loan['book_id'] == book_id and loan['borrower'] == borrower:
            loan_found = loan
            break

    if loan_found is None:
        return "NOT_ON_LOAN"

    books[book_id]["available"] =True
    loans.remove(loan_found)
    return "OK"


    



## The main function that runs the user interface for the library system.
## The function must first load the library data from a JSON file, then display a menu for the user to select options.
## The options include searching for books by title or category, borrowing a book, returning a book, and exiting the program.
## When the user selects an option, the corresponding function is called to perform the action.
## The program continues to display the menu until the user chooses to exit, at which point the library data is saved back to the JSON file.
## The main function should also handle invalid selections by displaying an error message and prompting the user to select again.
def main():
    data = load_library("library.json")
    books = data["books"]
    loans = data["loans"]

    while True:
        print()
        print("LIBRARY USER SYSTEM")
        print("=" * 40)
        print("1. Search books by category")
        print("2. Search books by title")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        
        choice = input("Please select an option: ").strip()

        if choice == "1":
            category = input("Enter book category: ")
            results = books_in_category(books, category)
            if results:
                print(f"Found books: {', '.join(results)}")
            else:
                print("No books found in this category.")
        
        elif choice == "2":
            title_query = input("Enter title or part of title: ")
            results = search_by_title(books, title_query)
            if results:
                print(f"Found books: {', '.join(results)}")
            else:
                print("No books found matching your search.")
        
        elif choice == "3":
            book_query = input("Enter book ID/title/author to borrow: ")
            borrower_name = input("Enter your name: ")
            result = borrow_book(books, loans, book_query, borrower_name)
            if result == "OK":
                print("Success! Book borrowed.")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "NOT_AVAILABLE":
                print("Error: Book is currently not available.")
        
        elif choice == "4":
            book_query = input("Enter book ID/title/author to return: ")
            borrower_name = input("Enter your name: ")
            result = return_book(books, loans, book_query, borrower_name)
            if result == "OK":
                print("Success! Book returned.")
            elif result == "BOOK_NOT_FOUND":
                print("Error: Book not found.")
            elif result == "EMPTY_NAME":
                print("Error: Borrower name cannot be empty.")
            elif result == "NOT_ON_LOAN":
                print("Error: This book is not on loan to you.")
        
        elif choice == "5":
            save_library(data, "library.json")
            print("Library data saved. Goodbye!")
            break
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
