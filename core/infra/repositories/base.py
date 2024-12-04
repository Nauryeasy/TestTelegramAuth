from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.telegram_auth.entities.base import BaseEntity
from core.apps.telegram_auth.entities.telegram_user import TelegramUser


@dataclass
class BaseRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> BaseEntity:
        ...

    @abstractmethod
    def create(self, entity: BaseEntity) -> BaseEntity:
        ...

    @abstractmethod
    def check_exists(self, entity: BaseEntity) -> bool:
        ...


@dataclass
class BaseTelegramUserRepository(BaseRepository):
    @abstractmethod
    def get_by_id(self, id: int) -> TelegramUser:
        ...

    @abstractmethod
    def create(self, entity: TelegramUser) -> TelegramUser:
        ...

    @abstractmethod
    def check_exists(self, entity: TelegramUser) -> bool:
        ...
