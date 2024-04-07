from app.models.utils import ResponseModel
from fastapi import HTTPException
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from app.models.userModel import User, UpdateUserModel
from app.controllers.userController import (
    get_all_users,
    add_user,
    retrieve_user,
    delete_user,
    update_user,
)

router = APIRouter()
@router.post("/add/user", response_description="Adding New user in the database")
async def add_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "New User Added")


@router.get("/get/users", response_description="Get All Users")
async def get_all_user():
    users = await get_all_users()
    return ResponseModel(users, "List of All users")


@router.get("/get/user/{id}", response_description="Fetching Specific User")
async def get_user_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User Retrieved Successfully")
    return HTTPException(status_code=404, detail=f"User with {id} doesn't Exist")


@router.delete(
    "/delete/user/{id}", response_description="Delete The User with their Id"
)
async def delete_user_data(id):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    else:
        return HTTPException(status_code=404, detail=f"User with Id {id} not exist")


@router.put("/update/user/{id}", response_description="Update the User")
async def update_user_data(id: str, req: UpdateUserModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}

    updated_user = await update_user(id, req)
    if update_user:
        return ResponseModel(
            "User with ID: {}  update is successful".format(id),
            "User updated successfully",
        )
    else:
        return HTTPException(status_code=404, detail=f"User with ID {id} not found")
