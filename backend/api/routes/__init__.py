from api import app

from . import courses

app.include_router(courses.router)

