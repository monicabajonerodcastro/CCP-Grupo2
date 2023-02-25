from flask import Flask
from flask import jsonify, request
import requests
import pika
from decimal import Decimal

app = Flask(__name__)


@app.route('/plan-ruta-1', methods=['GET'])
def get():
    params = request.args
    fecha = params.get("fecha")
    cliente = params.get("cliente")
    
    

    def es_valida_direccion(direccion):
        latitud_rangos = [4.51360957443485, 4.778211501715016]
        longitud_rangos = [-74.23457623538577, -74.02618417788635]
        if direccion['nombre_cliente'] is not None and not direccion['nombre_cliente'].replace(" ", "").isalnum():
            return {'status': False, 'message': 'el nombre no es valido'}
        try:
            latitud = Decimal(direccion['direccion']['latitud'])
            longitud = Decimal(direccion['direccion']['longitud'])
        except:
            return {'status': False, 'message': 'la direccion debe ser un numero'}
        if not (latitud_rangos[0] < latitud < latitud_rangos[1] and longitud_rangos[0] < longitud < longitud_rangos[1]):
            return {'status': False, 'message': 'la direccion no esta en el rango'}
        return {'status': True, 'message': 'la direccion es valida'}


    def validar_listado_direcciones(direcciones):
        response = {'status': True, 'message': 'la direcciones son validas'}
        for direccion in direcciones:
            if not es_valida_direccion(direccion)['status']:
                print("Validacion fallo # 1", flush=True)
                response = {'status': False, 'message': 'Todas las direcciones deben ser validas'}
                break
        return response

    try:
        response_ruta_1 = requests.get(url="http://orden:5005/ordenes?fecha={}&cliente={}".format(fecha, cliente))
        data_orden = response_ruta_1.json()
        valildacion = validar_listado_direcciones(data_orden)
        return jsonify(valildacion),200
    except:
        publicar()
        return jsonify({'status': False, 'message':"No hay conexión con el servicio"}), 200

    


def publicar():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue="plan_ruta")
    channel.basic_publish(exchange='',
                            routing_key='plan_ruta',
                            body="Consulta de direcciones - 1")
    print("[x] Mensaje enviado", flush=True)
    connection.close()
