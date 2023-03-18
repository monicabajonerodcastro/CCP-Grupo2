import pika, sys, os, json, requests

HOST_RABBIT_MQ = 'rabbitmq'

def publish(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_RABBIT_MQ))
    channel = connection.channel()
    channel.queue_declare(queue="CCP-Queue")
    channel.basic_publish(exchange='',
                            routing_key="CCP-Queue",
                            body=json.dumps(message))
    print("========== Mensaje enviado a {} ==========".format("CCP-Queue"), flush=True)
    connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_RABBIT_MQ))
    channel = connection.channel()
    channel.queue_declare(queue="RequestUsuarios")

    def callback(ch, method, properties, body):
        print("========== Consulta de usuario recibida ==========", flush=True)
        body_decoded = body.decode("utf-8")
        body_json = json.loads(body_decoded)
        response_usuario = requests.get(url = "http://usuario:5002/usuario", json=body_json)
        response = {
            "operacion": "respuesta",
            "tipo_operacion": "consulta",
            "status": response_usuario.status_code,
            "orden": response_usuario.json()
        }
        publish(response)


    channel.basic_consume(queue="RequestUsuarios",
                            auto_ack=True,
                            on_message_callback=callback)

    print('********** Esperando mensajes (Usuarios) **********', flush=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        try:
            sys.exit(0)
        except:
            os._exit(0)