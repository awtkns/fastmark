from typing import Optional, List

from .config import BaseConfig
config = BaseConfig()

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import CurrentMessage
broker = RabbitmqBroker(host=config.RABBITMQ_HOST, middleware=[CurrentMessage()])
dramatiq.set_broker(broker)

from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from . import models, schemas
from .database import session, engine
from .websockets import router

models.BaseModel.metadata.create_all(bind=engine)
app = FastAPI(docs_url='/')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from . import routes

config.apply_post_initialization_config()
