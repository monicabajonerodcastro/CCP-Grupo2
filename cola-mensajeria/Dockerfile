FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /orden

COPY . .

RUN pip install -r requirements.txt
RUN apt-get update;apt-get install nano -y;