import time

from redis import StrictRedis


def expire_assignmnet(assignment):
    assignment = IntentionAssignmentsModel.objects.get(intention__serial_number=assignment)
    assignment.flags = 1
    assignment.save()


def expire_order(order):
    cancelling_order = OrderModel.objects.get(serial_number=order)
    cancelling_order.flags = 4
    cancelling_order.save()


class Daemon:
    def __init__(self):
        self.redis = StrictRedis(host='106.54.170.236', port=6379)
        self.pubsub = self.redis.pubsub()

    # 订阅消息
    def createListener(self):
        self.pubsub.psubscribe('__keyevent@0__:expired')

    def set_value(self, key, value, cycle):
        self.redis.set(key, value, cycle)

    def get_value(self, key):
        return self.redis.get(key)

    def listen(self):
        while True:
            # 订阅过期消息
            message = self.pubsub.get_message()
            if message:
                print(message)
                mess = message.data
                if mess.startswith('LY'):
                    expire_assignmnet(mess)
                else:
                    expire_order(mess)
            else:
                time.sleep(1)


if __name__ == '__main__':
    demeno = Daemon()
    demeno.createListener()
    demeno.listen()
