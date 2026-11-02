import os
from src.auth import signup, login, remove_user
from src.library import (
    add_book, remove_book,
    search_books, borrow_book, return_book, list_all_books,
    display_books_skip_order
)
from src.recent_searches import create_recent_searches, add_recent_search, get_recent_searches

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# User Portal
def user_portal(username):
    recent_searches = create_recent_searches(capacity=10)
    while True:
        clear_screen()
        print(f"\n USER PORTAL - Welcome, {username}!")
        print("1 Search Books")
        print("2 Borrow Book")
        print("3 Return Book")
        print("4 Logout")
        print("5 Recent searches")
        print("6 View all books")

        choice = input("\nSelect an option: ")

        if choice == "1":
            query = input("\nEnter Book Title, Author, or Genre: ")
            add_recent_search(recent_searches, query)
            search_books(query)
        elif choice == "2":
            borrow_book(username)
        elif choice == "3":
            return_book(username)
        elif choice == "4":
            print(f"\n Goodbye, {username}!")
            break
        elif choice == "5":
            print("\n📜 Your Recent Searches:")
            for term in get_recent_searches(recent_searches):
                print(f"{term}")
        elif choice == "6":
            list_all_books()
        else:
            print("Invalid choice.")

        input("\nPress Enter to continue...")

# Admin Portal
def admin_portal(username):
    recent_searches = create_recent_searches(capacity=10)
    while True:
        clear_screen()
        print(f"\n ADMIN PORTAL - Welcome, {username}!")
        print("1 Add Book")
        print("2 Remove Book")
        print("3 Search Books")
        print("4 Logout")
        print("5 Remove User")
        print("6 Recent Searches")
        print("7 View all books")
        print("8 View Books (Skip List Order)")

        choice = input("\nSelect an option: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            query = input("\nEnter Book Title, Author, or Genre: ")
            add_recent_search(recent_searches, query)
            search_books(query)
        elif choice == "4":
            print(f"\nGoodbye, Admin {username}!")
            break
        elif choice == "5":
            target = input("Enter the username to remove: ").strip()
            remove_user(target, username)
        elif choice == "6":
            print("\n Your Recent Searches:")
            for term in get_recent_searches(recent_searches):
                print(f"{term}")
        elif choice == "7":
            list_all_books()
        elif choice == "8":
            display_books_skip_order()
        else:
            print("Invalid choice.")

        input("\nPress Enter to continue...")




# Main Function
def main():
    clear_screen()
    print("WELCOME TO THE LIBRARY SYSTEM")

    while True:
        print("\n Login or Signup to continue")
        choice = input("Do you want to Signup (S) or Login (L)? ").strip().lower()

        if choice == "s" :
            result = signup()
        elif choice == "l":
            result = login()
        else:
            print("Invalid Operation")
            return 
        if result:
            username, role = result
            if role == "admin":
                admin_portal(username)
            else:
                user_portal(username)
            break  # Exit after logout

if __name__ == "__main__":
    main()
