from api import app

from . import courses, assignments, submissions, builds

app.include_router(courses.router, tags=['Courses'])
app.include_router(assignments.router, tags=['Assignments'])
app.include_router(submissions.router, tags=['Submissions'])
app.include_router(builds.router, tags=['Build & Test'])

