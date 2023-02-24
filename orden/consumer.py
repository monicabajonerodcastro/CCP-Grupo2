import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue="plan_ruta")

    def callback(ch, method, properties, body):
        print("[x] Mensaje recibido %r" % body)

    channel.basic_consume(queue="plan_ruta",
                            auto_ack=True,
                            on_message_callback=callback)

    print('[x] Esperando mensajes...')
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