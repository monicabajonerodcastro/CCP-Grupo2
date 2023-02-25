from flask import Flask 
from flask import jsonify, request
import requests
import pika

app = Flask(__name__)

@app.route('/plan-ruta-3', methods=['GET'])
def get():
    params = request.args
    fecha = params.get("fecha")
    cliente = params.get("cliente")
    
    try:
        response_ruta_1 = requests.get(url="http://orden:5005/ordenes?fecha={}&cliente={}".format(fecha, cliente))
        data_1 = response_ruta_1.json()
        retorno=True
        for i in data_1:
            if i['nombre_cliente'] is not None and i['direccion']['latitud'] is not None and i['direccion']['longitud'] is not None:
                if not is_dataOk(i['nombre_cliente'],i['direccion']['latitud'],i['direccion']['longitud']):
                    retorno =False
                    break
            else:
                retorno =False
                break
        if(retorno):
            mensaje='Los datos son validos'
        else:
            print("Validacion fallo # 3", flush=True)
            mensaje='Los datos no son validos'
        response = {'message': mensaje, 'status': retorno}
        return jsonify(response), 200
    except:
        publicar()
        return jsonify({'status': False, 'message':"No hay conexión con el servicio"}), 200


def isNameOk(nombre):
    return nombre !=""

def is_float(variable):
    try:
        float(variable)
        return True
    except:
        return False

def isAddressOk(latitud, longitud):
    if is_float(latitud) and is_float(longitud) and latitud !="" and longitud !="":
        if (float(latitud)<= 4.778211501715016 and float(latitud) >= 4.51360957443485 and float(longitud)<= -74.02618417788635 and float(longitud) >= -74.23457623538577):
            return True
    return False

def is_dataOk(nombre, latitud, longitud):
    return isNameOk(nombre) and isAddressOk(latitud, longitud)

def publicar():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue="plan_ruta")
    channel.basic_publish(exchange='',
                            routing_key='plan_ruta',
                            body="Consulta de direcciones - 3")
    print("[x] Mensaje enviado", flush=True)
    connection.close()
