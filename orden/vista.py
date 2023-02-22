from flask import jsonify
from flask_restful import Resource
from modelo import Orden, OrdenSchema

orden_schema = OrdenSchema()

class VistaOrden(Resource):
    def get(self):
        ordenes = Orden.query.all()
        return [orden_schema.dump(orden) for orden in ordenes]

class VistaHealthCheck(Resource):
    def get(self):
        return jsonify({'status': 'UP'})
