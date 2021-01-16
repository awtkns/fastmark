import shutil
import os
from typing import List
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, utils, config

router = APIRouter()


@router.post("/assignments/", response_model=schemas.Assignment)
def add_assignment(assignment: schemas.AssignmentCreate, db: session = Depends(session)):
    db_assignment = models.Assignment(expected_files=['fcts.cpp', 'fcts.h', 'fcts_unittest.cpp'], **assignment.dict()).save(db)

    return db_assignment


@router.get("/assignments/", response_model=List[schemas.Assignment])
def get_assignments(db: session = Depends(session)):
    return db.query(models.Assignment).all()


@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentFull)
def get_assignment(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    assignment.submissions.sort(key=lambda x: x.student.name)

    return assignment


@router.put("/assignments/{assignment_id}")
def make_moss_folder(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    files = db.query(models.SubmissionFile)\
        .join(models.Submission, models.Assignment)\
:ti        .filter(models.SubmissionFile.filename == "BST.cpp", models.Assignment.id == assignment_id)\
        .all()

    moss_folder = os.path.join(assignment.path, '__MOSS__')
    if os.path.exists(moss_folder):
        shutil.rmtree(moss_folder)
    os.mkdir(moss_folder)
    [shutil.copy(
            os.path.join(config.UPLOAD_DIR, f.path),
            os.path.join(moss_folder, f'{f.submission.student.name.replace(" ","")}_{f.filename}'))
        for f in files]


@router.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: session = Depends(session)):
    if assignment := db.query(models.Assignment).get(assignment_id):
        assignment.delete(db)

    return 'Deleted'


@router.post("/assignments/{assignment_id}/key", response_model=schemas.AssignmentSolution)
def set_assignment_solution(assignment_id: int, file: bytes = File(...), db: session = Depends(session)):
    """Upload a solution for the assignment."""

    if not (key_student := db.query(models.Student).filter_by(name="__KEY__").first()):
        key_student = models.Student(name="__KEY__").save(db)

    solution = models.Submission(assignment_id=assignment_id, is_key=True, student_id=key_student.id)
    solution.save(db)

    with open('tmp_key', 'wb') as f:
        f.write(file)

    shutil.unpack_archive('tmp_key', extract_dir=solution.path, format='zip')
    utils.flatten_dir(solution.path)

    return solution
