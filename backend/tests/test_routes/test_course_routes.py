from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from api import app, schemas

app.add_middleware(CORSMiddleware)
client = TestClient(app)


def test_get_courses():
    response = client.get("/courses")
    assert response.status_code == 200
    return response.json()


def test_post_course():
    course = schemas.CourseCreate(d2l_id="123", name="test_course")
    response = client.post("/courses/", json=course.dict())
    assert response.status_code == 200


