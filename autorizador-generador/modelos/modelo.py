from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()


class RolTipo(enum.Enum):
    VENDEDOR = 1
    ADMIN = 2    


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))   
    rol = db.Column(db.Enum(RolTipo))