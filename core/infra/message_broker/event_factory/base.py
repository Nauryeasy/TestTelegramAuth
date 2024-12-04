from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.apps.telegram_auth.events.base import BaseEvent


@dataclass
class BaseEventFactory(ABC):

    @abstractmethod
    def convert_event_to_message(self, event: BaseEvent) -> dict:
        ...

    @abstractmethod
    def convert_message_to_event(self, message: dict) -> BaseEvent:
        ...
