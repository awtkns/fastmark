from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel as BaseSchema


class BaseORMSchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class Student(BaseORMSchema):
    d2l_id: str
    name: str


class Submission(BaseORMSchema):
    assignment_id: int
    student_id: int
    submission_datetime: datetime

    student: Student


class Course(BaseORMSchema):
    d2l_id: str
    name: str


class CourseCreate(BaseSchema):
    d2l_id: str
    name: str


class Assignment(BaseORMSchema):
    name: str
    due_datetime: datetime


class AssignmentFull(Assignment):
    submissions: List[Submission] = []


class AssignmentCreate(BaseSchema):
    # class_id: int
    name: str
    due_datetime: datetime

