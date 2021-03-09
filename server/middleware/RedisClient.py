import redis

pool = redis.ConnectionPool()

r = redis.Redis(connection_pool=pool)
