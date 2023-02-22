from flask import Flask 
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/plan-ruta', methods=['GET'])
def get():

    response_ruta_1 = requests.get(url = "http://plan-ruta-1:5001/plan-ruta-1")
    response_ruta_2 = requests.get(url = "http://plan-ruta-2:5002/plan-ruta-2")
    response_ruta_3 = requests.get(url = "http://plan-ruta-3:5003/plan-ruta-3")

    data_1 = response_ruta_1.json()
    data_2 = response_ruta_2.json()
    data_3 = response_ruta_3.json()

    response = {'1': data_1['message'], '2': data_2['message'], '3': data_3['message']}
    return jsonify(response)
