FROM python:3.9-slim

WORKDIR /orden

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5001 app:app