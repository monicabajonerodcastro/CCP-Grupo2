from flask import Flask 
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/plan-ruta-3', methods=['GET'])
def get():
    response_ruta_1 = requests.get(url = "http://orden:5005/ordenes")
    data_1 = response_ruta_1.json()
    retorno=True
    for i in data_1:
        if i['nombre_cliente'] is not None and i['direccion']['latitud'] is not None and i['direccion']['longitud'] is not None:
            if not is_dataOk(i['nombre_cliente'],i['direccion']['latitud'],i['direccion']['longitud']):
                retorno =False
                break
        else:
            retorno =False
            break
    if(retorno):
        mensaje='Los datos son validos'
    else:
        mensaje='Los datos no son validos'
    response = {'message': mensaje, 'status': retorno}
    return jsonify(response), 200

def isNameOk(nombre):
    return nombre !=""

def is_float(variable):
    try:
        float(variable)
        return True
    except:
        return False

def isAddressOk(latitud, longitud):
    if is_float(latitud) and is_float(longitud) and latitud !="" and longitud !="":
        if (float(latitud)<= 4.778211501715016 and float(latitud) >= 4.51360957443485 and float(longitud)<= -74.02618417788635 and float(longitud) >= -74.23457623538577):
            return True
    return False

def is_dataOk(nombre, latitud, longitud):
    return isNameOk(nombre) and isAddressOk(latitud, longitud)


