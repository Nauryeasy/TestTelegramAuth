import threading
from functools import lru_cache

import punq
from punq import Scope

from core.application.events.telegram_user import TelegramUserCreatedEventHandler
from core.application.mediator import Mediator
from core.application.use_cases.telegram_user import CreateTelegramUserUseCase, GetTelegramUserUseCase
from core.application.use_cases.token import GenerateTokenUseCase
from core.apps.telegram_auth.events.telegram_user import TelegramUserCreatedEvent
from core.infra.cache_repositories.base import BaseCacheRepository
from core.infra.cache_repositories.redis import RedisCacheRepository
from core.infra.message_broker.consumer.rabbit_consumer import RabbitMQConsumer
from core.infra.message_broker.event_factory.base import BaseEventFactory
from core.infra.message_broker.event_factory.rabbit_factory import RabbitEventFactory
from core.infra.message_broker.event_factory.telegram_user.message_to_event import \
    telegram_user_created_message_to_event
from core.infra.repositories.base import BaseTelegramUserRepository
from core.infra.repositories.telegram_user import TelegramUserRepository
from core.project.settings.main import *


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:

    container = punq.Container()

    container.register(BaseTelegramUserRepository, instance=TelegramUserRepository(), scope=Scope.singleton)

    container.register(BaseCacheRepository, instance=RedisCacheRepository(REDIS_HOST, REDIS_PORT), scope=Scope.singleton)

    container.register(CreateTelegramUserUseCase)
    container.register(GetTelegramUserUseCase)
    container.register(GenerateTokenUseCase)

    container.register(TelegramUserCreatedEventHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        mediator.register_event(
            event_type=TelegramUserCreatedEvent,
            handler=container.resolve(TelegramUserCreatedEventHandler)
        )

        return mediator

    def register_consumers() -> None:
        container.register(
            'user_consumer',
            instance=RabbitMQConsumer(
                mediator=container.resolve(Mediator),
                host=RABBIT_MQ_HOST,
                port=RABBIT_MQ_PORT,
                user=RABBIT_MQ_DEFAULT_USER,
                password=RABBIT_MQ_DEFAULT_PASS,
                exchange_name=USER_EXCHANGE,
                factory=container.resolve(BaseEventFactory),
            )
        )

    def init_event_factory() -> BaseEventFactory:
        factory = RabbitEventFactory()

        #  TODO: Register event converters

        factory.register_message('TelegramUserCreatedEvent', telegram_user_created_message_to_event)

        return factory

    container.register(Mediator, instance=init_mediator(), scope=Scope.singleton)

    container.register(BaseEventFactory, instance=init_event_factory(), scope=Scope.singleton)

    register_consumers()

    user_consumer = container.resolve('user_consumer')
    thread = threading.Thread(target=user_consumer.subscribe, daemon=True)

    thread.start()

    return container
