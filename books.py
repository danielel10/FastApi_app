from typing import Optional

from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'title one', 'author': 'author one'},
    'book_2': {'title': 'title two', 'author': 'author two'},
    'book_3': {'title': 'title three', 'author': 'author three'},
    'book_4': {'title': 'title four', 'author': 'author four'},
    'book_5': {'title': 'title five', 'author': 'author five'}
}


class DirectionName(str, Enum):
    north = 'north'
    south = 'south'
    east = 'east'
    west = 'west'


@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.post("/")
async def create_book(book_title, book_author):
    curr_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > curr_book_id:
                curr_book_id = x

    BOOKS[f'book_{curr_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{curr_book_id + 1}']


@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_auth: str):
    book_info = {'title': book_title, 'author': book_auth}
    BOOKS[book_name] = book_info
    return book_info


@app.delete("/{book_name}")
async def del_book(book_name: str):
    del BOOKS[book_name]
    return f'{book_name} was deleted'


@app.get("/assignment/")
async def read_book_assignment(book_n: str):
    return BOOKS[book_n]
