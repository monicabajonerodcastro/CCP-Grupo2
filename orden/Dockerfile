FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /orden

COPY . .

RUN pip install -r requirements.txt
RUN apt-get -y update; apt-get -y install curl

CMD gunicorn --bind 0.0.0.0:5005 app:app