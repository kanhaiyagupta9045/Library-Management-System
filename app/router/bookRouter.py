from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from fastapi import HTTPException
from app.models.bookModel import Book, UpdateBookModel
from app.controllers.bookController import (
    add_book,
    get_all_book,
    retrieve_book,
    delete_book,
    update_book,
)

from app.models.utils import ResponseModel, ErrorResponseModel


router = APIRouter()


@router.post("/add/book", response_description="New Book is Added into Database")
async def add_new_book(book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = await add_book(book)
    return ResponseModel(new_book, "New Book Added")


@router.get("/get/books", response_description="List of All Books")
async def get_all_books():
    books = await get_all_book()
    return ResponseModel(books, "List of All books in Library")


@router.get("/get/book/{id}", response_description="Book Details Retrived")
async def get_book_data(id):
    book = await retrieve_book(id)
    if book:
        return ResponseModel(book, "Book Data Retrieved Succesfully")
    raise HTTPException(status_code=404, detail=f"Book with ID: {id} doesn't exist")


@router.delete(
    "/delete/book/{id}", response_description="Book Data deleted from the database"
)
async def delete_book_data(id):
    deleted_book = await delete_book(id)
    if deleted_book:
        return ResponseModel(
            "Book with ID: {} removed".format(id), "Book deleted successfully"
        )
    else:
        raise HTTPException(status_code=404, detail=f"Book with ID {id} not found")


@router.put("/update/book/{id}", response_description="Update the Book")
async def update_the_book(id: str, req: UpdateBookModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_book = await update_book(id, req)
    if updated_book:
        return ResponseModel(
            "Book with ID: {}update is successful".format(id),
            "Book updated successfully",
        )

    return HTTPException(status_code=404, detail=f"Book with ID {id} not found")
