from constant import host
import pika
from time import sleep

# Создаем подключение
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host,
                              port=5672,
                              virtual_host='/',
                              credentials=credentials))
channel = connection.channel()


def send(mess):
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='',
                          routing_key='A',
                          body=mess)
    print(f" [x] Sent '{mess}'")


def send_exch_declare(mess, rout):
    # Обьявляем обменник (exchange)
    channel.exchange_declare(exchange='logs', exchange_type='direct')
    channel.basic_publish(exchange='logs', routing_key=rout, body=mess)
    print(f" [x] Sent '{mess}'")


if __name__ == '__main__':
    for i in range(20):
        sleep(1)
        send_exch_declare(f'test message from Денис {i} Aa', 'A')
        send_exch_declare(f'test message from Денис {i} Ac', 'C')
        send_exch_declare(f'test message from Денис {i} B', 'B')
        # send(f'test message from Денис {i}')x
    connection.close()
