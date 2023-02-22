from flask import Flask 
from flask import jsonify


app = Flask(__name__)

@app.route('/plan-ruta-2', methods=['GET'])
def get():
    response = {'message': 'Respuesta plan ruta # 2'}
    return jsonify(response)


