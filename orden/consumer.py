import pika, sys, os, json, requests

def publish(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="CCP-Queue")
    channel.basic_publish(exchange='',
                            routing_key="CCP-Queue",
                            body=json.dumps(message))
    print("=== Mensaje enviado a {} ===".format("CCP-Queue"), flush=True)
    connection.close()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="RequestOrdenes")

    def callback(ch, method, properties, body):
        print("=== Actualización de orden recibida ===")
        body_decoded = body.decode("utf-8")
        body_json = json.loads(body_decoded)
        response_ordenes = requests.post(url = "http://127.0.0.1:5000/orden", json=body_json)
        response = {
            "operacion": "respuesta",
            "status": response_ordenes.status_code,
            "orden": response_ordenes.json()
        }
        publish(response)


    channel.basic_consume(queue="RequestOrdenes",
                            auto_ack=True,
                            on_message_callback=callback)

    print('*** Esperando mensajes ***')
    channel.start_consuming()


print(__name__)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        try:
            sys.exit(0)
        except:
            os._exit(0)