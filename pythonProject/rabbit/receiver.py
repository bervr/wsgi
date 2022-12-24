import pika

rmq_host = 'mgf-dkr01.dalimo.ru'
rmq_port = '15672'
vhost = 'dalimo'
queue = 'bervr'
user = 'bervr'
password = '1q2w3e4rasdf'

creds = pika.credentials.PlainCredentials(username=user, password=password, erase_on_connect=False)
param = pika.ConnectionParameters(host=rmq_host, virtual_host=vhost, credentials=creds)
connection = pika.BlockingConnection(param)
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)


def callback(ch, method, proprties, body):
    print(f'[x] received message {body}')


channel.basic_consume(queue, on_message_callback=callback, auto_ack=False)
channel.start_consuming()
