from flask import jsonify, request
from flask_restful import Resource
from modelo import Orden, OrdenSchema

orden_schema = OrdenSchema()

class VistaOrden(Resource):
    def get(self):
        params = request.args
        fecha = params.get("fecha")
        cliente = params.get("cliente")
        if fecha and cliente:
            ordenes = Orden.query.filter_by(fecha_entrega = fecha, nombre_cliente = cliente)
        else:
            if fecha:
                ordenes = Orden.query.filter_by(fecha_entrega = fecha)
            elif cliente:
                ordenes = Orden.query.filter_by(nombre_cliente = cliente)
            else:
                ordenes = Orden.query.all()
        
        respuesta_json = [orden_schema.dump(orden) for orden in ordenes]
        lista_ordenes = []
        for orden_json in respuesta_json:
            direccion = orden_json['direccion']
            direccion_split = direccion.split(";")
            direccion_formato = ({"latitud": direccion_split[0], "longitud": direccion_split[1]})
            orden_json['direccion'] = direccion_formato
            lista_ordenes.append(orden_json)

        return jsonify(lista_ordenes)


class VistaHealthCheck(Resource):
    def get(self):
        return jsonify({'status': 'UP'})
