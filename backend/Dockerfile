FROM python:3.8
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["uvicorn", "asgi:application", "--host", "0.0.0.0", "--port", "5000", "--reload"]
