from rabbitmq.constants import BindEvent
from rabbitmq.manager import RabbitMQManager


async def publish(message: str, exchange_name: str = None, routing_key: BindEvent = None):
    async with RabbitMQManager() as client:
        await client.publish(message=message, exchange_name=exchange_name, routing_key=routing_key)
