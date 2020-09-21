from typing import List
import shutil
import os
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config

router = APIRouter()


@router.post("/courses/", response_model=schemas.Course)
def add_course(course: schemas.CourseCreate, db: session = Depends(session)):
    db_course = models.Course(**course.dict()).save(db)

    return db_course


@router.get("/courses/", response_model=List[schemas.Course])
def get_courses(db: session = Depends(session)):
    return db.query(models.Course).all()


@router.post("/assignments/", response_model=schemas.Assignment)
def add_assignment(assignment: schemas.AssignmentCreate, db: session = Depends(session)):
    db_assignment = models.Assignment(expected_files=['fcts.cpp', 'fcts.h'], **assignment.dict()).save(db)

    return db_assignment


@router.get("/assignments/", response_model=List[schemas.Assignment])
def get_assignments(db: session = Depends(session)):
    return db.query(models.Assignment).all()


@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentFull)
def get_assignment(assignment_id: int, db: session = Depends(session)):
    ass = db.query(models.Assignment).get(assignment_id)
    return ass


@router.post("/submissions/{submission_id}")
def build_submission(submission_id):
    print("building submission", submission_id)
    return f'build_submission {submission_id}'


@router.post("/ingest")
async def create_upload_file(file: bytes = File(...), filename: str = Form(...), assignment_id: int = Form(...), db: session = Depends(session)):
    db_assignment = db.query(models.Assignment).get(assignment_id)

    if not os.path.exists(assignment_folder := db_assignment.path):
        os.mkdir(assignment_folder)

    with open('tmp', 'wb') as f:
        f.write(file)
    shutil.unpack_archive('tmp', extract_dir=assignment_folder, format='zip')

    for file in os.listdir(assignment_folder):
        fp = os.path.join(assignment_folder, file)

        if os.path.isdir(file):
            break

        if file.endswith('.zip'):
            d2l_id, name, submission_datetime, *_ = file.split(' - ')
            submission_datetime = datetime.strptime(submission_datetime, '%b %d, %Y %I%M %p')

            if not (student := db.query(models.Student).filter_by(d2l_id=d2l_id).first()):
                student = models.Student(d2l_id=d2l_id, name=name).save(db)

            db_submission = models.Submission(
                assignment_id=assignment_id,
                student_id=student.id,
                submission_datetime=submission_datetime,
            ).save(db)

            os.mkdir(submission_folder := db_submission.path)
            print(fp)
            print(os.listdir('.'))
            shutil.unpack_archive(fp, extract_dir=submission_folder)

            [models.SubmissionFile(
                submission_id=db_submission.id,
                filename=f,
                path=os.path.relpath(os.path.join(submission_folder, filename), config.UPLOAD_DIR)
            ).save(db) for f in os.listdir(submission_folder)]

        os.remove(fp)

    return {"filename": filename}
