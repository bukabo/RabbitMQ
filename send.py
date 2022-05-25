from constant import host
import pika
from time import sleep

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host,
                              port=5672,
                              virtual_host='/',
                              credentials=credentials))

channel = connection.channel()


def send(mess):
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='my-exch',
                          routing_key='A',
                          body=mess)
    print(f" [x] Sent '{mess}'")

def send_exch_declare(mess):
    channel.exchange_declare(exchange='logs')
    channel.basic_publish(exchange='logs',
                          routing_key='B',
                          body=mess)
    print(f" [x] Sent '{mess}'")


if __name__ == '__main__':
    for i in range(10):
        sleep(1)
        send_exch_declare(f'test message from den {i}')
    connection.close()
