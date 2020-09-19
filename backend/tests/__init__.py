from fastapi import TestClient
from src import app

client = TestClient(app)
print("HERE")
Assert(False)