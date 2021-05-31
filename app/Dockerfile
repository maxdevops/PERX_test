# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .


CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:5000", "app:app"]
