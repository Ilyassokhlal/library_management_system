from models import init_db
from crud import add_author, add_book, add_member, checkout_a_book, list_all_books, list_all_members, search_books_by_author, search_books_by_title, list_member_borrowings, list_overdue_books, return_a_book, update_member_email, delete_book, delete_member
from datetime import date

def menu_add_book():
    """Prompt for book details and add to the database."""
    # nb = new book
    nb_title = input("\nPlease input the title of the new book: ")
    nb_isbn = input("\nPlease input the isbn of the new book: ")
    nb_year_published = int((input("\nPlease input the publication year of the new book: ")))
    nb_available_copies = int((input("\nPlease input the number of available copies of the new book: ")))
    add_book(title= nb_title, isbn= nb_isbn, year_published= nb_year_published, available_copies= nb_available_copies)

def menu_add_author():
    """Prompt for member details and add to the database."""
    # na = new author
    na_name = input("\nPlease input the name of the new author: ")
    na_bio = input("\nPlease input the bio of the new author (250 chars): ")
    add_author(name= na_name, bio= na_bio)

def menu_add_member():
    """Prompt for member details and add to the database."""
    # nm = new member
    nm_name = input("\nPlease input the name of the new member: ")
    nm_email = input("\nPlease input the email of the new member: ")
    nm_membership_date = date.today()
    add_member(name= nm_name, email= nm_email, membership_date= nm_membership_date)

def menu_search_books():
    """Prompt for book details and search for them in the database."""
    print("\nWould you like to search by title or author?")
    print("1. Search by title")
    print("2. Search by author")

    choice = input("Please enter your choice: ")

    if choice =="1":
        search_title = input("\nPlease enter the title: ")
        search_books_by_title(search_title)
    elif choice =="2":
        search_author = input("\nPlease enter the name of the author: ")
        search_books_by_author(search_author)
    else:
        print("Invalid choice. Please choose either 1 or 2.")

def menu_checkout_a_book():
    """Prompt for book details and add that borrowing."""
    list_all_books()
    checkout_book_id = int(input("\nPlease input the book id of the book you would like: "))
    list_all_members()
    checkout_member_id = int(input("\nPlease input the member id of the person checking out the book: "))
    checkout_a_book(book_id= checkout_book_id, member_id= checkout_member_id)
    

def menu_return_a_book():
    """Prompt for book details and updatte that borrowing."""
    list_all_books()
    return_book_id = int(input("\nPlease input the id of the book being returned: "))
    return_a_book(return_book_id)

def menu_view_member_borrowings():
    """Prompt for member details and return their borrowings from the database."""
    list_all_members()
    member_id = int(input("\nPlease input the id of the member whose borrowings you want to see: "))
    list_member_borrowings(member_id)

def menu_view_overdue_books():
    """Return overdue books from the database the database."""
    list_overdue_books()

def main():
    init_db()

    while True:
        print("\n=== Library Management System ===")
        print("1. Add a book")
        print("2. Add an author")
        print("3. Add a member")
        print("4. Search books")
        print("5. Check out a book")
        print("6. Return a book")
        print("7. View member's borrowings")
        print("8. View overdue books")
        print("9. Exit")

        choice = input("\nChoose an option (1-9): ").strip()

        if choice =="1":
            menu_add_book()
        elif choice =="2":
            menu_add_author()
        elif choice =="3":
            menu_add_member()
        elif choice =="4":
            menu_search_books()
        elif choice =="5":
            menu_checkout_a_book()
        elif choice =="6":
            menu_return_a_book()
        elif choice =="7":
            menu_view_member_borrowings()
        elif choice =="8":
            menu_view_overdue_books()
        elif choice =="9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")

if __name__ == "__main__":
    main()
