from bson.objectid import ObjectId
from app.models.borrowModel import BorrowedBook, UpdateBorrowedBookModel
from app.database import connect_to_mongodb
from app.controllers.userController import Usercollection
from app.controllers.bookController import Bookcollection


async def get_mongodb_client():
    return await connect_to_mongodb()


async def collection():
    client = await get_mongodb_client()
    database = client["Borrow"]
    user_collection = database["BorrowCollection"]
    return user_collection


def borrow_helper(borrow) -> dict:
    return {
        "id": str(borrow["_id"]),
        "user_id": borrow["user_id"],
        "book_id": borrow["book_id"],
        "borrowed_date": borrow["borrowed_date"],
        "due_date": borrow["due_date"],
        "fine_amount": borrow["fine_amount"],
    }


# apis for adding user who is taking book from library
async def add_borrower(borrow_data: dict) -> dict:
    borrow_collection = await collection()
    user_collection = await Usercollection()
    book_collection = await Bookcollection()
    if "user_id" not in borrow_data:
        return {"error": "User ID is required"}
    existing_user = await user_collection.find_one(
        {"_id": ObjectId(borrow_data["user_id"])}
    )
    if not existing_user:
        return {"error": "User does not exist, please create an account"}
    if "book_id" not in borrow_data:
        return {"error": "Book ID is required to check availability"}
    existing_book = await book_collection.find_one(
        {"_id": ObjectId(borrow_data["book_id"])}
    )
    if not existing_book:
        return {"error": "Book is not available in the Library. We will add it later."}

    borrowed_book = await borrow_collection.insert_one(borrow_data)
    inserted_borrowed_book = await borrow_collection.find_one(
        {"_id": borrowed_book.inserted_id}
    )

    return borrow_helper(inserted_borrowed_book)


# apis for getting all borrower_data
async def get_borrower_data():
    borrow_collection = await collection()
    borrowers = []
    async for borrower in borrow_collection.find():
        borrowers.append(borrow_helper(borrower))
    return borrowers


# update borrower data
async def update_borrower(id: str, borrower: dict):
    if not borrower:
        return False
    borrow_collection = await collection()
    borrower_data = await borrow_collection.find_one({"_id": ObjectId(id)})
    if borrower_data:
        updated_borrower_data = await borrow_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": borrower}
        )
        if updated_borrower_data:
            return True
        else:
            return False
    else :
        return False


# apis for removing the borrwer data from database
async def remove_borrower(id: str):
    borrow_collection = await collection()
    borrower_data = await borrow_collection.find_one({"_id": ObjectId(id)})
    if borrower_data:
        await borrow_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False
