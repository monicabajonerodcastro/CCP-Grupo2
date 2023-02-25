from flask import Flask
from flask import jsonify, request
import requests
import pika
import pandas
import json

app = Flask(__name__)

@app.route('/plan-ruta-2', methods=['GET'])
def get():
    params = request.args
    fecha = params.get("fecha")
    cliente = params.get("cliente")
    
    try:
        resultado_consulta_ordenes = requests.get(url="http://orden:5005/ordenes?fecha={}&cliente={}".format(fecha, cliente))
    except:
        publicar()
        return jsonify({'status': False, 'message':"No hay conexión con el servicio"}), 200

    dictData = json.loads(resultado_consulta_ordenes.content)
    if validacion(dictData) == 'invalido':
        print("Validacion fallo # 2", flush=True)
        return jsonify({'status': False, 'message': 'Existen datos de ordenes que NO son correctos'}), 200
    else:
        return jsonify({'status': True, 'message': 'Los datos de ordenes son correctos'}), 200  


def check_registro(row):
    try:
        float(row['latitud'])
        float(row['longitud'])
        if float(row['latitud'])>=4.51360957443485 and float(row['latitud'])<=4.778211501715016 and float(row['longitud'])>=-74.23457623538577 \
           and float(row['longitud'])<=-74.02618417788635 and len(row['nombre_cliente'].strip())>0 and not pd.isna(row['fecha_entrega']):
            return "valido"
        else:
            return "invalido"
    except:
        return "invalido"
    

def validacion(dictData):
    df = pandas.DataFrame(dictData)
    df['fecha_entrega'] = pandas.to_datetime(df['fecha_entrega'], errors='coerce', infer_datetime_format=True)
    df['latitud'] = df['direccion'].apply(lambda x: x['latitud'])
    df['longitud'] = df['direccion'].apply(lambda x: x['longitud'])
    df['check_registro'] = df.apply(check_registro, axis=1)
    if len(df[df['check_registro']=='invalido']) > 0:
        return 'invalido'
    else:
        return 'valido'
    

def publicar():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue="plan_ruta")
    channel.basic_publish(exchange='',
                            routing_key='plan_ruta',
                            body="Consulta de direcciones - 3")
    print("[x] Mensaje enviado", flush=True)
    connection.close()