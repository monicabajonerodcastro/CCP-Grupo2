from flask import Flask
from flask import jsonify
import requests
from decimal import Decimal

app = Flask(__name__)


@app.route('/plan-ruta-1', methods=['GET'])
def get():
    response_ruta_1 = requests.get(url="http://orden:5005/ordenes?fecha=2023-02-22&cliente=Exito%20170")
    data_orden = response_ruta_1.json()

    def es_valida_direccion(direccion):
        latitud_rangos = [4.51360957443485, 4.778211501715016]
        longitud_rangos = [-74.23457623538577, -74.02618417788635]
        if direccion['nombre_cliente'] is not None and not direccion['nombre_cliente'].replace(" ", "").isalnum():
            return {'status': False, 'message': 'el nombre no es valido'}
        try:
            latitud = Decimal(direccion['direccion']['latitud'])
            longitud = Decimal(direccion['direccion']['longitud'])
        except:
            return {'status': False, 'message': 'la direccion debe ser un numero'}
        if not (latitud_rangos[0] < latitud < latitud_rangos[1] and longitud_rangos[0] < longitud < longitud_rangos[1]):
            return {'status': False, 'message': 'la direccion no esta en el rango'}
        return {'status': True, 'message': 'la direccion es valida'}


    def validar_listado_direcciones(direcciones):
        response = {'status': True, 'message': 'la direcciones son validas'}, 200
        for direccion in direcciones:
            if not es_valida_direccion(direccion)['status']:
                response = {'status': False, 'message': 'Todas las direcciones deben ser validas'}, 200
                break
        return response

    return jsonify(validar_listado_direcciones(data_orden))
