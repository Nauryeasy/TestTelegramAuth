import json
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type, Callable

from domain.events.base import BaseEvent
from message_broker.event_factory.base import BaseEventFactory


@dataclass()
class RabbitEventFactory(BaseEventFactory):
    event_to_message_map: dict[Type[BaseEvent], Callable] = field(
        default_factory=dict, kw_only=True
    )

    message_to_event_map: dict[str, Callable] = field(
        default_factory=dict, kw_only=True
    )

    def register_event(self, event_type: Type[BaseEvent], converter: Callable):
        self.event_to_message_map[event_type] = converter

    def register_message(self, event_type: str, converter: Callable):
        self.message_to_event_map[event_type] = converter

    def convert_event_to_message(self, event: BaseEvent) -> dict:
        return self.event_to_message_map[type(event)](event)

    def convert_message_to_event(self, message: dict) -> BaseEvent:
        return self.message_to_event_map[message['type']](message)

