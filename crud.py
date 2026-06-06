from datetime import date, timedelta
from sqlalchemy.orm import Session
from models import engine, Author, Book, Member, Borrowing
from sqlalchemy import select


# CRUD QUERIES: CREATE


# Adding a new book
def add_book(title: str, isbn: str, year_published: int, available_copies: int) -> Book:
    with Session(engine) as session:
        new_book = Book(title = title, isbn = isbn, year_published = year_published, available_copies = available_copies)
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        return new_book


# Adding a new member    
def add_member(name: str, email: str, membership_date: date) -> Member:
    with Session(engine) as session:
        new_member = Member(name = name, email = email, membership_date = membership_date)
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        return new_member
    
# Adding a new author    
def add_author(name: str, bio: str = None) -> Author:
    with Session(engine) as session:
        new_author = Author(name = name, bio = bio)
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        return new_author
    

# Adding book checkout    
def checkout_a_book(book_id: int, member_id: int) -> Borrowing:
    with Session(engine) as session:
        new_borrowing_book = session.get(Book, book_id)

        if new_borrowing_book.available_copies > 0:
            new_borrowing = Borrowing(book_id = book_id, member_id = member_id, checkout_date = date.today())
            new_borrowing_book.available_copies -=1
            session.add(new_borrowing)
            session.commit()
            session.refresh(new_borrowing)
            return new_borrowing

        else:
            raise ValueError ("There are currently no available copies for this book!")


# Adding a new borrowing    
def add_borrowing(book_id: int, member_id: int, checkout_date: date, return_date: date = None) -> Borrowing:
    with Session(engine) as session:
        new_borrowing = Borrowing(book_id = book_id, member_id = member_id, checkout_date = checkout_date, return_date = return_date)
        session.add(new_borrowing)
        session.commit()
        session.refresh(new_borrowing)
        return new_borrowing


# CRUD QUERIES: READ


# listing all books
def list_all_books():
    with Session(engine) as session:
        print("\n=== All Books! ===")
        books = session.execute(select(Book)).scalars().all()
        for book in books:
            print(f"ID: {book.id} | Book: {book.title} | Year published: {book.year_published} | Available copies: {book.available_copies} | isbn: {book.isbn}")

# listing all members
def list_all_members():
    with Session(engine) as session:
        print("\n=== All Members! ===")
        members = session.execute(select(Member)).scalars().all()
        for member in members:
            print(f"ID: {member.id} | Member: {member.name} | email: {member.email} | Membership date: {member.membership_date}")

# searching for books by title
def search_books_by_title(title):
    with Session(engine) as session:
        print("\n=== Books Found by Title ===")
        books = session.execute(select(Book).where(Book.title.ilike(f"%{title}%"))).scalars().all()
        if not books:
            raise ValueError(f"No books found with this title: {title}")
        for book in books:
            print(f"Book: {book.title} | Year published: {book.year_published} | Available copies: {book.available_copies} | isbn: {book.isbn}")


# searching for books by author
def search_books_by_author(author):
    with Session(engine) as session:
        print("\n=== Books Found by Author ===")
        authors = session.execute(select(Author).where(Author.name.ilike(f"%{author}%"))).scalars().all()
        if not authors:
            raise ValueError(f"No books found from this author: {author}")
        for found_author in authors:
            for book in found_author.books:
                print(f"Book: {book.title} | Year published: {book.year_published} | Available copies: {book.available_copies} | isbn: {book.isbn}")


# listing a member's borrowings
def list_member_borrowings(member_id):
    with Session(engine) as session:
        print("\n=== Borrowings by Member ===")
        found_member = session.execute(select(Borrowing).where(Borrowing.return_date == None, Borrowing.member_id == member_id)).scalars().all()
        for book in found_member:
            print(f"Book: {book.book.title} | Checkout Date: {book.checkout_date}")



# listing books that are overdue by 14 days
def list_overdue_books():
    with Session(engine) as session:
        print("\n=== Overdue Books (Checked-out more than 14 days ago) ===")
        fourteen_days_ago = date.today() - timedelta(days=14)
        books = session.execute(select(Borrowing).where(Borrowing.return_date == None, Borrowing.checkout_date < fourteen_days_ago)).scalars().all()
        for book in books:
            print(f"Book: {book.book.title} | Checkout Date: {book.checkout_date}")



# CRUD QUERIES: UPDATE


# Returning a book (adding a return date)
def return_a_book(book_id: int) -> Book:
    with Session(engine) as session:
        new_return_book = session.execute(select(Borrowing).where(Borrowing.return_date == None, Borrowing.book_id == book_id)).scalars().first()
        book = session.get(Book, book_id)
        book.available_copies +=1
        new_return_book.return_date = date.today()
        session.add(new_return_book)
        session.commit()
        session.refresh(new_return_book)
        return new_return_book

 
# Updating a member's email
def update_member_email(member_id: int, new_email: str) -> Member:
    with Session(engine) as session:
        member = session.get(Member, member_id)
        member.email = new_email
        session.add(member)
        session.commit()
        session.refresh(member)
        return member


# CRUD QUERIES: DELETE


# Book Deletion (if not borrowed now)
def delete_book(book_id):
    """Deleting the book if not borrowed"""
    with Session(engine) as session:
        book = session.get(Book, book_id)

        active_borrowing = session.execute(select(Borrowing).where(Borrowing.book_id == book_id, Borrowing.return_date == None)).scalars().first()

        if active_borrowing:
                print(f"Book cuurently borrowed! Please return all books before deletion!")
                return
    
        title = book.title
        session.delete(book)
        session.commit()
        print(f"Deleted Book: {title}")



# Member Deletion (if no active borrowings)
def delete_member(member_id):
    """Deleting the member if he has no books borrowed"""
    with Session(engine) as session:
        member = session.get(Member, member_id)

        active_borrowings = session.execute(select(Borrowing).where(Borrowing.member_id == member_id, Borrowing.return_date == None)).scalars().all()

        if active_borrowings:
                print(f"The member currently has unreturned books. Please return all books before deletion.")
                return
    
        name = member.name
        session.delete(member)
        session.commit()
        print(f"Deleted Member: {name}")