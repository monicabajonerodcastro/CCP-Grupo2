FROM python:3.9-slim

WORKDIR /monitoreo

COPY . .

RUN pip install -r requirements.txt
RUN apt-get -y update; apt-get -y install curl; apt-get -y install vim

CMD [ "python", "./monitoring.py"]
