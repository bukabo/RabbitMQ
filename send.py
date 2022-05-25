import pika

credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(
    pika.ConnectionParameters('94.198.130.58',
                              port=5672,
                              virtual_host='/',
                              credentials=credentials))

channel = connection.channel()


def send():
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='my-exch',
                          routing_key='A',
                          body='test message from den')
    print(" [x] Sent 'Hello World!'")


send()
connection.close()
