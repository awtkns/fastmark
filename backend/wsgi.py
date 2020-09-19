import uvicorn

from api import app as application


if __name__ == '__main__':
    uvicorn.run('wsgi:application', port=5000, reload=True)
