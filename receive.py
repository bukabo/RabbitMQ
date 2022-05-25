from constant import host
import pika
import sys
import os

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host,
                              port=5672,
                              virtual_host='/',
                              credentials=credentials))

channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [V] Received %r" % body)


if __name__ == '__main__':
    try:
        channel.basic_consume(queue='A', on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
