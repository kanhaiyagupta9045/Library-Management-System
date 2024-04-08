from app.models.userModel import User, UpdateUserModel
from app.database import connect_to_mongodb
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
import bcrypt
import asyncio


async def get_mongodb_client():
    return await connect_to_mongodb()


async def Usercollection():
    client = await get_mongodb_client()
    database = client["user"]
    user_collection = database["UserCollection"]
    return user_collection


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "is_librarian": user["is_librarian"],
    }

def hash_password(password: str) -> str:
    # Hash the password using bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

# get all users
async def get_all_users():
    user_collection = await Usercollection()
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

# add user
async def add_user(user_data: dict) -> dict:
    user_collection = await Usercollection()
    if "email" not in user_data:
        return {"error": "Email is required"}

    email = user_data["email"]
    existing_user = await user_collection.find_one({"email": email})
    if existing_user:
        return {"error": "User with this email already exists"}
    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])
    user = await user_collection.insert_one(user_data)
    inserted_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(inserted_user)





# retrieve the specific user 
async def retrieve_user(id : str) ->dict :
    user_collection = await Usercollection()
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    


#delete user
async def delete_user(id: str)-> dict :
    user_collection = await Usercollection()
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user :
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True
    else :
        return False
    


#update user 
async def update_user(id: str, user : dict):
    
    if not user:
        return False
    user_collection = await Usercollection()
    user = await user_collection.find_one({"_id":ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": user}
        )
        if update_user :
            return user
        else :
            return false 
    else :
        return False
    
        

