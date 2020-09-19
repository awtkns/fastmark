from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from api import schemas, session, models

router = APIRouter()


@router.post("/courses/", response_model=schemas.Course)
def add_course(course: schemas.CourseCreate, db: session = Depends(session)):
    db_course = models.Course(**course.dict()).save(db)
    print(course)

    return db_course


@router.get("/courses/", response_model=List[schemas.Course])
def get_courses(db: session = Depends(session)):
    return db.query(models.Course).all()
