import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID

from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __int__(self, books_to_return):
        self.book_to_return = books_to_return


app = FastAPI()

BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_execption_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"{exception.book_to_return}"}
    )


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "12312",
                "title": "test",
                "author": "test auth",
                "description": "test desc",
                "rating": 75
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100,
                                       min_length=1)


@app.post("/books/login")
async def book_login(username: str = Form(), password: str = Form()):
    return {"username": username, "pass": password}

@app.get("/header")


@app.get("/")
async def read_all_books():
    return BOOKS


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):

def create_books_no_api():
    book_1 = Book(id=uuid.uuid4().hex,
                  title="title 1",
                  author="author 1",
                  description="none",
                  rating=2)
