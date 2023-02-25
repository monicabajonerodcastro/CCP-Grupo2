from flask import Flask 
from flask import jsonify, request
import requests
import pika

app = Flask(__name__)

@app.route('/plan-ruta', methods=['GET'])
def get():

    params = request.args
    fecha = params.get("fecha")
    cliente = params.get("cliente")

    response_ruta_1 = requests.get(url = "http://plan-ruta-1:5001/plan-ruta-1?fecha={}&cliente={}".format(fecha, cliente))
    response_ruta_2 = requests.get(url = "http://plan-ruta-2:5002/plan-ruta-2?fecha={}&cliente={}".format(fecha, cliente))
    response_ruta_3 = requests.get(url = "http://plan-ruta-3:5003/plan-ruta-3?fecha={}&cliente={}".format(fecha, cliente))

    data_1 = response_ruta_1.json()
    data_2 = response_ruta_2.json()
    data_3 = response_ruta_3.json()

    print(data_1, flush=True)
    print(data_2, flush=True)
    print(data_3, flush=True)

    if(data_1['status'] == data_2['status'] == data_3['status']):
        print("La respuesta de los servicios son iguales", flush=True)
        response = {'status': True, 'message':"La respuesta de los servicios son iguales"}
    else:
        print("Al menos una respuesta es diferente. Servicio 1: {}, Servicio 2: {}, Servicio 3: {}".format(data_1['status'], data_2['status'], data_3['status']), flush=True)
        response = {'status': False, 'message':"Al menos una respuesta es diferente"}
    
    print("=======================================================================================================================", flush=True)
    return jsonify(response)


def publicar():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue="plan_ruta")
    channel.basic_publish(exchange='',
                            routing_key='plan_ruta',
                            body="Creacion de orden correcta")
    print("[x] Mensaje enviado", flush=True)
    connection.close()