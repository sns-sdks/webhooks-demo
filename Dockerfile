FROM tiangolo/uvicorn-gunicorn:python3.8

COPY . /app

RUN pip install -r /app/requirements/app.txt
