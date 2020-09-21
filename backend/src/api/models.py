import datetime
import os

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from . import config
from .database import BaseModel


class Course(BaseModel):
    d2l_id = Column(String)
    name = Column(String)


class Assignment(BaseModel):
    # class_id = Column(ForeignKey('course.id'), nullable=False)
    name = Column(String, unique=True, nullable=False)
    due_datetime = Column(DateTime)
    expected_files = Column(ARRAY(String))
    submissions = relationship('Submission')

    @property
    def path(self):
        return os.path.join(config.UPLOAD_DIR, self.name)


class Student(BaseModel):
    d2l_id = Column(String)
    name = Column(String)


class Submission(BaseModel):
    assignment_id = Column(ForeignKey('assignment.id'), nullable=False)
    student_id = Column(ForeignKey('student.id'), nullable=False)
    submission_datetime = Column(DateTime)

    student = relationship('Student')
    assignment = relationship('Assignment')
    files = relationship('SubmissionFile', backref="submission")

    @hybrid_property
    def late(self):
        return self.submission_datetime > self.assignment.due_datetime

    @hybrid_property
    def overdue(self):
        return self.submission_datetime > (self.assignment.due_datetime + datetime.timedelta(days=1))

    @property
    def path(self):
        return os.path.join(self.assignment.path, f"{self.student.d2l_id}_{self.student.name.replace(' ', '')}")


class SubmissionFile(BaseModel):
    submission_id = Column(ForeignKey('submission.id'), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)