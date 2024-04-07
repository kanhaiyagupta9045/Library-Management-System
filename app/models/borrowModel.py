from typing import Optional
from pydantic import BaseModel, Field


class BorrowedBook(BaseModel):
    id: Optional[str] = Field(default=None, read_only=True)
    user_id: str = Field(...) 
    book_id: str = Field(...) 
    borrowed_date: str = Field(...)
    due_date: str = Field(...)
    fine_amount: Optional[float] = Field(
        default=None, description="Fine amount (if any) for late return"
    )

    class Config:
        schema_extra = {
            "example": {
                "user_id": "user456",
                "book_id": "book123",
                "borrowed_date": "2024-04-06",
                "due_date": "2024-05-06",
                "fine_amount": 5.0,
            }
        }


class UpdateBorrowedBookModel(BaseModel):
    user_id: Optional[str] = Field(description="New user ID")
    book_id: Optional[str] = Field(description="New book ID")
    borrowed_date: Optional[str] = Field(description="New borrowed date")
    due_date: Optional[str] = Field(description="New due date")
    fine_amount: Optional[float] = Field(description="New fine amount")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "new_user456",
                "book_id": "new_book123",
                "borrowed_date": "2024-04-07",
                "due_date": "2024-05-07",
                "fine_amount": 10.0,
            }
        }
