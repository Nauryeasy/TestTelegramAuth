from dataclasses import dataclass

from core.apps.telegram_auth.entities.base import BaseEntity


@dataclass(eq=False)
class TelegramUser(BaseEntity):
    telegram_id: int
    telegram_username: str
    telegram_first_name: str
    telegram_last_name: str
