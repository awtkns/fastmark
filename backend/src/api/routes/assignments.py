import shutil
from typing import List
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, utils

router = APIRouter()


@router.post("/assignments/", response_model=schemas.Assignment)
def add_assignment(assignment: schemas.AssignmentCreate, db: session = Depends(session)):
    db_assignment = models.Assignment(expected_files=['fcts.cpp', 'fcts.h'], **assignment.dict()).save(db)

    return db_assignment


@router.get("/assignments/", response_model=List[schemas.Assignment])
def get_assignments(db: session = Depends(session)):
    return db.query(models.Assignment).all()


@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentFull)
def get_assignment(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    assignment.submissions.sort(key=lambda x: x.student.name)

    return assignment


@router.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: session = Depends(session)):
    if assignment := db.query(models.Assignment).get(assignment_id):
        assignment.delete(db)

    return 'Deleted'


@router.post("/assignments/{assignment_id}/key", response_model=schemas.Assignment)
def set_assignment_solution(assignment_id: int, file: bytes = File(...), db: session = Depends(session)):
    """Upload a solution for the assignment."""

    assignment = db.query(models.Assignment).get(assignment_id)
    assignment.set_solution_path()

    with open('tmp_key', 'wb') as f:
        f.write(file)

    shutil.unpack_archive('tmp_key', extract_dir=assignment.solution_path, format='zip')
    utils.flatten_dir(assignment.solution_path)
    assignment.save(db)

    return assignment
