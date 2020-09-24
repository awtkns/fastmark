from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, File, Form
from api import schemas, session, models, config, dramatiq

router = APIRouter()


@router.get("/builds/", response_model=List[schemas.BuildResult])
def get_builds(db: session = Depends(session)):
    return db.query(models.BuildResult).all()


@router.get("/tests/", response_model=List[schemas.TestResult])
def get_tests(db: session = Depends(session)):
    return db.query(models.TestResult).all()


@router.get("/jobs/", response_model=List[schemas.ActiveJob])
def get_all_active_jobs(db: session = Depends(session)):
    return db.query(models.ActiveJob).all()
