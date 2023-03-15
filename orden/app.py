from flask import Flask 
from flask_cors import CORS
from flask_restful import Api

from modelo import db
from vista import VistaOrden, VistaHealthCheck

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaOrden, '/orden')
api.add_resource(VistaHealthCheck, '/health-check')
