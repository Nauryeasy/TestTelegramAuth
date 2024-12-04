import json
import logging

import pika
from dataclasses import dataclass

from core.application.mediator import Mediator
from core.infra.message_broker.consumer.base import BaseConsumer
from core.infra.message_broker.event_factory.base import BaseEventFactory


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(threadName)s] - %(levelname)s - %(message)s",
)


@dataclass
class RabbitMQConsumer(BaseConsumer):
    mediator: Mediator
    factory: BaseEventFactory
    host: str
    port: int
    user: str
    password: str
    exchange_name: str

    def _declare_exchange(self):
        print(self.user, self.password, self.host, self.port)
        credentials = pika.PlainCredentials(self.user, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, self.port, "/", credentials))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange_name, queue=queue_name)

        return connection, channel, queue_name

    def _callback(self, ch, method, properties, body):
        message_body = json.loads(body)
        logging.debug(f"Received message: {message_body}")
        event = self.factory.convert_message_to_event(message_body)

        self.mediator.handle_event(event)

    def subscribe(self):
        connection, channel, queue_name = self._declare_exchange()

        channel.basic_consume(queue=queue_name, on_message_callback=self._callback, auto_ack=True)

        channel.start_consuming()
