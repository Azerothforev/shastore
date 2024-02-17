# flake8: noqa
import asyncio
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aio_pika import IncomingMessage
import aio_pika
from config import (
    RABBITMQ_USER, RABBITMQ_PASS, RABBITMQ_HOST)
from mail.service import EmailSender


async def listen_to_queue(
):
    connection = await aio_pika.connect_robust(
        host=RABBITMQ_HOST,
        port=5672,
        login=RABBITMQ_USER,
        password=RABBITMQ_PASS
    )
    channel = await connection.channel()

    queue = await channel.declare_queue('email_queue', durable=True)
    await queue.consume(process_message)


async def process_message(message: IncomingMessage):
    body = message.body.decode()
    print(body)
    if body.split()[1] == 'buy':
        await EmailSender.send_email_after_buying_product(body.split()[0])
    else:
        await EmailSender.send_email_after_register(body.split()[0])
    await message.ack()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(listen_to_queue())
    loop.run_forever()
