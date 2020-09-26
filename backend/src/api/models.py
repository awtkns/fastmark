import datetime
import os
import shutil

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
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

    solution = relationship('AssignmentSolution', backref="assignment", cascade="all,delete,delete-orphan", uselist=False)
    submissions = relationship('Submission', backref="assignment", cascade="all,delete,delete-orphan")

    @property
    def path(self):
        return os.path.join(config.UPLOAD_DIR, self.name)

    def delete(self, session):
        super().delete(session)

        # Cleaning up folders
        if os.path.exists(path := self.path) and os.path.isdir(path):
            shutil.rmtree(path)


class AssignmentSolution(BaseModel):
    assignment_id = Column(ForeignKey('assignment.id'), unique=True)
    build_result_id = Column(ForeignKey('build_result.id'))
    path = Column(String)

    build_result = relationship('BuildResult', uselist=False)

    def set_path(self, folder_name='__KEY__'):
        self.path = os.path.join(self.assignment.path, folder_name)

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
    build_result_id = Column(ForeignKey('build_result.id'))
    submission_datetime = Column(DateTime)

    student = relationship('Student')
    files = relationship('SubmissionFile', backref="submission", cascade="all,delete,delete-orphan")
    build_result = relationship('BuildResult', uselist=False)

    @hybrid_property
    def late(self):
        return self.submission_datetime > self.assignment.due_datetime

    @hybrid_property
    def overdue(self):
        return self.submission_datetime > (self.assignment.due_datetime + datetime.timedelta(days=1))

    @property
    def path(self):
        return os.path.join(self.assignment.path, f"{self.student.name.replace(' ', '')}")


class TestResult(BaseModel):
    build_result_id = Column(ForeignKey('build_result.id', ondelete='CASCADE'), nullable=False, unique=True)
    exit_code = Column(Integer, nullable=False)
    error_message = Column(String)

    total_tests = Column(Integer)
    total_failures = Column(Integer)
    total_errors = Column(Integer)

    json_report_path = Column(String)
    error_report_path = Column(String)


class BuildResult(BaseModel):
    exit_code = Column(Integer)
    error_message = Column(String)

    test_result = relationship('TestResult', cascade="all,delete,delete-orphan", uselist=False)


class SubmissionFile(BaseModel):
    submission_id = Column(ForeignKey('submission.id', ondelete='CASCADE'), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)


class ActiveJob(BaseModel):
    name = Column(String)
    type = Column(String, nullable=False)
    status = Column(String, default='queued')
