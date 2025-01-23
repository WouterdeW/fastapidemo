import re
from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


class UserType(str, Enum):
    student = "student"
    teacher = "teacher"


class Contact(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    user_type: UserType

    @validator('first_name', 'last_name')
    def name_must_be_in_alphabetic_characters(self, name):
        if not re.match("^[a-zA-Z_]+$", name):
            raise ValueError("Name cannot be empty and must only contain characters from the Alphabet")


class Student(Contact):
    user_type: UserType = UserType.student
    curriculum: str
    enrollment_year: int


class Teacher(Contact):
    user_type: UserType = UserType.teacher
    subject: str


class Course(BaseModel):
    name: str
    subject: str
    start_date: date


