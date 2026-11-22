from fastapi import FastAPI, Path, Depends, APIRouter, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

books = {
    1: {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    2: {"title": "1984", "author": "George Orwell"},
    3: {"title": "Animal Farm", "author": "George Orwell"},
}


#“This is a FastAPI route decorator. 
# It registers the function directly below it to handle HTTP GET requests to /book
@app.get("/books")
def get_books(author: str | None = None ): # = None makes it optional
    if author:
        return [book for book in books.values() if book["author"] == author] 
    
    return books


@app.get("/books/{book_id}") #/books is the URL path. More precisely, the HTTP method and path together identify the operation:
def get_author_id(book_id: int):
    if book_id not in books.keys():
        raise HTTPException(status_code = 404, detail = "Book not found")

    return books[book_id]

@app.get("/search") #Putting {title} in the route makes it a path parameter.e
def search(title: str):
    if not title:
        raise HTTPException(detail = "Enter a title")
    return [book for book in books.values() if title.lower() in book["title"].lower()]

"""else print(...). A filtering comprehension automatically returns [] when nothing matches. print() writes to your terminal; it doesn’t send a message to the client."""



class BookCreate(BaseModel):
    title: str = Field(min_length = 1)
    author: str = Field(min_length = 1)    


@app.post("/books", status_code = 201)    #201 means “Created.” It tells the client that the request successfully 
# created a resource. Adding status_code=201 to the decorator tells FastAPI
def new_book(new_book: BookCreate):
    new_id = max(books, default= 0)+1
    books[new_id] = {
        "title": new_book.title,
        "author": new_book.author
    }

    return {
    "id": new_id,
    "title": new_book.title,
    "author": new_book.author,
}


    
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books.keys():
        raise HTTPException(status_code = 404, detail = "No such book buddy")
    del books[book_id]
    return books

class UpdateBook(BaseModel):
    title: str = Field(min_length = 1)
    author: str = Field(min_length= 1)



class BookResponse(BaseModel):
    title: str
    author: str
#response_model describes the data your endpoint sends back.



@app.put("/books/{book_id}")
def update_book(book_id: int, book_update: UpdateBook):
    if book_id not in books:
        raise HTTPException(status_code = 404, detail="No such book honey")

    books[book_id] = {"title":book_update.title, "author": book_update.author}
    # return {book_id, books[book_id] }  fails because a set cannot contain a dictionary.
    return {
    "id": book_id,
    "title": book_update.title,
    "author": book_update.author,
}


def find_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code= 404, detail="book not found")
    return books[book_id]

@app.get("/book/{book_id}", response_model = BookResponse)
def get_single_book(book: dict=Depends(find_book)): #depends supplies sth that your endpoint needs
    return book


"""async def defines a coroutine function—a function
 that can pause while waiting for an asynchronous operation.
 await is used inside it to wait for that operation’s result.
   While it waits, Python can run other tasks instead of blocking the program.

This is useful for I/O-bound work, such as making API requests or querying a database, 
especially when an application handles many tasks at once. The operation you await must support asynchronous use."""

"""An API request is a message your program sends to another program over
 the internet to ask for data or perform an action. For example, your app can ask GitHub for information."""




"""async doesn’t automatically make code faster. It helps the server handle concurrent requests while operations wait."""
import asyncio
@app.get("/books/{book_id}/availability")
async def check_awailability(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code = 404, detail= "Book not found")
    await asyncio.sleep(3)
    return {f"{book_id} is available!"}

