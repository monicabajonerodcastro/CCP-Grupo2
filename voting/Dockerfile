FROM python:3.9-slim

WORKDIR /voting

COPY . .

RUN pip install -r requirements.txt
RUN apt-get -y update; apt-get -y install curl


CMD gunicorn --bind 0.0.0.0:5004 app:app --log-level debug
