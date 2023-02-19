from flask import Flask 
from flask import jsonify


app = Flask(__name__)

@app.route('/plan-ruta', methods=['GET'])
def crear():
    response = {'message': 'Respuesta Crear Ruta'}
    return jsonify(response)
