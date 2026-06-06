from models import init_db
from crud import add_author, add_book, add_member, add_borrowing
from datetime import date
import json

def seed_data():
    init_db()
    print("\nDatabase initialized.")
    with open("sample_data.json") as sample_data:
        data = json.load(sample_data)

    for author in data["authors"]:
        add_author(name=author["name"], bio=author["bio"])
    print("\nAuthors Seeded!")

    for book in data["books"]:
        add_book(title=book["title"], isbn=book["isbn"], year_published=book["year_published"], available_copies=book["available_copies"])
    print("\nBooks Seeded!")

    for member in data["members"]:
        add_member(name=member["name"], email=member["email"], membership_date= date.fromisoformat(member["membership_date"]))
    print("\nMembers Seeded!")

    for borrowing in data["borrowings"]:
        add_borrowing(book_id=borrowing["book_id"], member_id=borrowing["member_id"], checkout_date= date.fromisoformat(borrowing["checkout_date"]), return_date= date.fromisoformat(borrowing["return_date"]) if borrowing["return_date"] else None)
    print("\nBorrowings Seeded!")

    print("\nAll Data Seeding Complete!")

if __name__ == "__main__":
    seed_data()