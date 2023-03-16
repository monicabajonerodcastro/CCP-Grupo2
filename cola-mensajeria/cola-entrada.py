import pika, sys, os, json

HOST_RABBIT_MQ = 'rabbitmq'

def publish_queue(queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_RABBIT_MQ))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='',
                            routing_key=queue,
                            body=json.dumps(message))
    print("=== Mensaje enviado a {} ===".format(queue), flush=True)
    connection.close()


def redirect_message(body):
    body_decoded = body.decode("utf-8")
    body_json = json.loads(body_decoded)
    if body_json["operacion"]=='consultar_vendedor':
        publish_queue(queue="RequestUsuarios", message=body_json)
    elif body_json["operacion"]=='actualizar_orden':
        publish_queue(queue="RequestOrdenes", message=body_json)
    else:
        #TODO retornar
        print("ok")


def main(queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(HOST_RABBIT_MQ))
    channel = connection.channel()
    channel.queue_declare(queue=queue)

    def callback(ch, method, properties, body):
        redirect_message(body)
        print("=== Mensaje recibido ===")

    channel.basic_consume(queue=queue,
                            auto_ack=True,
                            on_message_callback=callback)

    print('*** Esperando mensajes {} ***'.format(queue))
    channel.start_consuming()


print(__name__)
if __name__ == '__main__':
    try:
        main("CCP-Queue")
    except KeyboardInterrupt:
        print('Interrupted', flush=True)
        try:
            sys.exit(0)
        except:
            os._exit(0)