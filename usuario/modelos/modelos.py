from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import enum

db = SQLAlchemy()


class RolTipo(enum.Enum):
    VENDEDOR = 1
    ADMIN = 2
    OTHER = 3


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))   
    rol = db.Column(db.Enum(RolTipo))


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'tipo_rol':value.name, 'valor_rol':value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    rol = EnumADiccionario(attribute=("rol"))
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        
    id = fields.String()
        
