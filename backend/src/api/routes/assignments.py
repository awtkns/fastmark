import shutil
import os
import io
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from api import schemas, session, models, utils, config, worker_session, export

router = APIRouter()


@router.post("/assignments/", response_model=schemas.Assignment)
def add_assignment(assignment: schemas.AssignmentCreate, db: session = Depends(session)):
    db_assignment = models.Assignment(**assignment.dict()).save(db)

    return db_assignment


@router.get("/assignments/", response_model=List[schemas.Assignment])
def get_assignments(db: session = Depends(session)):
    return db.query(models.Assignment).all()


@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentFull)
def get_assignment(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    assignment.submissions.sort(key=lambda x: x.student.name)

    return assignment


@router.get("/assignments/{assignment_id}/export")
def get_assignment(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    bytes_ = export.generate_results_report(assignment)
    report_name = f'{assignment.name}_report'

    response = StreamingResponse(io.BytesIO(bytes_), media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={report_name}.csv"

    return response


@router.put("/assignments/{assignment_id}")
def make_moss_folder(assignment_id: int, db: session = Depends(session)):
    assignment = db.query(models.Assignment).get(assignment_id)
    files = db.query(models.SubmissionFile)\
        .join(models.Submission, models.Assignment)\
        .filter(models.SubmissionFile.filename == "BST.cpp", models.Assignment.id == assignment_id)\
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


@router.post("/assignments/{assignment_id}/artifacts")
def set_assignment_solution(assignment_id: int, file: bytes = File(...), filename: str = Form(...), db: session = Depends(session)):
    """ Upload build artifacts for the assignment."""

    if not (assignment := db.query(models.Assignment).get(assignment_id)):
        raise HTTPException(404)

    if not os.path.exists(artifacts_path := assignment.artifacts_path):
        os.mkdir(artifacts_path)

    file_path = os.path.join(artifacts_path, filename)
    with open(file_path, 'wb') as f:
        f.write(file)
