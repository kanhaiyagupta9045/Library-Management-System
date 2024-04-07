from fastapi import APIRouter, Body, HTTPException
from app.controllers.borrowController import (
    add_borrower,
    remove_borrower,
    get_borrower_data,
    update_borrower,
)
from app.models.utils import ResponseModel
from app.models.borrowModel import BorrowedBook, UpdateBorrowedBookModel
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.post("/add/borrower", response_description="Adding Data of Borrower")
async def add_borrower_data(borrow_data: BorrowedBook = Body(...)):
    borrow_data = jsonable_encoder(borrow_data)
    inserted_borrowed_data = await add_borrower(borrow_data)
    if "error" in inserted_borrowed_data:
        return HTTPException(status_code=404, detail=inserted_borrowed_data["error"])

    return ResponseModel(inserted_borrowed_data, "Borrower Data Added Successfully")


@router.get(
    "/get/borrowers",
    response_description="APIS to retrieve All the borrower from Database",
)
async def retrive_borrowers_data():
    borrowers = await get_borrower_data()
    return ResponseModel(borrowers, "Borrowers Data Retrieved Successfully")


@router.put("/update/borrower/{id}", response_description="APis to Update Borrower Data")
async def update_borrowe_data(id: str, req: UpdateBorrowedBookModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_borrower_data = await update_borrower(id,req)
    if updated_borrower_data:
        return ResponseModel(
            "Borrower with ID: {} update is successful".format(id),
            "Borrower Data updated successfully",
        )
    return HTTPException(status_code=404, detail=f"Borrower with ID {id} not found")


@router.delete(
    "/delete/borrower/{id}", response_description="Removing Borrower Data from Database"
)
async def remove_borrower_data(id: str):
    deleted_borrower_data = await remove_borrower(id)
    if deleted_borrower_data:
        return ResponseModel(
            "Borrower with ID: {} removed".format(id), "Borrower deleted successfully"
        )
    else:
        return HTTPException(status_code=404, detail=f"User with Id {id} not exist")
