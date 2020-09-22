from api import app

from . import courses, submissions

app.include_router(courses.router)
app.include_router(submissions.router)
