from flask import Flask 
from flask import jsonify


app = Flask(__name__)

@app.route('/plan-ruta-1', methods=['GET'])
def get():
    response = {'message': 'Respuesta plan ruta # 1'}
    return jsonify(response)


