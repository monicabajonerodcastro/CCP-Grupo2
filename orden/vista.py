from flask import jsonify, request
from flask_restful import Resource
from modelo import db, Orden, OrdenSchema
import datetime

orden_schema = OrdenSchema()

class VistaOrden(Resource):
    def post(self):
        id_orden = request.json["id"]
        orden = Orden.query.get_or_404(id_orden)
        if orden is None:
            return "No se encuentra a orden {}".format(id_orden), 404
        else:
            orden.nombre_cliente = request.json["nombre_cliente"]
            orden.direccion = request.json["direccion"]
            fecha_entrega = request.json["fecha_entrega"].split("-")
            orden.fecha_entrega = datetime.datetime(year=int(fecha_entrega[0]),
                                                    month=int(fecha_entrega[1]),
                                                    day=int(fecha_entrega[2]))
            db.session.add(orden)
            db.session.commit()
            return orden_schema.dump(orden)


class VistaHealthCheck(Resource):
    def get(self):
        return jsonify({'status': 'UP'})
