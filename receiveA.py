from constant import host, auth
import pika
import sys
import os

# Создаем подключение
credentials = pika.PlainCredentials(auth['login'], auth['pass'])
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host,
                              port=5672,
                              virtual_host='/',
                              credentials=credentials))
channel = connection.channel()

# Обьявляем обменник (exchange)
channel.exchange_declare(exchange='logs', exchange_type='direct')

# Обьявляем очередь
channel.queue_declare(queue='A', durable=True, auto_delete=True)
# channel.queue_declare(queue='B', durable=True, auto_delete=True)

# Создаем подписку на события (из какой очереди с каким ключем хотим получать сообщения)
channel.queue_bind(exchange='logs', queue='A', routing_key='C')
channel.queue_bind(exchange='logs', queue='A', routing_key='A')
# channel.queue_bind(exchange='logs', queue='B', routing_key='B')


def callback(ch, method, properties, body):
    print(" [V] Received %r" % body.decode("utf-8"))


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
