from typing import Optional
from fastapi import FastAPI
from fastapi.datastructures import Default
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Not required at the time of creating", default=None
    )
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A New Book",
                "author": "Ajinath",
                "description": "Anew description of book",
                "rating": 5,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Ajinath Ghodake", "A very Nice Book!", 5),
    Book(2, "Be fast with FastAPI", "Ajinath Ghodake", "A Great Book!", 5),
    Book(3, "Master Endpoints", "Ajinath Ghodake", "A Awesome Book", 5),
    Book(4, "HP1", "Author 1", "Book Description", 4),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 2),
    Book(7, "HP4", "Author 4", "Book Description", 1),
    Book(8, "HP5", "Author 5", "Book Description", 0),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(new_book)
    return BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
