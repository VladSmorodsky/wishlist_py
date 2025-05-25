import os

from aio_pika import connect, ExchangeType, Message
from dotenv import load_dotenv

load_dotenv()

from rabbitmq.constants import WISH_EXCHANGE_NAME, BindEvent


class RabbitMQManager:
    """
    Context manager for rabbitmq connection
    """

    def __init__(self, routing_key: BindEvent = BindEvent.GET_WISHES):
        self.broker_url = os.getenv('RABBITMQ_URL')
        self.exchange_name = WISH_EXCHANGE_NAME
        self.routing_key = routing_key.value
        self.connection = None
        self.channel = None

    async def __aenter__(self):
        self.connection = await connect(self.broker_url)
        self.channel = await self.connection.channel()
        return self

    async def publish(self, message: str, exchange_name: str = None, routing_key: BindEvent = None):
        routing_key = routing_key if routing_key else self.routing_key
        exchange_name = exchange_name if exchange_name else self.exchange_name
        exchange = await self.channel.declare_exchange(exchange_name, ExchangeType.TOPIC, durable=True)
        message = Message(message.encode('utf-8'), content_type="application/json")
        await exchange.publish(
            message=message,
            routing_key=routing_key.value,
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
