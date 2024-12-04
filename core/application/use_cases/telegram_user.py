from dataclasses import dataclass

from core.application.use_cases.base import BaseUseCase
from core.apps.telegram_auth.entities.telegram_user import TelegramUser
from core.infra.cache_repositories.base import BaseCacheRepository
from core.infra.repositories.base import BaseTelegramUserRepository


@dataclass
class CreateTelegramUserUseCase(BaseUseCase):

    telegram_user_repository: BaseTelegramUserRepository
    cache_repository: BaseCacheRepository

    def __call__(
        self,
        token: str,
        telegram_id: int,
        telegram_username: str,
        telegram_first_name: str,
        telegram_last_name: str
    ):
        telegram_user = TelegramUser(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            telegram_first_name=telegram_first_name,
            telegram_last_name=telegram_last_name
        )

        self.telegram_user_repository.create(telegram_user)

        self.cache_repository.set_value(
            key=token,
            value=telegram_user.telegram_id,
            duration=3600
        )


@dataclass
class GetTelegramUserUseCase(BaseUseCase):

    telegram_user_repository: BaseTelegramUserRepository
    cache_repository: BaseCacheRepository

    def __call__(self, token: str) -> TelegramUser | None:
        telegram_id = self.cache_repository.get_value(token)
        if telegram_id is None:
            return None

        telegram_id = telegram_id.decode('utf-8')
        return self.telegram_user_repository.get_by_id(telegram_id)
