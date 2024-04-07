from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: Optional[str] = Field(default=None, read_only=True)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_librarian: bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "jdoe@library.com",
                "is_librarian": True,
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str] = Field(description="New username for the user")
    email: Optional[EmailStr] = Field(description="New email address for the user")
    password: Optional[str] = Field(description="New password for the user")
    is_librarian: Optional[bool] = Field(description="New value for librarian status")

    class Config:
        schema_extra = {
            "example": {
                "username": "newusername",
                "email": "newemail@example.com",
                "password": "newpassword123",
                "is_librarian": True,
            }
        }
