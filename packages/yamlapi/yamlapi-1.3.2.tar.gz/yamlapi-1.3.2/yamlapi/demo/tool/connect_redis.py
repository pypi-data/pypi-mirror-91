import redis

from setting.project_config import *


class ConnectRedis(object):
    # 封装redis-py的增删改查

    def __init__(self):
        # 初始化
        try:
            self.pool = redis.ConnectionPool(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                password=redis_password,
                max_connections=20,
                decode_responses=True,
                encoding='utf-8',
                socket_connect_timeout=15,
                socket_timeout=15,
            )
            # 连接池配置
        except Exception as e:
            logger.error("初始化Redis连接池发生错误：{}", e)
            raise e

    def insert_redis_str_one(self, key, value):
        """
        插入Redis，str类型，一条数据
        :param key: 键
        :param value: 值
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            conn.set(key, value)
            logger.info("redis插入一条str数据成功")
        except Exception as e:
            logger.error("redis插入一条str数据发生错误：{}", e)

    def insert_redis_str_many(self, kvs):
        """
        插入Redis，str类型，多条数据
        :param kvs: 插入的键值对，字典格式
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            conn.mset(kvs)
            logger.info("redis插入多条str数据成功")
        except Exception as e:
            logger.error("redis插入多条str数据发生错误：{}", e)

    def insert_redis_list(self, key, *args):
        """
        插入Redis，list类型
        :param key: 键
        :param args: 值，元素个数不限
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            result = conn.rpush(key, *args)
            logger.info("redis插入list数据成功，键{}的元素个数为：{}", key, result)
        except Exception as e:
            logger.error("redis插入list数据发生错误：{}", e)

    def insert_redis_hash_one(self, name, key, value):
        """
        插入Redis，hash类型，一条数据
        :param name: hash名称
        :param key: hash键
        :param value: hash值
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            conn.hset(name, key, value)
            logger.info("redis插入一条hash数据成功")
        except Exception as e:
            logger.error("redis插入一条hash数据发生错误：{}", e)

    def insert_redis_hash_many(self, name, kvs):
        """
        插入Redis，hash类型，多条数据
        :param name: hash名称
        :param kvs: hash键值对，字典格式
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            conn.hmset(name, kvs)
            logger.info("redis插入多条hash数据成功")
        except Exception as e:
            logger.error("redis插入多条hash数据发生错误：{}", e)

    def insert_redis_set(self, key, *args):
        """
        插入Redis，set类型
        :param key: 键
        :param args: 值，元素个数不限
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            result = conn.sadd(key, *args)
            logger.info("redis插入set数据成功，键{}的元素个数为：{}", key, result)
        except Exception as e:
            logger.error("redis插入set数据发生错误：{}", e)

    def insert_redis_zset(self, key, vss):
        """
        插入Redis，zset类型
        :param key: 键
        :param vss: 值与分数，字典格式，元素个数不限
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            result = conn.zadd(key, vss)
            logger.info("redis插入zset数据成功，键{}的元素个数为：{}", key, result)
        except Exception as e:
            logger.error("redis插入zset数据发生错误：{}", e)

    def delete_redis(self, key):
        """
        删除Redis
        :param key: 参数为Redis键
        :return:
        """

        conn = redis.StrictRedis(connection_pool=self.pool)
        # 打开redis连接

        try:
            if conn.exists(key):
                # 如果键存在
                result = conn.delete(key)
                logger.info("redis删除成功，删除的个数为：{}", result)
            else:
                logger.error("redis删除发生错误：键{}不存在", key)
        except Exception as e:
            logger.error("redis删除发生错误：{}", e)
