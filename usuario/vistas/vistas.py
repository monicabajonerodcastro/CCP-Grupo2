from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource
import hashlib
from modelos import db, Usuario, UsuarioSchema


usuario_schema = UsuarioSchema()


class VistaUsuario(Resource):

    def post(self):        
        contrasena_encriptada = hashlib.md5(request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"], Usuario.contrasena == contrasena_encriptada).first()
        if usuario is None:
            return "Credenciales incorrectas", 404
        else:
            return usuario_schema.dump(usuario)    
    
class VistaUsuarios(Resource):
    def get(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"]).first()
        if usuario is None:
            return "Usuario no encontrado", 404
        else:
            return usuario_schema.dump(usuario)



