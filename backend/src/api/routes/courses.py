from typing import List
import shutil
import os
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config, utils

router = APIRouter()


@router.post("/courses/", response_model=schemas.Course)
def add_course(course: schemas.CourseCreate, db: session = Depends(session)):
    db_course = models.Course(**course.dict()).save(db)

    return db_course


@router.get("/courses/", response_model=List[schemas.Course])
def get_courses(db: session = Depends(session)):
    return db.query(models.Course).all()


def delete_makefile(path):
    if ret := path.lower().endswith('makefile'):
        os.remove(path)

    return ret


@router.post("/ingest")
async def create_upload_file(file: bytes = File(...), filename: str = Form(...), assignment_id: int = Form(...), db: session = Depends(session)):
    db_assignment = db.query(models.Assignment).get(assignment_id)

    if not os.path.exists(assignment_folder := db_assignment.path):
        os.mkdir(assignment_folder)

    with open('tmp', 'wb') as f:
        f.write(file)
    shutil.unpack_archive('tmp', extract_dir=assignment_folder, format='zip')

    for file in os.listdir(assignment_folder):
        print(file)

        submission_file_path = os.path.join(assignment_folder, file)

        if os.path.isdir(file):
            break

        try:
            d2l_id, name, submission_datetime, file_name, *_ = file.split(' - ')
        except ValueError:
            break

        submission_datetime = datetime.strptime(submission_datetime, '%b %d, %Y %I%M %p')
        if not (student := db.query(models.Student).filter_by(d2l_id=d2l_id).first()):
            student = models.Student(d2l_id=d2l_id, name=name).save(db)

        db_submission = models.Submission(
            assignment_id=assignment_id,
            student_id=student.id,
            submission_datetime=submission_datetime,
        ).save(db)

        os.mkdir(submission_folder := db_submission.path)

        # Students submitted a zip
        if file.endswith('.zip'):

            shutil.unpack_archive(submission_file_path, extract_dir=submission_folder)
            utils.flatten_dir(submission_folder)

            # Cleaning up
            [os.rmdir(dir_) for dir_ in os.listdir(submission_folder) if os.path.isdir(dir_)]

        # student submitted a single file
        else:
            shutil.copyfile(submission_file_path, os.path.join(submission_folder, file_name))

        # Saving files
        [models.SubmissionFile(
            submission_id=db_submission.id,
            filename=f,
            path=os.path.relpath(p, config.UPLOAD_DIR)
        ).save(db) for f in os.listdir(submission_folder) if
         not delete_makefile(p := os.path.join(submission_folder, f))]

        try:
            os.remove(submission_file_path)
        except PermissionError:
            pass

    return {"filename": filename}
