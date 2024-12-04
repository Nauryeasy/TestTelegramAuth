from functools import lru_cache

import punq
from punq import Scope

from domain.events.telegram_user import TelegramUserCreatedEvent
from message_broker.event_factory.base import BaseEventFactory
from message_broker.event_factory.rabbit_factory import RabbitEventFactory
from message_broker.event_factory.telegram_user.event_to_message import telegram_user_created_event_to_message
from message_broker.producer.rabbit_mq_producer import UserRabbitMQProducer, RabbitMQProducer
from settings import Settings


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:

    container = punq.Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)

    def register_producers() -> None:
        container.register(
            UserRabbitMQProducer,
            instance=RabbitMQProducer(
                factory=container.resolve(BaseEventFactory),
                host=container.resolve(Settings).RABBIT_MQ_HOST,
                user=container.resolve(Settings).RABBITMQ_DEFAULT_USER,
                password=container.resolve(Settings).RABBITMQ_DEFAULT_PASS,
                port=container.resolve(Settings).RABBITMQ_PORT,
                exchange_name=container.resolve(Settings).USER_EXCHANGE,
            )
        )

    def init_event_factory() -> BaseEventFactory:
        factory = RabbitEventFactory()

        #  TODO: Register event converters

        factory.register_event(TelegramUserCreatedEvent, telegram_user_created_event_to_message)

        return factory

    container.register(BaseEventFactory, factory=init_event_factory, scope=Scope.singleton)
    register_producers()

    return container
