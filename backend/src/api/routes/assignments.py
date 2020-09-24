from typing import List
from fastapi import APIRouter, Depends
from api import schemas, session, models

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
    ass = db.query(models.Assignment).get(assignment_id)
    return ass


@router.delete("/assignments/{assignment_id}")
def delete_assignment(assignment_id: int, db: session = Depends(session)):
    if assignment := db.query(models.Assignment).get(assignment_id):
        assignment.delete(db)

    return 'Deleted'
