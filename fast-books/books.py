from typing import Optional, Literal
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import random 
import os
import json


# *I want to create an API for an e-commerce book store where I can see all the books in my catalog.
# *I also would like to add new ones and things like that.

# List of paths:
# / = root path

# /list-books = shows me all the books I have in my catalog

# /book-by-index/{index} = if i give it a specific number, I can get that exact book and nothing else-
# I want this to take a number for example: /book-by-index/0

# /get-random-book = recommending random books to my customers

# /add-book = for adding books to my catalog. The data for this will be sent through a request body

# /get-book?id = if I have the id or unique identifier of a book, I might want the API to get that book directly.
# This will use a Query parameter 

app = FastAPI()

# TODO: Creating a data model (Book Model)
# In fastapi, to create a data model i need to create a class-
# that extends from the base model object (pydantic basemodel)
class Book(BaseModel):
    name: str
    price: float
    # this Literal will be so that the user can pick from fiction or non-fiction
    genre: Literal["fiction", "non-fiction"]
    # this is for string conversion and also converts it to a random id
    book_id: Optional[str] = uuid4().hex


# *Saving the books data in memory as a json file
BOOKS_FILE = "books.json"

# *Global Variable acting like fake database for the books
BOOK_DATABASE = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        # When I add my books I want it to save in this json
        BOOK_DATABASE = json.load(f)

# TODO: Create root/home path
@app.get("/")
async def home():
    return {"Message": "Welcome to my bookstore!"}

# TODO: Create list-books path
@app.get("/list-books")
async def list_books():
    return {"books": BOOK_DATABASE}

# TODO: Create book-by-index path
# I need to detect when an index is out of range and if the index is-
# out of range, I don't want the app to crash. I want to respond with a-
# error message. 
@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
    # For the body of the function i want it to return the book that is at the index given
    if index < 0 or index >= len(BOOK_DATABASE):
        # Fail
        raise HTTPException(404, f"Index {index} is out of range {len(BOOK_DATABASE)}.")
    else:
        return {"book": BOOK_DATABASE[index]}

# TODO: Create get-random-book path
@app.get("/get-random-book")
async def get_random_book():
    # this will pick a random element out of the BOOK_DATABASE
    return random.choice(BOOK_DATABASE)

# TODO: Create add-book path
@app.post("/add-book")
async def add_book(book: Book):
    # when I add a book i want to give it a new uuid, so i want to overwrite the id and give it a new one.
    book.book_id = uuid4().hex
    # allows the data to be converted into json
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        # When I add my books I want it to save in this json
        json.dump(BOOK_DATABASE, f)
    return {"Message": f"The book {book} was added.", "book_id":  book.book_id}

# TODO: Create get-book?id path (Request Body)
# *In fastapi and REST api's in general, there is a consept called request body.
# *If I send information to my post method like add-book-
# *aside from using a query parameter, I can also use a request body.

# *Which is basically a json object that is sent with the request.

# *Due to the request body being json object, means that my API can still be used-
# *across different paltforms.

# *Even though I am defining my book data structure in python, someone else can still use-
# *this API, aslong as they can build a similar data structure. Whether its in JS, C#, -
# *or whatever platform is communicating with this API

@app.get("/get-book")
async def get_book(book_id: str):
    # This is not a real database, its just a list. But if it was a real database then a string look-
    # up or a key look-up should be fairly quick. Because I dont care much for the backend at the moment-
    # I will brute force it and i will get every element and find the book with the id.
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return book
    
    raise HTTPException(404, f"Book not found: {book_id}")