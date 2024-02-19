# flake8: noqa
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import aio_pika
from config import (
    RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST)


class RabbitMQConnection:
    def __init__(self):
        self._connection = None
        self._channel = None
        self._queue = None

    @classmethod
    async def get_connection(cls):
        cls._connection = await aio_pika.connect_robust(
            host=RABBITMQ_HOST,
            port=5672,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASS
        )
        cls._channel = await cls._connection.channel()
        cls._exchange = await cls._channel.declare_exchange("topic_exchange", type=aio_pika.ExchangeType.TOPIC)
        cls._queue = await cls._channel.declare_queue('email_queue', durable=True)
        await cls._queue.bind(cls._exchange, "add product/success register")
        return [cls._connection, cls._channel, cls._queue, cls._exchange]