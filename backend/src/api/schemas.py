from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel as BaseSchema, Json


class BaseORMSchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class Student(BaseORMSchema):
    d2l_id: Optional[str]
    name: str


class TestResult(BaseORMSchema):
    build_result_id: int
    name: str
    exit_code: int

    error_message: Optional[str]
    total_tests: Optional[int]
    total_errors: Optional[int]
    total_failures: Optional[int]
    json_report: Optional[dict]
    error_report_path: Optional[str]


class BuildResult(BaseORMSchema):
    submission_id: int
    exit_code: int

    error_message: Optional[str]
    test_results: Optional[List[TestResult]] = []


class SubmissionFile(BaseORMSchema):
    filename: str
    path: str


class Submission(BaseORMSchema):
    assignment_id: int
    student_id: int
    submission_datetime: datetime
    late: bool
    overdue: bool
    is_key: bool

    student: Student
    files: List[SubmissionFile]
    build_result: Optional[BuildResult] = None


class Course(BaseORMSchema):
    d2l_id: str
    name: str


class CourseCreate(BaseSchema):
    d2l_id: str
    name: str


class AssignmentSolution(BaseORMSchema):
    build_result: Optional[BuildResult] = None


class Assignment(BaseORMSchema):
    name: str
    due_datetime: datetime
    expected_files: Optional[List[str]] = []


class AssignmentFull(Assignment):
    submissions: Optional[List[Submission]] = []
    solution: Optional[AssignmentSolution] = None


class AssignmentCreate(BaseSchema):
    # class_id: int
    name: str
    due_datetime: datetime
    expected_files: Optional[List[str]] = []
    solution_test_suite: str
    student_test_suite: Optional[str]


class ActiveJob(BaseORMSchema):
    name: str
    type: str
    status: str
