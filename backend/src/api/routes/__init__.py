from api import app

from . import courses, submissions, builds

app.include_router(courses.router)
app.include_router(submissions.router)
app.include_router(builds.router)
