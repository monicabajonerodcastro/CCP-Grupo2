from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import event

import datetime
import json

db = SQLAlchemy()

class Orden(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(128))
    direccion = db.Column(db.String(128))
    fecha_entrega = db.Column(db.Date())
    
class OrdenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Orden
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.String()
    nombre_cliente = fields.String()
    direccion = fields.String()
    fecha_entrega = fields.String()

# Insertar Datos iniciales
def insert_data(target, connection, **kw):
    f = open('datos.json')
    data = json.load(f)
    for i in data:
        fecha_split = i['fecha_entrega'].split("-")
        connection.execute(target.insert(), {'id': i['id'], 'nombre_cliente':i['nombre_cliente'], 'direccion':i['direccion'], 'fecha_entrega':datetime.datetime(int(fecha_split[0]), int(fecha_split[1]), int(fecha_split[2]))})

event.listen(Orden.__table__, 'after_create', insert_data)