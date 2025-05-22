import asyncio
import json
import os

from aio_pika import connect, ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from logger import get_logger
from rabbitmq.constants import WISH_QUEUE_NAME, WISH_EXCHANGE_NAME, BindEvent
from rabbitmq.consumer_handlers import get_wish_event_register
from rabbitmq.schemas import WishListSchema

logger = get_logger(__name__)


async def on_message(message: AbstractIncomingMessage):
    data = json.loads(message.body.decode("utf-8"))
    wish_data = WishListSchema(**data)
    wish_event_register = get_wish_event_register()
    handler = wish_event_register.handlers[message.routing_key]
    if handler is None:
        logger.error(f"No handler registered with routing_key {message.routing_key}")
        return
    await handler.handle(wish_data)
    logger.info(f"[x] Retrieve message: data={wish_data} key={message.routing_key}")


async def main():
    conn = await connect(os.getenv('RABBITMQ_URL'))
    channel = await conn.channel()
    wish_exchange = await channel.declare_exchange(WISH_EXCHANGE_NAME, ExchangeType.TOPIC, durable=True)
    queue = await channel.declare_queue(WISH_QUEUE_NAME)
    await queue.bind(wish_exchange, routing_key=f"{BindEvent.GET_WISHES.value}")
    await queue.consume(on_message)
    logger.info(f"[*] Waiting for messages. To exit press CTRL+C")
    # keep the loop running
    await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
