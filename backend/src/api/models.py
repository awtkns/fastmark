import datetime
import os
import shutil

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.hybrid import hybrid_property

from . import config
from .database import BaseModel


class Course(BaseModel):
    name = Column(String)

    assignments = relationship('Assignment')


class Assignment(BaseModel):
    course_id = Column(ForeignKey('course.id'))
    name = Column(String, nullable=False)
    description = Column(String)
    due_datetime = Column(DateTime)
    expected_files = Column(ARRAY(String))

    submissions = relationship('Submission', backref="assignment", cascade="all,delete,delete-orphan")

    @property
    def path(self):
        return os.path.join(config.UPLOAD_DIR, f'{self.name}_{self.id}')

    def delete(self, session):
        super().delete(session)

        # Cleaning up folders
        if os.path.exists(path := self.path) and os.path.isdir(path):
            shutil.rmtree(path)


class Student(BaseModel):
    d2l_id = Column(String)
    name = Column(String)


class Submission(BaseModel):
    assignment_id = Column(ForeignKey('assignment.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    submission_datetime = Column(DateTime, default=datetime.datetime.now)
    is_key = Column(Boolean, default=False)

    student = relationship('Student')
    files = relationship('SubmissionFile', backref="submission", cascade="all,delete,delete-orphan")
    build_result = relationship('BuildResult', backref="submission", cascade="all,delete,delete-orphan", uselist=False)

    @hybrid_property
    def late(self):
        return self.submission_datetime > self.assignment.due_datetime

    @hybrid_property
    def overdue(self):
        return self.submission_datetime > (self.assignment.due_datetime + datetime.timedelta(days=1))

    @property
    def path(self):
        return os.path.join(self.assignment.path, self.student.name.replace(' ', ''))


class TestResult(BaseModel):
    build_result_id = Column(ForeignKey('build_result.id', ondelete='CASCADE'), nullable=False)
    name = Column(String)
    exit_code = Column(Integer, nullable=False)
    error_message = Column(String)

    total_tests = Column(Integer)
    total_failures = Column(Integer)
    total_errors = Column(Integer)

    json_report = Column(postgresql.JSONB)
    stderr = Column(String)


class BuildResult(BaseModel):
    submission_id = Column(ForeignKey('submission.id', ondelete='CASCADE'), nullable=False)
    exit_code = Column(Integer)
    error_message = Column(String)

    test_results = relationship('TestResult', cascade="all,delete,delete-orphan")


class SubmissionFile(BaseModel):
    submission_id = Column(ForeignKey('submission.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)


class ActiveJob(BaseModel):
    name = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, default='queued')
