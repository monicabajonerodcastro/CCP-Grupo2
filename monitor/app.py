from flask import Flask 
import requests
import time
import threading
import socket
import logging

app = Flask(__name__)

def get():

    response_health = requests.get(url = "http://orden:5005/health-check")

    data_health = response_health.json()

    if data_health['status']=='UP':
        alert='Connection established'
    else:
        alert='Connection NOT established'

def timer():
    while True:
        tiempo=time.strftime("%H:%M:%S %d/%m/%y")
        try:
            get()
            print(tiempo, 'Connection established', flush=True)
            logging.info(tiempo+ ' Connection established')
        except:
            print(tiempo, 'Connection NOT established', flush=True)
            logging.warning(tiempo+ ' Connection NOT established')
        time.sleep(5)   

logging.basicConfig(filename='logConnection.log', encoding='utf-8', level=logging.INFO)
t = threading.Thread(target=timer)
t.start()
