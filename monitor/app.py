from flask import Flask 
import requests
import time
import threading
import socket
import logging

app = Flask(__name__)

@app.route('/monitor', methods=['GET'])
def get():

    response_ruta_1 = requests.get(url = "http://orden:5005/health-check")

    data_1 = response_ruta_1.json()

    if data_1['status']=='UP':
        alert='Connection established'
    else:
        alert='Connection NOT established'

    return alert

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

logging.basicConfig(filename='logConnection.log', encoding='utf-8', level=logging.DEBUG, force=True)
t = threading.Thread(target=timer)
t.start()
