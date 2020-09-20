from typing import List
import shutil
import os

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
    db_assignment = models.Assignment(**assignment.dict()).save(db)
    print(db_assignment)

    return db_assignment


@router.get("/assignments/", response_model=List[schemas.Assignment])
def get_assignments(db: session = Depends(session)):
    return db.query(models.Assignment).all()


@router.post("/ingest")
async def create_upload_file(file: bytes = File(...), filename: str = Form(...), assignment_id: int = Form(...)):
    db_assignment = db.query(models.Assignment).get(assignment_id)

    new_folder = db_assignment.name
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)

    print("HERE")

    archive_fp = f'__zip.archive'
    with open(archive_fp, 'wb') as f:
        f.write(file)
    shutil.unpack_archive(archive_fp, new_folder, format='zip')

    for file in os.listdir(new_folder):
        if file.endswith('.zip'):
            d2l_id, name, submission_datetime, *_ = file.split(' - ')

            if not (student := db.query(models.Student).filter_by(d2l_id=d2l_id).first()):
                student = models.Student(d2l_id=d2l_id, name=name).save(db)

            submission = models.Submission(
                assignment_id=assignment_id,
                student_id=student.id,
                path=file
            ).save(db)
            print(submission)

    return {"filename": filename}
