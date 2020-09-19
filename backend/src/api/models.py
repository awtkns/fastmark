from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import BaseModel


class Course(BaseModel):
    d2l_id = Column(String)
    name = Column(String)


class Assignment(BaseModel):
    class_id = Column(ForeignKey('course.id'), nullable=False)
    name = Column(String, unique=True, nullable=False)
    due_datetime = Column(DateTime)


class Student(BaseModel):
    d2l_id = Column(String)
    name = Column(String)


class Submission(BaseModel):
    assignment_id = Column(ForeignKey('assignment.id'), nullable=False)
    student_id = Column(ForeignKey('student.id'), nullable=False)
    submission_datetime = Column(DateTime)
    path = Column(String)
