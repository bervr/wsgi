from pydantic import BaseModel, validator, Field
from datetime import date
from typing import List


class Genre(BaseModel):
    name: str


class Book(BaseModel):
    title: str
    writer: str = {}
    duration: str
    date: date
    summary: str
    genres: List[Genre] = []
    pages: int = 0


class Author(BaseModel):
    first_name: str = Field(..., max_length=14, description="max lenght is 14 characters")
    last_name: str
    age: int = Field(..., gt=15, lt=99, description="age must be more 15 and less 99")
    # @validator('age')
    # def check_age(cls, v):
    #     if v <18:
    #         raise ValueError('Age must be more 18')
    #     return v