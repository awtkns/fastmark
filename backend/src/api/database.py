from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, Session
from inflection import underscore

from api import config

engine = create_engine(config.POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://localhost:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@contextmanager
def worker_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


def session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()


class BaseModel(object):
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(self):
        return underscore(self.__name__)

    def save(self, session: Session):
        session.add(self)
        self._flush(session)
        return self

    def delete(self, session: Session):
        session.delete(self)
        self._flush(session)

    # noinspection PyMethodMayBeStatic
    def _flush(self, session: Session):
        try:
            session.flush()
        except DatabaseError:
            session.rollback()
            raise


BaseModel = declarative_base(cls=BaseModel)
