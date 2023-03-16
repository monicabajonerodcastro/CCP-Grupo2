import json
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
import requests

class VistaToken(Resource):
    
    def post(self):
        contrasena=request.json["contrasena"]
        usuario=request.json["usuario"]

        json_body={"usuario": usuario, "contrasena":contrasena}

        #try:
        response = requests.post(url = "http://usuario:5002/signin", json=json_body)
        data = response.json()
        print(response)
        if data=="Credenciales incorrectas" or data is None:
            return {"mensaje": "Credenciales incorrectas"}, 401    
        else:
            additional_claims = {"id_rol": data['rol']['valor_rol']}
            token_de_acceso = create_access_token(identity=data['id'], additional_claims=additional_claims)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": data['id'],
                "tipo_usuario": data['rol']['tipo_rol'], "id_rol": data['rol']['valor_rol']}, 200
        #except:
         #   return {"mensaje": "No se pudo validar información de inicio de sesión"}, 401
