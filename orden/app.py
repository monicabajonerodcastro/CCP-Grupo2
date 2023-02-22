from flask import Flask 
from flask_cors import CORS
from flask_restful import Api

import datetime

from modelo import db, Orden
from vista import VistaOrden

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaOrden, '/ordenes')

#Insertar Datos
#with app.app_context():
#    o = Orden(id=1, nombre_cliente='Exito 170', direccion='{4.755046542855191, -74.04498580229195}', fecha_entrega=datetime.datetime(2023,2,23))
#    db.session.add(o)
#    db.session.commit()


