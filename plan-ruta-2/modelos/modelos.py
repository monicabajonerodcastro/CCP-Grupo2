from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()


class PlanRuta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_entrega = db.Column(db.Date)
    clientes = db.Column(db.String)
    ruta_optima = db.Column(db.String)

    





