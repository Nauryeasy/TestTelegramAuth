from dataclasses import dataclass

from core.apps.telegram_auth.entities.telegram_user import TelegramUser
from core.apps.telegram_auth.events.base import BaseEventHandler, ET, ER
from core.apps.telegram_auth.events.telegram_user import TelegramUserCreatedEvent
from core.infra.cache_repositories.base import BaseCacheRepository
from core.infra.repositories.base import BaseTelegramUserRepository


@dataclass
class TelegramUserCreatedEventHandler(BaseEventHandler):

    telegram_user_repository: BaseTelegramUserRepository
    cache_repository: BaseCacheRepository

    def handle(self, event: TelegramUserCreatedEvent) -> None:
        telegram_user = TelegramUser(
            telegram_id=event.telegram_id,
            telegram_username=event.telegram_username,
            telegram_first_name=event.telegram_first_name,
            telegram_last_name=event.telegram_last_name,
        )

        telegram_user = self.telegram_user_repository.create(telegram_user)

        self.cache_repository.set_value(
            key=event.token,
            value=telegram_user.telegram_id,
            duration=60 * 60 * 24
        )
