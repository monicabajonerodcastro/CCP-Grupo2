FROM python:3.9-slim

WORKDIR /autorizador-generador

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5003 app:app