import json, pika
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_restful import Resource
import requests
from datetime import datetime
from datetime import timezone

HOST_RABBIT_MQ = 'rabbitmq'

class VistaToken(Resource):

    def post(self):
        contrasena = request.json["contrasena"]
        usuario = request.json["usuario"]

        json_body = {"usuario": usuario, "contrasena": contrasena}

        # try:
        response = requests.post(url="http://usuario:5002/signin", json=json_body)
        data = response.json()
        if data == "Credenciales incorrectas" or data is None:
            return {"mensaje": "Credenciales incorrectas"}, 401
        else:
            additional_claims = {"id_rol": data['rol']['valor_rol']}
            token_de_acceso = create_access_token(identity=data['id'], additional_claims=additional_claims)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": data['id'],
                    "tipo_usuario": data['rol']['tipo_rol'], "id_rol": data['rol']['valor_rol']}, 200
        # except:
        #   return {"mensaje": "No se pudo validar información de inicio de sesión"}, 401


class VistaValidar(Resource):

    @jwt_required()
    def post(self):
        #tipo_operacion = request.json["operacion"]
        claims = get_jwt()
        entitlements = {'request': False, 'update': False}
        #response = {}
        if claims['id_rol'] == 1:
            entitlements['request'] = True
            entitlements['update'] = True
        elif claims['id_rol'] == 2:
            entitlements['request'] = True
        else:
            return {"mensaje": "El usuario no tiene permisos para esta acción"}, 401

        #if tipo_operacion == "actualizar_orden" and entitlements['update'] == True:
        #    response = requests.post(url="http://orden:5005/orden", json=request.json)
        #elif tipo_operacion == "consultar_vendedor" and entitlements['request'] == True:
        #    response = requests.get(url = "http://usuario:5002/usuario", json=request.json)
        #else:
        #    return {"mensaje": "Operación no valida"}, 401
        request_json = {
            "operacion": request.json["operacion"],
            "id": request.json["id"],
            "usuario": request.json["usuario"],
            "nombre_cliente": request.json["nombre_cliente"],
            "direccion": request.json["direccion"],
            "fecha_entrega": request.json["fecha_entrega"]    
        }
        publish_queue(request_json)
        return {"mensaje": "Operación enviada correctamente"}, 200


def publish_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_RABBIT_MQ))
    channel = connection.channel()
    channel.queue_declare(queue="CCP-Queue")
    channel.basic_publish(exchange='',
                            routing_key="CCP-Queue",
                            body=json.dumps(message))
    print("========== Mensaje enviado a CCP-Queue ==========", flush=True)
    connection.close()