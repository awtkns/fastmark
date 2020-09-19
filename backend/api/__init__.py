from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from . import models, schemas
from . import SessionLocal, engine


if __name__ == '__main__':
    pass