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
channel.exchange_declare(exchange='logs', exchange_type='direct')

# channel.queue_declare(queue='A', durable=True)
channel.queue_declare(queue='B', durable=True)

# channel.queue_bind(exchange='logs', queue='A', routing_key='A')
channel.queue_bind(exchange='logs', queue='B', routing_key='B')



def callback(ch, method, properties, body):
    print(" [V] Received %r" % body.decode("utf-8"))


if __name__ == '__main__':
    try:
        channel.basic_consume(queue='B', on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
