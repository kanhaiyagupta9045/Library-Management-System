import asyncio
from app.database import connect_to_mongodb
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId


async def get_mongodb_client():
    return await connect_to_mongodb()


async def Bookcollection():
    client = await get_mongodb_client()
    database = client["books"]
    book_collection = database["BooksCollection"]
    return book_collection


# book helper function
def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "category": book["category"],
        "description": book["description"],
        "published_date": book["published_date"],
        "quantity": book["quantity"],
    }


# add a book in the database
async def add_book(book_data: dict) -> dict:

    book_collection = await Bookcollection()
    book = await book_collection.insert_one(book_data)
    new_book = await book_collection.find_one({"_id": book.inserted_id})
    return book_helper(new_book)


# get all books
async def get_all_book():
    book_collection = await Bookcollection()
    books = []
    async for book in book_collection.find():
        books.append(book_helper(book))
    return books


# Get a book from the database
async def retrieve_book(id: str) -> dict:
    book_collection = await Bookcollection()
    book = await book_collection.find_one({"_id": ObjectId(id)})

    if book:
        return book_helper(book)


# delete a book from the database


async def delete_book(id: str):
    book_collection = await Bookcollection()
    book = await book_collection.find_one({"_id": ObjectId(id)})

    if book:
        await book_collection.delete_one({"_id": ObjectId(id)})
        return True
    else:
        return False


# update a book from the database


async def update_book(id: str, data: dict):
    # Return false if an empty request body is sent.
    if not data:
        return False

    book_collection = await Bookcollection()
    book = await book_collection.find_one({"_id": ObjectId(id)})

    if book:
        update_result = await book_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_result:
            return True
        else:
            return False
    else:
        return False
