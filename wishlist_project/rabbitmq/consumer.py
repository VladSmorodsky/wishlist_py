import json
import os

import django
from pika import BlockingConnection, ConnectionParameters
from dotenv import load_dotenv

from logger import get_logger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wishlist_project.settings")
django.setup()
load_dotenv()

from rabbitmq.constants import WISH_EXCHANGE_NAME, BindEvent, TELEGRAM_REQUEST_QUEUE
from rabbitmq.handlers import get_wish_event_register
from rabbitmq.schemas import WishData

logger = get_logger(__name__)


def on_message(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    wish_data = WishData(**data)
    wish_event_register = get_wish_event_register()
    handler = wish_event_register.handlers[method.routing_key]
    if handler is None:
        logger.error(f'No handler registered with routing_key: {method.routing_key}')
        return
    handler.handle(wish_data)
    logger.info(f"Received event: {method.routing_key}, data: {data}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = BlockingConnection(
    ConnectionParameters(host=os.getenv("RABBITMQ_BROKER_HOST"), port=int(os.getenv("RABBITMQ_PORT", 5672))))
channel = connection.channel()
channel.exchange_declare(exchange=WISH_EXCHANGE_NAME, exchange_type="topic", durable=True)
channel.queue_declare(queue=TELEGRAM_REQUEST_QUEUE)
channel.queue_bind(exchange=WISH_EXCHANGE_NAME, queue=TELEGRAM_REQUEST_QUEUE, routing_key=BindEvent.CREATE_WISH.value)
channel.queue_bind(exchange=WISH_EXCHANGE_NAME, queue=TELEGRAM_REQUEST_QUEUE,
                   routing_key=BindEvent.GET_WISHES_REQUEST.value)
channel.basic_consume(queue=TELEGRAM_REQUEST_QUEUE, on_message_callback=on_message)
logger.info('Started consuming...')
channel.start_consuming()
