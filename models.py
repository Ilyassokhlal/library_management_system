from sqlalchemy import create_engine, String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, relationship, Session
)
from typing import Optional
from datetime import date

engine = create_engine("sqlite:///library.db", echo=False)

class Base(DeclarativeBase):
    pass

# Association table for (Book <-> Author)
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("author_id", Integer, ForeignKey("authors.id"))
)

# --- Models ---

class Author(Base):
    __tablename__= "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(250))

    # authors <-> books
    books: Mapped[list["Book"]] = relationship(
        secondary=book_authors, back_populates="authors"
    )

    def __repr__(self):
        return f"Author(name='{self.name}')"



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(unique=True, nullable=False)
    year_published: Mapped[int] = mapped_column(nullable=False)
    available_copies: Mapped[int] = mapped_column(nullable=False)

    # books <-> authors
    authors: Mapped[list["Author"]] = relationship(
        secondary=book_authors, back_populates="books"
    )

    # Relationship to borrowings
    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="book")

    def __repr__(self):
        return f"Book(title='{self.title}')"



class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    membership_date: Mapped[date] = mapped_column(nullable=False)

    # member -> borrowing
    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="member")

    def __repr__(self):
        return f"Member(name='{self.name}')"



class Borrowing(Base):
    __tablename__ = "borrowings"

    id: Mapped[int] = mapped_column(primary_key=True)
    checkout_date: Mapped[date] = mapped_column(nullable=False)
    return_date: Mapped[Optional[date]] = mapped_column()
    
    # Foreign key to books
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    # Foreign key to members
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    # Relationship to book
    book: Mapped["Book"] = relationship(back_populates="borrowings")
    # Relationship to member
    member: Mapped["Member"] = relationship(back_populates="borrowings")

    def __repr__(self):
        return f"Borrowing(checkout:'{self.checkout_date}', return: '{self.return_date}')"


# Create all the tables
def init_db():
    Base.metadata.create_all(engine)
    print("\nTables Created!")
