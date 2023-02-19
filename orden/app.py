from flask import Flask 
from flask import jsonify


app = Flask(__name__)

@app.route('/ordenes', methods=['GET'])
def get():
    response = {'message': 'Respuesta Ordenes'}
    return jsonify(response)
