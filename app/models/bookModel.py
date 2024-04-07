from typing import Optional
from pydantic import BaseModel, Field, validator

class Book(BaseModel):
    id: Optional[str] = Field(default=None, read_only=True)
    title: str = Field(...)
    author: str = Field(...)
    isbn: str = Field(..., min_length=10)
    category: str = Field(...)
    description: Optional[str] = Field(default=None)
    published_date: str = Field(...)
    quantity: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "isbn": "9780345504243",
                "category": "Science Fiction",
                "description": "A humorous science fiction comedy series created by Douglas Adams.",
                "published_date": "1979-10-12",
                "quantity": 5,
            }
        }


class UpdateBookModel(BaseModel):
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]
    category: Optional[str]
    description: Optional[str]
    published_date: Optional[str]
    quantity: Optional[int]

    @validator('isbn', pre=True)
    def validate_isbn(cls, v):
        if v is not None:
            cleaned_isbn = ''.join(filter(str.isdigit, v))
            if len(cleaned_isbn) < 10:
                raise ValueError('ISBN must be at least 10 characters long')
        return v
