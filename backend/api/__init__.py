from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from . import models, schemas
from .database import session, engine
from .websockets import router


models.BaseModel.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)
# from . import websockets


def make_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password).save(db)
    print(db_user.__dict__)

    return db_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(session)):
    return make_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(session)):
    return db.query(models.User).all()
