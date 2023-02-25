from flask_restful import Resource
from ..modelos import db
from flask import request, jsonify
import json
import requests
import pika
from validacion import validacion 



class vistaCrearPlanRuta(Resource):

    def get(self):
        params = request.args
        fecha = params.get("fecha")
        cliente = params.get("cliente")    

        try:
            resultado_consulta_ordenes = requests.get(url="http://orden:5005/ordenes?fecha={}&cliente={}".format(fecha, cliente))    
            dictData = json.loads(resultado_consulta_ordenes.content)
            if validacion(dictData) == 'invalido':
                return jsonify({'status': False, 'message': 'Existen datos de ordenes que NO son correctos'}), 200
            else:
                return jsonify({'status': True, 'message': 'Los datos de ordenes son correctos'}), 200
        except:
            Publicar.publicar()
            return jsonify({'status': False, 'message':"No hay conexión con el servicio"}), 200
    


class Publicar():

    def publicar():        
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue="plan_ruta")
        channel.basic_publish(exchange='',
                                routing_key='plan_ruta',
                                body="Consulta de direcciones - 2")
        print("[x] Mensaje enviado", flush=True)
        connection.close()
        