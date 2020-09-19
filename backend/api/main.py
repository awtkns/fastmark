from datetime import datetime
from typing import List, Optional

# from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

# from . import models, schemas
# from . import SessionLocal, engine

# models.BaseModel.metadata.create_all(bind=engine)


class User(BaseModel):
    id: int
    name = "John Doe"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
