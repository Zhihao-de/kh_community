import threading

import pika


class DelayMessageListener(threading.Thread):
    def order_callback(self, ch, method, properties, body):
        return None

    @staticmethod
    def _get_connection():
        conn_str = 'amqp://admin:admin@81.71.33.22:5672/%2F'
        # parameters = pika.URLParameters(settings.Rabbit_url)
        connection = pika.BlockingConnection(pika.URLParameters(conn_str))
        return connection

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()

        channel.queue_declare(queue='RetryQueue', durable=True)
        print('listening order expiration information')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.order_callback(), queue='RetryQueue')
        print('消费完成')
