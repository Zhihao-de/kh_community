import pika


class MessageCosumer:
    def __init__(self, host, username, password):
        self.hostname = host
        self.port = 5672
        self.username = username
        self.password = password

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(host=self.hostname, port=5672, virtual_host='/', credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        return connection

    def consume(self, message):
        channel = self.connection.channel()
        channel.queue_declare(queue='sat')
        channel.basic_publish(exchange='', routing_key='sat', body=message)
        print(" [x] Sent %s" % message)

    def close(self):
        self.connection.close()


hostname = '81.71.33.22'
credentials = pika.PlainCredentials('admin', 'admin')
parameters = pika.ConnectionParameters(host=hostname, port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters)

# 创建通道
channel = connection.channel()
channel.queue_declare(queue='sat')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


# 告诉rabbitmq使用callback来接收信息
channel.basic_consume('sat', callback)

# 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理,按ctrl+c退出
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
