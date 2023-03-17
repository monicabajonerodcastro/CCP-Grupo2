import json
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask_restful import Resource
import requests
from datetime import datetime
from datetime import timezone


class VistaToken(Resource):

    def post(self):
        contrasena = request.json["contrasena"]
        usuario = request.json["usuario"]

        json_body = {"usuario": usuario, "contrasena": contrasena}

        # try:
        response = requests.post(url="http://usuario:5002/signin", json=json_body)
        data = response.json()
        print(response)
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
        tipo_operacion = request.json["operacion"]
        claims = get_jwt()
        entitlements = {'request': False, 'update': False}
        response = {}
        if claims['id_rol'] == 1:
            entitlements['request'] = True
            entitlements['update'] = True
        elif claims['id_rol'] == 2:
            entitlements['request'] = True
        else:
            return {"mensaje": "El usuario no tiene permisos para esta acción"}, 401

        if tipo_operacion == "actualizar_orden" and entitlements['update'] == True:
            response = requests.post(url="http://orden:5005/orden", json=request.json)
            response = response.json()
        elif tipo_operacion == "consultar_vendedor" and entitlements['request'] == True:
            # TODO -> redirigir a servicio de consulta vendedor
            # response = requests.get(url = "http://orden:5005/vendedor", json=request.json)
            response = {"mensaje": "Soy el admin y puedo consultar"}, 401
        else:
            return {"mensaje": "Operación no valida"}, 401
        return response
