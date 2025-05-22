from rabbitmq.constants import BindEvent
from rabbitmq.manager import RabbitMQManager
from wishlist_project.settings import RABBITMQ_PORT, RABBITMQ_BROKER_HOST


def publish(message, routing_key: BindEvent = None):
    with RabbitMQManager(host=RABBITMQ_BROKER_HOST, port=RABBITMQ_PORT) as client:
        client.publish(message=message, routing_key_event=routing_key)
