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
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models, schemas
from .database import session, engine
from .websockets import router

models.BaseModel.metadata.create_all(bind=engine)
app = FastAPI()


from . import routes


@dramatiq.actor
def identity(x):
    print("sadsd")
    return x


@app.get('/actor')
def do_actor():
    identity.send_with_options(args=(42,))
    return 'success'