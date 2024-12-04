from dataclasses import dataclass

from core.apps.telegram_auth.events.base import BaseEvent


@dataclass(frozen=True)
class TelegramUserCreatedEvent(BaseEvent):
    token: str
    telegram_id: int
    telegram_username: str
    telegram_first_name: str
    telegram_last_name: str
