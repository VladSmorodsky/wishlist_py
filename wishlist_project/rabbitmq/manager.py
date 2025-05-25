from pika import BlockingConnection, ConnectionParameters

from rabbitmq.constants import WISH_EXCHANGE_NAME, BindEvent


class RabbitMQManager:
    """
    Context manager for rabbitmq connection
    """

    def __init__(self, host: str, port: int, exchange: str = WISH_EXCHANGE_NAME,
                 routing_key_event: BindEvent = BindEvent.GET_WISHES):
        self.host = host
        self.port = port
        self.exchange = exchange
        self.routing_key = routing_key_event.value
        self.connection = None
        self.channel = None

    def __enter__(self):
        parameters = ConnectionParameters(host=self.host, port=self.port)
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()
        return self

    def publish(self, message: str, exchange: str = None, routing_key_event: BindEvent = None):
        routing_key = routing_key_event.value if routing_key_event else self.routing_key
        exchange = exchange if exchange else self.exchange
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.channel and self.channel.is_open:
            self.channel.close()
        if self.connection and self.connection.is_open:
            self.connection.close()
