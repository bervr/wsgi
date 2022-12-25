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
channel.basic_publish(exchange='', routing_key=queue, body='Hello World!')
print('sent "Hello World!"')
connection.close()