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


class SubmissionFile(BaseORMSchema):
    filename: str
    path: str


class Submission(BaseORMSchema):
    assignment_id: int
    student_id: int
    submission_datetime: datetime
    late: bool
    overdue: bool

    student: Student
    files: List[SubmissionFile]


class Course(BaseORMSchema):
    d2l_id: str
    name: str


class CourseCreate(BaseSchema):
    d2l_id: str
    name: str


class Assignment(BaseORMSchema):
    name: str
    due_datetime: datetime
    expected_files: Optional[List[str]] = []


class AssignmentFull(Assignment):
    submissions: Optional[List[Submission]] = []


class AssignmentCreate(BaseSchema):
    # class_id: int
    name: str
    due_datetime: datetime

