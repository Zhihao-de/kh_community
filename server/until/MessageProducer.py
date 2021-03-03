import pika


# 新建连接，rabbitmq安装在本地则hostname为'localhost'


class MessageProducer:
    connection = None

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

    def produce(self, message):
        channel = self.connection.channel()
        channel.queue_declare(queue='sat')
        channel.basic_publish(exchange='', routing_key='sat', body=message)
        print(" [x] Sent %s" % message)

    def close(self):
        self.connection.close()
