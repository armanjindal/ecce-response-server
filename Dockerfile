FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app

COPY ./requirements-actions.txt ./

USER root 

RUN pip install -r requirements-actions.txt

USER 1001