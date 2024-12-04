import json
from dataclasses import dataclass
import pika

from domain.events.base import BaseEvent
from message_broker.event_factory.base import BaseEventFactory
from message_broker.producer.base import BaseProducer


@dataclass
class RabbitMQProducer(BaseProducer):
    factory: BaseEventFactory
    user: str
    password: str
    host: str
    port: int
    exchange_name: str

    def _declare_exchange(self, channel):
        channel.exchange_declare(exchange=self.exchange_name, exchange_type="fanout")

    def publish(self, event: BaseEvent):
        credentials = pika.PlainCredentials(self.user, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, "/", credentials))
        try:
            channel = connection.channel()

            self._declare_exchange(channel)

            message_body = json.dumps(self.factory.convert_event_to_message(event))
            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key="",
                body=message_body,
            )
        finally:
            connection.close()


@dataclass
class UserRabbitMQProducer(RabbitMQProducer):
    ...
