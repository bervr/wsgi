from typing import List

from fastapi import FastAPI, Query, Path, Body
from schemas import Book, Author

app = FastAPI()


# @app.get('/')
# def home():
#     return {"key": "hello"}
#
#
# @app.get('/{pk}')
# def get_item(pk: int, q: str =None):
#     return {"key": pk, "q": q}
#
#
# @app.get('/user/{pk}/items/{item}')
# def get_user_item(pk: int, item: str):
#     return {"user": pk, "item": item}
#

@app.post('/book', response_model=Book, response_model_exclude_unset=True)
def create_book(item: Book, author: Author, quantity: int = Body(...)):
    return {"item": item, "author": author, "quantity": quantity}


@app.get('/book')
def get_book(q: List[str] = Query(["test1", "test2"], min_length=2, max_length=5)):
    return q

@app.post('/author', response_model=Author)
def create_author(author: Author = Body(..., embed=True)):
    return {"author": author}

@app.get('/book/{pk}')
def get_single_book(pk: int = Path(..., gt=1, le=20)):
    return {"pk": pk}
