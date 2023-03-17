from flask import Flask 
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from vista import VistaToken, VistaValidar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

app_context = app.app_context()
app_context.push()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaToken, '/token')
api.add_resource(VistaValidar, '/operacion')
jwt = JWTManager(app)
