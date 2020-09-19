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


class Course(BaseORMSchema):
    d2l_id: str
    name: str


class CourseCreate(BaseSchema):
    d2l_id: str
    name: str


class Assignment(BaseORMSchema):
    course_id: int
    d2l_id: str
    name: str
    due_database: datetime


class AssignmentCreate(BaseSchema):
    course_id: int
    d2l_id: str
    name: str
    due_database: datetime


class AssignmentSubmission(BaseORMSchema):
    assignment_id: int
    student_id: int
    d2l_id: str
    name: str
    submission_datetime: datetime
