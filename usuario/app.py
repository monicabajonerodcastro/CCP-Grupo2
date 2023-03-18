from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import hashlib
from modelos import db, Usuario, RolTipo
from vistas import VistaUsuario, VistaUsuarios

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaUsuario, '/signin')
api.add_resource(VistaUsuarios, '/usuario')

jwt = JWTManager(app)

# Inicializar usuarios en base de datos
with app.app_context():
    usuarios = db.session.query(Usuario).all()
    for usuario in usuarios:
        db.session.delete(usuario)
        db.session.commit()

    contrasena = 'miso2022'
    usuario = Usuario(usuario='jm.carrillo', contrasena=hashlib.md5(contrasena.encode('utf-8')).hexdigest(),
                      rol=RolTipo.ADMIN)
    db.session.add(usuario)
    db.session.commit()
    contrasena = 'miso2023'
    usuario = Usuario(usuario='w.sanchez', contrasena=hashlib.md5(contrasena.encode('utf-8')).hexdigest(),
                      rol=RolTipo.VENDEDOR)
    db.session.add(usuario)
    db.session.commit()
    contrasena = 'miso2023'
    usuario = Usuario(usuario='a.calamaro', contrasena=hashlib.md5(contrasena.encode('utf-8')).hexdigest(),
                      rol=RolTipo.OTHER)
    db.session.add(usuario)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
